from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentProcessor(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()

    def __str__(self):
        return self.name


class PaymentWay(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    payment_processor = models.ForeignKey(PaymentProcessor, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f'{self.name}/{self.payment_processor}'


class Bank(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class CardIssuer(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=255)
    is_virtual = models.BooleanField(default=False)
    is_temporary = models.BooleanField(default=False)
    issuer = models.ForeignKey(CardIssuer, on_delete=models.RESTRICT, null=True)
    last_four_digits = models.CharField(max_length=4, null=True)

    def __str__(self):
        return f'{"[V]" if self.is_virtual else ""}' \
               f'{"[T]" if self.is_temporary else ""}' \
               f'[{self.issuer}]' \
               f'[{self.last_four_digits}]' \
               f' {self.name}'


class Currency(models.Model):
    name = models.CharField(max_length=255)
    minor_units = models.IntegerField()  # number of digits after decimal separator
    iso_code = models.CharField(max_length=10)  # ISO 4217, e.g. PLN; or pseudo-ISO, e.g. BTC for Bitcoin
    symbol = models.CharField(max_length=10)
    if_symbol_precedes_amount = models.BooleanField()  # true = $300, false = 300zł

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.iso_code


class Vault(models.Model):
    name = models.CharField(max_length=255)
    balance = models.IntegerField()  # most minor (e.g. cents instead of dollars)
    cards = models.ManyToManyField(Card)
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT, null=False)
    bank = models.ForeignKey(Bank, on_delete=models.RESTRICT, null=True)

    class VaultType(models.TextChoices):
        CURRENT = 'current', _('Current')
        SAVINGS = 'savings', _('Savings')
        SAFE = 'safe', _('Safe')

    type = models.CharField(
        choices=VaultType.choices,
        default=VaultType.CURRENT,
        max_length=10
    )

    def __str__(self):
        return self.name

    def get_least_minor_balance(self):
        return self.balance / (10 ** self.currency.minor_units)

    def get_iso_balance(self):
        return f'{self.get_least_minor_balance(self)} {self.currency.iso_code}'

    def get_symbol_balance(self):
        if self.currency.symbol_precedes_amount:
            return f'{self.currency.symbol}{self.get_least_minor_balance(self)}'
        else:
            return f'{self.get_least_minor_balance(self)}{self.currency.symbol}'


class EntityAddress(models.Model):
    street_name = models.CharField(max_length=255)
    building_number = models.IntegerField()
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    latitude = models.DecimalField(decimal_places=6, max_digits=9, null=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=9, null=True)

    class AddressType(models.TextChoices):
        STREET = 'st', _('Street')
        ALLEY = 'al', _('Alley')
        NBHD = 'nbhd', _('Neighborhood')

    type = models.CharField(
        choices=AddressType.choices,
        default=AddressType.STREET,
        max_length=10
    )

    def __str__(self):
        return f'{self.street_name} {self.type}, {self.city}'


class EntityChain(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField()

    def __str__(self):
        return self.name


class Entity(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(EntityAddress, on_delete=models.RESTRICT, null=True)
    chain = models.ForeignKey(EntityChain, on_delete=models.SET_NULL, null=True)
    website = models.URLField()

    class Meta:
        verbose_name_plural = 'Entities'

    def __str__(self):
        return f'{self.chain} {self.name} | {self.address}'


class Product(models.Model):
    name = models.CharField(max_length=255)
    ean_code = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=6)

    class AmountTypes(models.TextChoices):
        PIECES = 'pcs', _('Pieces')
        GRAMS = 'g', _('Grams')
        KILOGRAMS = 'kg', _('Kilograms')
        MILLILITERS = 'ml', _('Milliliters')
        LITRES = 'l', _('Litres')
        SECONDS = 'sec', _('Seconds')
        MINUTES = 'min', _('Minutes')
        HOURS = 'hr', _('Hours')
        MONTHS = 'mo', _('Months')
        YEARS = 'yr', _('Years')
        PAGES = 'pgs', _('Pages')

    amount_type = models.CharField(
        choices=AmountTypes.choices,
        default=AmountTypes.PIECES,
        max_length=5
    )

    class ProductCategory(models.TextChoices):
        SUPPORT = 'supp', _('Support')
        FOOD = 'food', _('Food')
        EARNINGS = 'earn', _('Earnings')
        CULTURE_AND_ENTERTAINMENT = 'cent', _('Culture&entertainment')
        ELECTRONICS = 'elec', _('Electronics')
        HEALTH_AND_HYGIENE = 'heal', _('Hygiene&health')
        TRANSPORT_AND_TRAVEL = 'trvl', _('Transport&travel')
        CLOTHING = 'clth', _('Clothing')
        OTHER = 'othr', _('Other')

    category = models.CharField(
        choices=ProductCategory.choices,
        max_length=4
    )

    def __str__(self):
        return f'{self.amount} {self.amount_type} of {self.name}'


class Transaction(models.Model):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    sender = models.ForeignKey(Entity,
                               related_name="%(app_label)s_%(class)s_related",
                               related_query_name="%(app_label)s_%(class)ss",
                               on_delete=models.RESTRICT,
                               null=False)
    recipient = models.ForeignKey(Entity, on_delete=models.RESTRICT, null=False)
    product = models.ManyToManyField(Product)
    receipt_image = models.ImageField(blank=True, null=True)

    class TransactionType(models.TextChoices):
        PURCHASE = 'pur', _('Purchase')
        SUBSCRIPTION = 'sub', _('Subscription')
        GIFT = 'gft', _('Gift')
        SALARY = 'sal', _('Salary')
        DONATION = 'don', _('Donation')
        CURRENCY_EXCHANGE = 'exc', _('Currency exchange')
        MONEY_TRANSFER = 'tra', _('Money transfer')
        CASHBACK_OR_RETURN = 'cbk', _('Cashback or return')
        OTHER = 'oth', _('Other')

    type = models.CharField(
        choices=TransactionType.choices,
        default=TransactionType.PURCHASE,
        max_length=3
    )

    def __str__(self):
        return f'{self.name} | from: {self.sender}, to: {self.recipient}'


class Payment(models.Model):
    amount = models.IntegerField()
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=False)
    payment_way = models.ForeignKey(PaymentWay, on_delete=models.CASCADE, null=False)
    vault = models.ForeignKey(Vault, on_delete=models.RESTRICT, null=False)

    def __str__(self):
        return f'{self.transaction.name} {self.amount}'
