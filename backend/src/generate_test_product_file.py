import openpyxl

# Создаем новую рабочую книгу
wb = openpyxl.Workbook()
ws = wb.active

# Заголовки столбцов
headers = [
    'Город', 
    'Название товара', 
    'Цена', 
    'Количество', 
    'Статус наличия'
]

ws.append(headers)

# Товар для "Город 1" - в наличии
ws.append([
    'Город 1', 
    'Тест из файла', 
    777, 
    77, 
    'В наличии'
])

# Товар для "Город 2" - предзаказ
ws.append([
    'Город 2', 
    'Тест из файла', 
    777, 
    77, 
    'Предзаказ'
])

# Сохраняем файл
wb.save('c:/OSPanel/domains/django/dvi-admin-backend/src/test_product_upload.xlsx')
print("Файл test_product_upload.xlsx создан успешно!")
