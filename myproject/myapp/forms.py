from django import forms

class SalesForm(forms.Form):
    date = forms.DateField(label="Дата", widget=forms.DateInput(attrs={'type': 'date'}))
    product = forms.CharField(label="Продукт", max_length=100)
    quantity = forms.IntegerField(label="Количество", min_value=1)
    price = forms.DecimalField(label="Цена", max_digits=10, decimal_places=2)

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Выберите файл (JSON или XML)")