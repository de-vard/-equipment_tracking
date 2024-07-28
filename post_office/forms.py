from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class AddEquipmentForm(forms.Form):
    barcode = forms.CharField(
        label='ШТРИХКОД\n',
        max_length=12,
        min_length=12,
        validators=[
            RegexValidator(
                regex='^\d{12}$',
                message='Штрих-код должен состоять только из 13 цифр.',
                code='invalid_barcode'
            ),
        ],
    )

    def clean_barcode(self):
        barcode = self.cleaned_data.get('barcode')
        if len(barcode) != 12:
            raise ValidationError('Штрих-код должен содержать ровно 12 цифр.')
        return barcode
