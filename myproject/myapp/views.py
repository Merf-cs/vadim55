import os
import json
import xml.etree.ElementTree as ET
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .forms import SalesForm, UploadFileForm


# Функция сохранения данных в JSON и XML
def save_sales_data(data):
    folder = os.path.join(settings.BASE_DIR, 'sales_data')
    os.makedirs(folder, exist_ok=True)

    # путь JSON
    json_path = os.path.join(folder, 'sales.json')

    # создаём файл, если его нет
    if not os.path.exists(json_path):
        with open(json_path, 'w') as f:
            json.dump([], f)
    try:
        with open(json_path, 'r') as f:
            try:
                sales = json.load(f)
                if not isinstance(sales, list):  # Если данные не список, сбрасываем
                     sales = []
            except json.JSONDecodeError:
                sales =[] # Если файл повреждён
    
        # Добавляем новые данные
        sales.append(data)

        # Записываем данные обратно в файл
        with open(json_path, 'w') as f:
            json.dump(sales, f, indent=4, ensure_ascii=False)
    
    except Exception as e:
        print (f"Ошибка при работе с файлом JSON: {e}")

    # XML
    xml_path = os.path.join(folder, 'sales.xml')
    if os.path.exists(xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
    else:
        root = ET.Element('Sales')
        tree = ET.ElementTree(root)

    sale = ET.Element('Sale')
    for key, value in data.items():
        ET.SubElement(sale, key).text = str(value)
    root.append(sale)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)


# Форма добавления данных
def sales_form(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            save_sales_data(form.cleaned_data)
            return redirect('sales_list')
    else:
        form = SalesForm()
    return render(request, 'sales/sales_form.html', {'form': form})


# Функция загрузки файлов
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            folder = os.path.join(settings.BASE_DIR, 'sales_data')
            os.makedirs(folder, exist_ok=True)
            file_path = os.path.join(folder, file.name)

            with default_storage.open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Валидация загруженного файла
            if file.name.endswith('.json'):
                try:
                    with open(file_path, 'r') as f:
                        json.load(f)
                except json.JSONDecodeError:
                    os.remove(file_path)
                    return render(request, 'sales/upload_file.html', {'form': form, 'error': 'Невалидный JSON-файл!'})
            elif file.name.endswith('.xml'):
                try:
                    ET.parse(file_path)
                except ET.ParseError:
                    os.remove(file_path)
                    return render(request, 'sales/upload_file.html', {'form': form, 'error': 'Невалидный XML-файл!'})

            return redirect('sales_list')
    else:
        form = UploadFileForm()
    return render(request, 'sales/upload_file.html', {'form': form})


# Вывод списка данных
def sales_list(request):
    folder = os.path.join(settings.BASE_DIR, 'sales_data')
    files = os.listdir(folder) if os.path.exists(folder) else []
    sales = []

    for file_name in files:
        file_path = os.path.join(folder, file_name)
        
        if file_name.endswith('.json'):  # Если файл JSON
            try:
                with open(file_path, 'r') as f:
                    sales.append({'type': 'JSON', 'data': json.load(f)})
            except json.JSONDecodeError:  # Обработка повреждённого файла
                os.remove(file_path)  # Удаляем файл
                sales.append({'type': 'JSON', 'data': 'Файл был удалён из-за повреждения.'})
        
        elif file_name.endswith('.xml'):  # Если файл XML
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                sales.append({
                    'type': 'XML',
                    'data': [
                        {child.tag: child.text for child in sale}
                        for sale in root.findall('Sale')
                    ]
                })
            except ET.ParseError:  # Обработка повреждённого файла
                os.remove(file_path)  # Удаляем файл
                sales.append({'type': 'XML', 'data': 'Файл был удалён из-за повреждения.'})

    return render(request, 'sales/sales_list.html', {'sales': sales, 'files': files})