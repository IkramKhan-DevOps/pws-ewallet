from django.db import models
from django_resized import ResizedImageField
from src.accounts.models import Wallet


""" GENERAL """


class Country(models.Model):

    name = models.CharField(max_length=255, unique=True)
    short_code = models.CharField(max_length=2, unique=True)
    phone_code = models.CharField(max_length=5, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


""" MAIN """


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=100, default="bx bx-transfer")
    image = ResizedImageField(
        upload_to='accounts/images/profiles/', null=True, blank=True, size=[100, 100], quality=75, force_format='PNG',
        help_text='size of image must be 100*100 and format must be png image file', crop=['middle', 'center']
    )
    description = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return self.name


class TopUp(models.Model):
    STATUS_CHOICE = (
        ('com', 'Completed'),
        ('pen', 'Pending'),
        ('can', 'Cancelled'),
    )
    PAYMENT_METHOD_CHOICE = (
        ('str', 'Stripe'),
    )

    total = models.PositiveIntegerField()
    tax = models.PositiveIntegerField()
    received = models.PositiveIntegerField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True)
    stripe_payment_intent = models.CharField(max_length=20000)
    status = models.CharField(choices=STATUS_CHOICE, max_length=3, default='pen')
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICE, max_length=3, default='str')

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Top Ups"

    def __str__(self):
        return str(self.pk)


class Withdrawal(models.Model):
    STATUS_CHOICE = (
        ('com', 'Completed'),
        ('pen', 'Pending'),
        ('can', 'Cancelled'),
    )

    total = models.FloatField(verbose_name='Amount')
    tax = models.FloatField(default=0)
    received = models.FloatField(default=0)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True)
    connected_account = models.ForeignKey(
        'payments.ExternalAccount', on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(choices=STATUS_CHOICE, max_length=3)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Withdrawals"

    def __str__(self):
        return str(self.pk)


class Transaction(models.Model):
    STATUS_CHOICE = (
        ('com', 'Completed'),
        ('pen', 'Pending'),
        ('can', 'Cancelled'),
    )
    TYPE_CHOICE = (
        ('p2p', 'Peer To Peer'),
    )

    total = models.PositiveIntegerField(default=0)
    tax = models.PositiveIntegerField(default=0)
    received = models.PositiveIntegerField(default=0)
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True, related_name='sender+')
    receiver_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True, related_name='receiver+')
    type = models.CharField(choices=TYPE_CHOICE, max_length=3, default='p2p')
    status = models.CharField(choices=STATUS_CHOICE, max_length=3, default='pen')

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Transactions"

    def __str__(self):
        return str(self.pk)


""" TICKET SYSTEM """


class TicketType(models.Model):
    PRIORITY_CHOICES = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
    )
    name = models.CharField(max_length=255)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='m')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ticket(models.Model):
    PRIORITY_CHOICES = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
    )
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.pk)
