# Системные импорты
import os
import json
import logging
import traceback
from decimal import Decimal
import sys
import traceback
import logging.handlers
from django.conf import settings
from datetime import datetime
import time

# Библиотеки
import pandas as pd

# Django импорты
from django.db import transaction
from django.db.models import F, Q, Value
from django.db.models.functions import Lower, Trim
from django.core.files.uploadedfile import InMemoryUploadedFile

# Локальные импорты
from core.service.translator import update_object_translate
from core.celery import app, PARSE_PRODUCT_QUEUE

from apps.dv_info_site.models import (
    ProductUpdateFile, 
    ProductUpdateFileStatus, 
    Product, 
    ProductItem, 
    City
)

# Настройка логирования
logger = logging.getLogger('product_parsing')

# Создаем отдельный файловый логгер для максимально подробной диагностики
diagnostic_logger = logging.getLogger('product_parsing_diagnostic')
diagnostic_logger.setLevel(logging.DEBUG)

# Создаем файловый обработчик
file_handler = logging.handlers.RotatingFileHandler(
    '/tmp/product_parsing_diagnostic.log', 
    maxBytes=10*1024*1024,  # 10 МБ
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
diagnostic_logger.addHandler(file_handler)

# Глобальные константы
AVAILABILITY_MAPPING = {
    'Предзаказ': 'preorder',
    'В наличии': 'in_stock',
    'Нет в наличии': 'out_of_stock'
}

class ProductUpdateFileService:
    """Парсер для обновления продуктов по загруженному Excel файлу"""
    
    PRODUCT_TITLE_COL = 'Название товара'
    CITY_COL = 'Город'
    PRICE_COL = 'Цена'
    COUNT_COL = 'Количество'
    AVAILABILITY_COL = 'Статус наличия'

    PRODUCT_ITEM_KEY = '{product_item_title}_{product_title}_{city}'
    
    def processing_product_update_file(self, product_update_file_id: int):
        """
        Надёжный метод обработки файла обновления продуктов
        с максимально подробной диагностикой и обработкой гонок
        """
        diagnostic_logger.info(f'[СТАРТ] Начало обработки файла. ID: {product_update_file_id}')
        
        # Максимально подробная диагностика базы данных
        all_files = ProductUpdateFile.objects.all()
        diagnostic_logger.info(f'[ДИАГНОСТИКА] Всего файлов в базе: {all_files.count()}')
        diagnostic_logger.info(f'[ДИАГНОСТИКА] Список всех ID файлов: {list(all_files.values_list("id", flat=True))}')
        
        # Расширенная проверка существования файла с учетом возможных гонок
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Попытка получить объект файла напрямую
                product_update_file = ProductUpdateFile.objects.get(id=product_update_file_id)
                diagnostic_logger.info(f'[УСПЕХ] Файл найден. Детали: {product_update_file.__dict__}')
                break
            except ProductUpdateFile.DoesNotExist:
                if attempt < max_attempts - 1:
                    # Небольшая пауза между попытками для обработки возможных гонок
                    time.sleep(0.5)
                    diagnostic_logger.warning(f'[ПРЕДУПРЕЖДЕНИЕ] Попытка {attempt + 1}: Файл не найден. Ожидание...')
                else:
                    diagnostic_logger.critical(f'[КРИТИЧЕСКАЯ ОШИБКА] Файл с ID {product_update_file_id} не найден в базе после {max_attempts} попыток')
                    
                    # Максимально подробная диагностика при отсутствии файла
                    diagnostic_logger.critical(f'[ДИАГНОСТИКА] Полный список файлов:')
                    for file in all_files:
                        diagnostic_logger.critical(f'ID: {file.id}, Имя: {file.file.name}, Статус: {file.status}')
                    
                    return None
        
        # Расширенная диагностика файла
        diagnostic_logger.info(f'[ФАЙЛ] Имя: {product_update_file.file.name}')
        diagnostic_logger.info(f'[ФАЙЛ] Путь: {product_update_file.file.path}')
        diagnostic_logger.info(f'[ФАЙЛ] Текущий статус: {product_update_file.status}')
        
        # Множественные стратегии определения пути
        possible_paths = [
            product_update_file.file.path,  # Основной путь Django
            os.path.join(settings.MEDIA_ROOT, product_update_file.file.name),  # Путь через MEDIA_ROOT
            os.path.join(settings.MEDIA_ROOT, 'product-update-files', str(product_update_file.update_date.year), 
                         str(product_update_file.update_date.month), str(product_update_file.update_date.day), 
                         os.path.basename(product_update_file.file.path))  # Динамический резервный путь
        ]
        
        # Поиск существующего файла с повторными попытками
        file_path = None
        for attempt in range(max_attempts):
            file_path = next((path for path in possible_paths if os.path.exists(path)), None)
            if file_path:
                break
            time.sleep(0.5)
            diagnostic_logger.warning(f'[ПРЕДУПРЕЖДЕНИЕ] Попытка {attempt + 1}: Файл не найден по указанным путям')
        
        if not file_path:
            diagnostic_logger.critical(f'[ОШИБКА] Файл не найден. Проверенные пути: {possible_paths}')
            product_update_file.status = ProductUpdateFileStatus.ERROR
            product_update_file.save(update_fields=['status'])
            return None
        
        # Проверка доступности файла
        try:
            with open(file_path, 'rb') as f:
                f.read(1)  # Проверка чтения
        except (PermissionError, IOError) as e:
            diagnostic_logger.error(f'[ОШИБКА ДОСТУПА] Невозможно прочитать файл: {e}')
            product_update_file.status = ProductUpdateFileStatus.ERROR
            product_update_file.save(update_fields=['status'])
            return None
        
        # Определение типа файла
        file_extension = os.path.splitext(file_path)[1].lower()
        file_type_mapping = {
            '.csv': 'csv',
            '.xlsx': 'xlsx',
            '.xls': 'xlsx'
        }
        file_type = file_type_mapping.get(file_extension)
        
        if not file_type:
            diagnostic_logger.error(f'[ОШИБКА] Неподдерживаемый тип файла: {file_extension}')
            product_update_file.status = ProductUpdateFileStatus.ERROR
            product_update_file.save(update_fields=['status'])
            return None
        
        # Обновление статуса файла
        product_update_file.status = ProductUpdateFileStatus.PROCESSING
        product_update_file.save(update_fields=['status'])
        
        diagnostic_logger.info(f'[ПОДГОТОВКА] Начало обработки файла: {file_path}')
        
        try:
            with open(file_path, 'rb') as file:
                # Основная логика обработки файла
                self.processing_atomic(file, file_type)
            
            # Успешное завершение
            product_update_file.status = ProductUpdateFileStatus.PROCESSED
            product_update_file.save(update_fields=['status'])
            
            diagnostic_logger.info(f'[УСПЕХ] Файл {file_path} успешно обработан')
            return product_update_file
        
        except Exception as process_error:
            # Обработка ошибок при процессинге
            diagnostic_logger.error(f'[ОШИБКА ОБРАБОТКИ] {process_error}')
            diagnostic_logger.error(traceback.format_exc())
            
            product_update_file.status = ProductUpdateFileStatus.ERROR
            product_update_file.save(update_fields=['status'])
            
            return None

    def processing_atomic(self, file, file_type):
        """ Обновляет продукты по загруженному файлу """
        diagnostic_logger.debug(f'[DIAGNOSTIC] Начало обработки файла. Тип: {file_type}')
        diagnostic_logger.debug(f'[DIAGNOSTIC] Содержимое файла: {file}')
        
        try:
            # Определяем тип файла и читаем его
            if file_type == 'csv':
                data = pd.read_csv(file, encoding='utf-8')
            elif file_type == 'xlsx':
                data = pd.read_excel(file)
            else:
                raise ValueError(f'[ERROR] Неподдерживаемый тип файла: {file_type}')
            
            # Расширенная диагностика данных
            diagnostic_logger.debug(f'[DIAGNOSTIC] Исходные данные:\n{data.head()}')
            diagnostic_logger.debug(f'[DIAGNOSTIC] Типы данных:\n{data.dtypes}')
            diagnostic_logger.debug(f'[DIAGNOSTIC] Количество строк: {len(data)}')
            
            # Добавляем отладочные print
            print("Начало обработки файла")
            print(f"Тип файла: {file_type}")
            print(f"Количество строк: {len(data)}")
            print(f"Столбцы: {list(data.columns)}")
            
            # Принудительное преобразование типов
            data[self.CITY_COL] = data[self.CITY_COL].astype(str).str.lower().str.strip()
            data[self.PRODUCT_TITLE_COL] = data[self.PRODUCT_TITLE_COL].astype(str).str.lower().str.strip()
            data[self.PRICE_COL] = pd.to_numeric(data[self.PRICE_COL], errors='coerce').fillna(0)
            data[self.COUNT_COL] = pd.to_numeric(data[self.COUNT_COL], errors='coerce').fillna(0).astype(int)
            
            # Маппинг статусов наличия
            availability_mapping = {
                'в наличии': 'in_stock',
                'предзаказ': 'preorder',
                'нет в наличии': 'preorder'  # Если нужно обрабатывать особым образом
            }
            
            # Преобразование статуса наличия
            data[self.AVAILABILITY_COL] = data[self.AVAILABILITY_COL].str.lower().map(availability_mapping).fillna('preorder')
            
            # Удаление строк с пустыми значениями
            data = data.dropna(subset=[self.CITY_COL, self.PRODUCT_TITLE_COL])
            
            # Логирование после преобразований
            diagnostic_logger.debug(f'[DIAGNOSTIC] Данные после преобразования:\n{data.head()}')
            
            # Проверка обязательных столбцов
            required_columns = [
                self.CITY_COL, 
                self.PRODUCT_TITLE_COL, 
                self.PRICE_COL, 
                self.COUNT_COL, 
                self.AVAILABILITY_COL
            ]
            missing_columns = [col for col in required_columns if col not in data.columns]
            
            if missing_columns:
                diagnostic_logger.error(f'[ERROR] Отсутствуют обязательные столбцы: {missing_columns}')
                print(f"ОШИБКА: Отсутствуют столбцы {missing_columns}")
                raise ValueError(f'[ERROR] Отсутствуют обязательные столбцы: {missing_columns}')
            
            # Получение списка новых продуктов
            missing_products = self.get_missing_products(data)
            
            # Создание новых продуктов
            self.create_missing_products(missing_products)
            
            # Подготовка к обновлению товаров
            new_product_items = []
            
            # Разбиваем данные на части для эффективной обработки
            for product_data_chunk in self.split_dataframe_generator(df=data, chunk_size=2500):
                update_products = []
                
                # Получаем существующие товары с использованием аннотаций
                product_items = self.get_product_items(product_data_chunk)
                logger.info(f'[INFO] Найдено существующих товаров: {len(product_items)}')
                
                # Обработка каждой строки
                for _, product_data in product_data_chunk.iterrows():
                    product_item_key = self.PRODUCT_ITEM_KEY.format(
                        product_item_title=str(product_data[self.PRODUCT_TITLE_COL]).strip().lower(),
                        product_title=str(product_data[self.PRODUCT_TITLE_COL]).strip().lower(),
                        city=str(product_data[self.CITY_COL]).strip().lower()
                    )
                    
                    # Обновление существующего товара
                    if product_item_key in product_items:
                        product_item = product_items[product_item_key]
                        product_item.price = Decimal(product_data[self.PRICE_COL])
                        product_item.count = int(product_data[self.COUNT_COL])
                        product_item.availability_status = product_data[self.AVAILABILITY_COL]
                        update_products.append(product_item)
                    else:
                        # Сбор данных для новых товаров
                        new_product_items.append(product_data)
                
                # Массовое обновление существующих товаров
                if update_products:
                    ProductItem.objects.bulk_update(
                        objs=update_products, 
                        fields=['price', 'count', 'availability_status']
                    )
            
            # Создание новых товаров
            logger.info(f'[INFO] Новых товаров для создания: {len(new_product_items)}')
            self.create_new_product_items(new_product_items)
        
        except Exception as e:
            # Расширенная диагностика ошибок
            diagnostic_logger.error(f'[ERROR] Критическая ошибка: {e}')
            diagnostic_logger.error(traceback.format_exc())
            
            # Вывод полного стека вызова
            print("ПОЛНЫЙ СТЕК ВЫЗОВА:")
            traceback.print_exc()
            
            raise  # Перевыбрасываем исключение

    def get_missing_products(self, data):
        # Безопасное получение уникальных названий продуктов
        product_names = list(set(data[self.PRODUCT_TITLE_COL].str.lower().str.strip()))
        
        # Проверка существующих продуктов с использованием аннотаций
        existing_products = Product.objects.annotate(
            lower_title=Lower('title')
        ).filter(
            lower_title__in=product_names
        ).values_list('title', flat=True)
        
        # Фильтрация новых продуктов
        missing_products = [
            name for name in product_names 
            if name.lower() not in [str(p).lower() for p in existing_products]
        ]
        
        logger.debug(f'[DEBUG] Найдено новых продуктов: {len(missing_products)}')
        
        return missing_products

    def create_missing_products(self, missing_products):
        # Создание новых продуктов
        new_products = [
            Product(title=name) 
            for name in missing_products
        ]
        
        if new_products:
            Product.objects.bulk_create(new_products)
            logger.info(f'[INFO] Создано новых продуктов: {len(new_products)}')

    def create_new_product_items(self, new_product_items):
        # Создание новых товаров
        products = {p.title.lower(): p for p in Product.objects.all()}
        
        # Используем аннотацию для городов
        cities = City.objects.annotate(
            lower_name=Lower('name')
        )
        cities_dict = {c.lower_name: c for c in cities}
        
        product_items_to_create = []
        
        for _, product_data in pd.DataFrame(new_product_items).iterrows():
            product_title = str(product_data[self.PRODUCT_TITLE_COL]).lower().strip()
            city_name = str(product_data[self.CITY_COL]).lower().strip()
            
            product = products.get(product_title)
            city = cities_dict.get(city_name)
            
            if not product or not city:
                logger.warning(f'[WARNING] Не найден продукт или город: {product_title}, {city_name}')
                continue
            
            product_item = ProductItem(
                product=product,
                city=city,
                title=product_title,
                price=Decimal(product_data[self.PRICE_COL]),
                count=int(product_data[self.COUNT_COL]),
                availability_status=product_data[self.AVAILABILITY_COL]
            )
            product_items_to_create.append(product_item)
        
        if product_items_to_create:
            ProductItem.objects.bulk_create(product_items_to_create)
            logger.info(f'[INFO] Создано новых товаров: {len(product_items_to_create)}')

    def get_product_items(self, data):
        # Получение существующих товаров с использованием аннотаций
        product_titles = data[self.PRODUCT_TITLE_COL].str.lower().str.strip().unique()
        city_names = data[self.CITY_COL].str.lower().str.strip().unique()
        
        product_items = ProductItem.objects.annotate(
            lower_title=Lower('title'),
            lower_city_name=Lower('city__name')
        ).filter(
            lower_title__in=product_titles,
            lower_city_name__in=city_names
        ).select_related('product', 'city')
        
        # Создание словаря для быстрого доступа
        product_items_dict = {}
        for item in product_items:
            key = self.PRODUCT_ITEM_KEY.format(
                product_item_title=item.title.lower(),
                product_title=item.product.title.lower(),
                city=item.city.name.lower()
            )
            product_items_dict[key] = item
        
        return product_items_dict

    def split_dataframe_generator(self, df, chunk_size=2500):
        # Генератор для разбиения DataFrame на части
        for i in range(0, len(df), chunk_size):
            yield df.iloc[i:i + chunk_size]

# Создаем единственный экземпляр сервиса
product_update_file_service = ProductUpdateFileService()

@app.task(ignore_result=True, queue=PARSE_PRODUCT_QUEUE)
def processing_product_update_file(product_update_file_id: int):
    try:
        product_update_file_service.processing_product_update_file(product_update_file_id)
    except Exception as e:
        logger.critical(f'[CRITICAL] Критическая ошибка при обработке файла {product_update_file_id}: {e}')
        logger.critical(f'[CRITICAL] Трассировка: {traceback.format_exc()}')
        
        # Попытка обновить статус файла в случае ошибки
        try:
            product_update_file = ProductUpdateFile.objects.get(id=product_update_file_id)
            product_update_file.status = ProductUpdateFileStatus.ERROR
            product_update_file.save(update_fields=['status'])
        except Exception as update_error:
            logger.error(f'[ERROR] Не удалось обновить статус файла: {update_error}')
