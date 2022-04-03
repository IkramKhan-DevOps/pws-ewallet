import json

import requests
import stripe
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, DeleteView, ListView
from notifications.signals import notify

from cocognite import settings
from src.accounts.models import Wallet
from src.payments.forms import ConnectCreateForm, ConnectUpdateForm, ExternalAccountCreateForm, \
    ExternalAccountUpdateForm
from src.payments.models import Connect, ExternalAccount
from src.portals.admins.models import TopUp
import urllib

""" STRIPE REQUESTS"""


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, pk):
    top_up = get_object_or_404(TopUp.objects.filter(wallet__user=request.user, status='pen'), pk=pk)
    domain_url = settings.DOMAIN_URL
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'name': 'Balance Top Up',
            'quantity': 1,
            'currency': 'usd',
            'amount': int(str(top_up.total) + "00"),
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment-stripe:success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payment-stripe:cancel')),
    )
    top_up.stripe_payment_intent = session.id
    top_up.save()

    return redirect(session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        # product = Product.objects.get(id=product_id)

    return HttpResponse(status=200)


class SuccessView(TemplateView):
    template_name = 'payments/success.html'

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        top_up = get_object_or_404(TopUp, stripe_payment_intent=session_id)
        top_up.status = 'com'
        top_up.received = top_up.total - top_up.tax
        top_up.save()

        wallet = Wallet.objects.get(pk=top_up.wallet.pk)
        wallet.amount += top_up.total
        wallet.total_top_up += 1
        wallet.total_top_up_amount += top_up.total
        wallet.save()

        # TODO: notification
        notify.send(
            request.user,
            recipient=wallet.user,
            verb=f'Balance Load',
            level='info',
            description=f"You have successfully deposited an amount of ${top_up.total} to your wallet."
        )
        # ------------------

        return render(request, self.template_name)


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'


class ConnectAccount(DetailView):
    model = Connect


""" CONNECT ACCOUNT """
""" ---------------------------------------------------------------------------------------------------------------- """


class ConnectCreateView(View):
    template_name = 'payments/connect_form.html'
    context = {}
    form_class = ConnectCreateForm

    def get(self, request):
        self.context['form'] = self.form_class
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = ConnectCreateForm(data=request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, "Connect account added successfully - please verify")
        self.context['form'] = form
        return render(request, self.template_name, self.context)


class ConnectUpdateView(View):
    template_name = 'payments/connect_form.html'
    context = {}
    form_class = ConnectUpdateForm

    def get(self, request):
        self.context['form'] = ConnectUpdateForm(instance=Connect.objects.get(user=request.user))
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = ConnectUpdateForm(instance=Connect.objects.get(user=request.user), data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Connect account updated successfully - please verify")
        self.context['form'] = form
        return render(request, self.template_name, self.context)


class ConnectDetailView(DetailView):
    template_name = 'payments/connect_detail.html'
    model = Connect

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "Please create connect account first")
            return redirect('payment-stripe:connect-create')
        return super(ConnectDetailView, self).dispatch(request)

    def get_object(self, queryset=None):
        return get_object_or_404(Connect.objects.filter(), user=self.request.user)


class ConnectDeleteView(DeleteView):
    template_name = 'payments/connect_delete_confirm.html'
    model = Connect
    success_url = reverse_lazy("payment-stripe:connect-create")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "You don't have any account yet.")
            return redirect('payment-stripe:connect-create')
        return super(ConnectDeleteView, self).dispatch(request)

    def get_object(self, queryset=None):
        return get_object_or_404(Connect.objects.filter(), user=self.request.user)


""" EXTERNAL ACCOUNTS """


class ExternalAccountListView(ListView):

    def get_queryset(self):
        return ExternalAccount.objects.filter(connect__user=self.request.user)


class ExternalAccountCreateView(View):
    template_name = 'payments/externalaccount_form.html'
    context = {}
    form_class = ExternalAccountCreateForm

    def get(self, request):
        self.context['form'] = self.form_class
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = ExternalAccountCreateForm(data=request.POST)

        # 0:: OVERALL VALIDATIONS
        if form.is_valid():
            connect_account = request.user.get_stripe_account()

            # 1:: IF CONNECT ACCOUNT EXISTS
            if connect_account:
                form.instance.connect = connect_account
                e_account = form.save()
                messages.success(request, "External account added successfully")
                return redirect('payment-stripe:connect-external-account')
            else:
                messages.error(request, "Please create your connect account first")
                return redirect('payment-stripe:connect')

        self.context['form'] = form
        return render(request, self.template_name, self.context)


class ExternalAccountUpdateView(View):
    template_name = 'payments/externalaccount_form.html'
    context = {}
    form_class = ExternalAccountUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "You don't have any account yet.")
            return redirect('payment-stripe:connect')
        return super(ExternalAccountUpdateView, self).dispatch(request)

    def get(self, request, *args, **kwargs):
        e_account = get_object_or_404(ExternalAccount.objects.filter(connect__user=self.request.user), pk=self.kwargs['pk'])
        self.context['form'] = ExternalAccountUpdateForm(instance=e_account)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        e_account = get_object_or_404(ExternalAccount.objects.filter(connect__user=self.request.user), pk=self.kwargs['pk'])
        form = ExternalAccountUpdateForm(instance=e_account, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "External Account updated successfully")
            return redirect('payment-stripe:connect-external-account')
        self.context['form'] = form
        return render(request, self.template_name, self.context)


class ExternalAccountDeleteView(DeleteView):
    model = ExternalAccount
    success_url = reverse_lazy("payment-stripe:connect-external-account")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "You don't have any account yet.")
            return redirect('payment-stripe:connect-create')
        return super(ExternalAccountDeleteView, self).dispatch(request)

    def get_object(self, queryset=None):
        return get_object_or_404(ExternalAccount.objects.filter(connect__user=self.request.user), pk=self.kwargs['pk'])
