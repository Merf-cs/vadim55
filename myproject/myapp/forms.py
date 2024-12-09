from django import forms

STORAGE_CHOICES = [
    ('file', 'Файл'),
    ('database', 'База данных'),
]

class SalesForm(forms.Form):
    date = forms.DateField(label="Дата", widget=forms.DateInput(attrs={'type': 'date'}))
    product = forms.CharField(label="Продукт", max_length=100)
    quantity = forms.IntegerField(label="Количество", min_value=1)
    price = forms.DecimalField(label="Цена", max_digits=10, decimal_places=2)
    storage = forms.ChoiceField(label="Сохранить в", choices=STORAGE_CHOICES)

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Выберите файл (JSON или XML)")