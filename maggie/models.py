from django.db import models


class Currency(models.Model):
    name = models.CharField()
    minor_units = models.IntegerField() # number of digits after decimal separator
    iso_code = models.CharField() # ISO 4217, e.g. PLN; or pseudo-ISO, e.g. BTC for Bitcoin
    symbol = models.CharField()
    symbol_precedes_amount = models.BooleanField() # true = $300, false = 300zł


class Wallet(models.Model):
    name = models.CharField()
    balance = models.IntegerField() # most minor (e.g. cents instead of dollars)
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT, null=False)

    def get_least_minor_balance(self):
        if self.currency.minor_units == 0:
            return self.balance
        else:
            return self.balance/(10**self.currency.minor_units)

    def get_iso_balance(self):
        return f'{self.get_least_minor_balance(self)} {self.currency.iso_code}'

    def get_symbol_balance(self):
        if self.currency.symbol_precedes_amount:
            return f'{self.currency.symbol}{self.get_least_minor_balance(self)}'
        else:
            return f'{self.get_least_minor_balance(self)}{self.currency.symbol}'


class Address(models.Model):
    class AddressType(models.TextChoices):
        STREET = 'st', _('Street')
        ALLEY = 'al', _('Alley')
        NBHD = 'nbhd', _('Neighborhood')

    type = models.CharField(
        choices=AddressType.choices,
        default=AddressType.STREET
    )
    name = models.CharField()
    building_number = models.IntegerField()
    postal_code = models.CharField()
    city = models.CharField()
    latitude = models.DecimalField(decimal_places=6,max_digits=9,null=True)
    longitude = models.DecimalField(decimal_places=6,max_digits=9,null=True)


class SellerChain(models.Model):
    name = models.CharField()
    address = models.ForeignKey(Address,on_delete=models.RESTRICT,null=True)
    website = models.URLField()


class Seller(models.Model):
    name = models.CharField()
    address = models.CharField()
    seller_chain = models.ForeignKey(Seller,on_delete=models.SET_NULL,null=True)


class Good(models.Model):
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

    name = models.CharField()
    EAN = models.CharField()
    amount = models.DecimalField()
    amount_type = models.CharField(
        choices=AmountTypes.choices,
        default=AmountTypes.PIECES
    )


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        PURCHASE = 'purchase', _('Purchase')
        RECURRING_PURCHASE = 'rec_pur', _('Recurring purchase')
        GIFT = 'gift', _('Gift')
        DONATION = 'donation', _('Donation')
        SALARY = 'salary', _('Salary')
        CURRENCY_EXCHANGE = 'exchange', _('Currency exchange')
        MONEY_TRANSFER = 'transfer', _('Money transfer')

    timestamp = models.DateTimeField(auto_now=False,auto_add_now=False)
    seller_address = models.CharField()
    place = models.CharField()
    goods = models.ForeignKey(Good,on_delete=models.RESTRICT,null=True)



