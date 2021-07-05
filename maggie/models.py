from django.db import models


class PaymentProcessor(models.Model):
    name = models.CharField()
    logo = models.ImageField()


class PaymentWay(models.Model):
    name = models.CharField()
    icon = models.ImageField()
    payment_processor = models.ForeignKey(PaymentProcessor,null=True)


class Bank(models.Model):
    name = models.CharField()
    logo = models.ImageField()


class CardIssuer(models.Model):
    name = models.CharField()
    logo = models.ImageField()


class Card(models.Model):
    name = models.CharField()
    is_virtual = models.BooleanField(default=False)
    is_temporary = models.BooleanField(default=False)
    issuer = models.ForeignKey(CardIssuer,on_delete=models.RESTRICT,null=True)


class Currency(models.Model):
    name = models.CharField()
    minor_units = models.IntegerField() # number of digits after decimal separator
    iso_code = models.CharField() # ISO 4217, e.g. PLN; or pseudo-ISO, e.g. BTC for Bitcoin
    symbol = models.CharField()
    if_symbol_precedes_amount = models.BooleanField() # true = $300, false = 300zł


class Vault(models.Model):
    name = models.CharField()
    balance = models.IntegerField() # most minor (e.g. cents instead of dollars)
    cards = models.ManyToManyField(Card)
    currency = models.ForeignKey(Currency,on_delete=models.RESTRICT,null=False)
    bank = models.ForeignKey(Bank,on_delete=models.RESTRICT,null=True)


    class VaultType(models.TextChoices):
        CURRENT = 'current', _('Current')
        SAVINGS = 'savings', _('Savings')
        SAFE = 'safe', _('Safe')

    type = models.CharField(
        choices=VaultType.choices,
        default=VaultType.CURRENT
    )

    def get_least_minor_balance(self):
        return self.balance/(10**self.currency.minor_units)

    def get_iso_balance(self):
        return f'{self.get_least_minor_balance(self)} {self.currency.iso_code}'

    def get_symbol_balance(self):
        if self.currency.symbol_precedes_amount:
            return f'{self.currency.symbol}{self.get_least_minor_balance(self)}'
        else:
            return f'{self.get_least_minor_balance(self)}{self.currency.symbol}'


class EntityAddress(models.Model):
    street_name = models.CharField()
    building_number = models.IntegerField()
    postal_code = models.CharField()
    city = models.CharField()
    latitude = models.DecimalField(decimal_places=6,max_digits=9,null=True)
    longitude = models.DecimalField(decimal_places=6,max_digits=9,null=True)


    class AddressType(models.TextChoices):
        STREET = 'st', _('Street')
        ALLEY = 'al', _('Alley')
        NBHD = 'nbhd', _('Neighborhood')

    type = models.CharField(
        choices=AddressType.choices,
        default=AddressType.STREET
    )


class EntityChain(models.Model):
    name = models.CharField()
    website = models.URLField()


class Entity(models.Model):
    name = models.CharField()
    address = models.ForeignKey(Address,on_delete=models.RESTRICT,null=True)
    chain = models.ForeignKey(EntityChain,on_delete=models.SET_NULL,null=True)
    website = models.URLField()


class Product(models.Model):
    name = models.CharField()
    ean_code = models.CharField(null=True)
    amount = models.DecimalField()

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

    amount_type = models.CharField(
        choices=AmountTypes.choices,
        default=AmountTypes.PIECES
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
        choices=TransactionCategory.choices,
        max_length=4
    )


class Payment(models.Model):
    amount = models.IntegerField()
    transaction = models.ForeignKey(Transaction)
    payment_way = models.ForeignKey(PaymentWay)
    vault = models.ForeignKey(Vault)


class Transaction(models.Model):
    name = models.CharField()
    timestamp = models.DateTimeField(auto_now=False,auto_add_now=False)
    sender = models.ForeignKey(Entity)
    recipient = models.ForeignKey(Entity)
    product = models.ManyToManyField(Product,on_delete=models.RESTRICT,null=True)
    receipt_image = models.ImageField()


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
