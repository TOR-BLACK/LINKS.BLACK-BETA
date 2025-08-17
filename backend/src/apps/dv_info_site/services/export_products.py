from io import BytesIO

import xlsxwriter
from django.db.models import QuerySet

from apps.dv_info_site.models import Product


def generate_excel_file(queryset: QuerySet[Product]) -> BytesIO:
    products_excel_file = BytesIO()
    workbook = xlsxwriter.Workbook(
        products_excel_file,
        options={
            'constant_memory': True
            # экономит память, но ограничевает функционал подробнее: https://xlsxwriter.readthedocs.io/working_with_memory.html
        }
    )
    worksheet = workbook.add_worksheet()
    row = 1
    for product in queryset:
        for product_item in product.items.all():
            worksheet.write(row, 0, product_item.city.name)
            worksheet.write(row, 1, product_item.title)
            worksheet.write(row, 2, product_item.price)
            worksheet.write(row, 4, product.title)
            row += 1
    workbook.close()
    products_excel_file.seek(0)
    return products_excel_file
