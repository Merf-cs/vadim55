from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import SalesForm
from .models import SalesRecord
import os
import json
import xml.etree.ElementTree as ET

def save_to_database(data):
    try:
        SalesRecord.objects.create(**data)
        return "Данные успешно сохранены в базу данных."
    except IntegrityError:
        return "Запись с такими данными уже существует."

def save_to_file(data, format):
    folder = os.path.join(settings.BASE_DIR, 'sales_data')
    os.makedirs(folder, exist_ok=True)

    if format == 'json':
        file_path = os.path.join(folder, 'sales.json')
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)
        with open(file_path, 'r+') as f:
            sales = json.load(f)
            sales.append(data)
            f.seek(0)
            json.dump(sales, f, indent=4, ensure_ascii=False)
        return "Данные успешно сохранены в файл JSON."
    
    elif format == 'xml':
        file_path = os.path.join(folder, 'sales.xml')
        if os.path.exists(file_path):
            tree = ET.parse(file_path)
            root = tree.getroot()
        else:
            root = ET.Element('Sales')
            tree = ET.ElementTree(root)

        sale = ET.Element('Sale')
        for key, value in data.items():
            ET.SubElement(sale, key).text = str(value)
        root.append(sale)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        return "Данные успешно сохранены в файл XML."

def sales_form(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            data = {
                'date': form.cleaned_data['date'],
                'product': form.cleaned_data['product'],
                'quantity': form.cleaned_data['quantity'],
                'price': form.cleaned_data['price'],
            }
            storage = form.cleaned_data['storage']
            if storage == 'file':
                message = save_to_file(data, 'json')  # Меняйте 'json' на 'xml', если нужно
            elif storage == 'database':
                message = save_to_database(data)
            return render(request, 'sales/success.html', {'message': message})
    else:
        form = SalesForm()
    return render(request, 'sales/sales_form.html', {'form': form})

def sales_list(request):
    # Определите источник: файлы или база
    source = request.GET.get('source', 'database')  # По умолчанию берём данные из базы

    if source == 'file':
        folder = os.path.join(settings.BASE_DIR, 'sales_data')
        file_path = os.path.join(folder, 'sales.json')
        data = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
    elif source == 'database':
        data = SalesRecord.objects.all()

    return render(request, 'sales/sales_list.html', {'data': data, 'source': source})

from django.http import JsonResponse

def sales_search(request):
    query = request.GET.get('q', '')
    results = SalesRecord.objects.filter(product__icontains=query).values('product', 'date')
    return JsonResponse(list(results), safe=False)


def sales_edit(request, pk):
    record = get_object_or_404(SalesRecord, pk=pk)

    if request.method == 'POST':
        form = SalesForm(request.POST, initial={
            'date': record.date,
            'product': record.product,
            'quantity': record.quantity,
            'price': record.price
        })
        if form.is_valid():
            # Обновляем данные в записи
            record.date = form.cleaned_data['date']
            record.product = form.cleaned_data['product']
            record.quantity = form.cleaned_data['quantity']
            record.price = form.cleaned_data['price']
            record.save()
            return HttpResponseRedirect(reverse('sales_list'))
    else:
        # Инициализируем форму данными из записи
        form = SalesForm(initial={
            'date': record.date,
            'product': record.product,
            'quantity': record.quantity,
            'price': record.price
        })

    return render(request, 'sales/sales_edit.html', {'form': form, 'record': record})

def sales_delete(request, pk):
    record = get_object_or_404(SalesRecord, pk=pk)

    if request.method == 'POST':
        record.delete()
        return HttpResponseRedirect(reverse('sales_list'))

    return render(request, 'sales/sales_confirm_delete.html', {'record': record})
