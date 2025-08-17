// utils/apiClient.ts
import { getUserLocale } from "@/services/locale"; // Импорт функции для определения локали пользователя

// Определяем интерфейс опций запроса, который расширяет стандартные настройки RequestInit
interface ApiFetchOptions extends RequestInit {
  revalidate?: number | false; // Указываем кэширование (false - отключает кэш)
  params?: Record<string, string | number | boolean>; // Параметры, передаваемые в URL
}

// Универсальная асинхронная функция для работы с API
export default async function api<T>(
  endpoint: string, // Путь к API-методу
  options: ApiFetchOptions = {} // Дополнительные опции запроса
): Promise<T> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL?.replace("http://", "https://");

  if (!baseUrl) {
    throw new Error("Базовый URL не определен в NEXT_PUBLIC_API_BASE_URL");
  }

  const locale = await getUserLocale();

  // Создаем заголовки для запроса, включая язык пользователя
  const headers = {
    "Accept-Language": locale,
    ...options.headers, // Добавляем возможные пользовательские заголовки
  };

  // Определяем время кэширования запроса (по умолчанию 60 секунд)
  const revalidate = typeof options.revalidate === "number" ? options.revalidate : 60;

  // Формируем полный URL, добавляя параметры запроса, если они есть
  const url = new URL(`${baseUrl}${endpoint}`);
  if (options.params) {
    Object.entries(options.params).forEach(([key, value]) => {
      url.searchParams.append(key, String(value)); // Преобразуем значения в строку и добавляем в параметры запроса
    });
  }

  // Настройки запроса, объединяющие переданные параметры и заголовки
  const fetchOptions: RequestInit = { ...options, headers };

  // Если выполняется на сервере (SSR), добавляем параметр кэширования для Next.js
  if (typeof window === "undefined") {
    fetchOptions.next = { revalidate };
  }

  // Выполняем запрос к API
  const response = await fetch(url.toString(), fetchOptions);

  // Проверяем успешность запроса, если нет - выбрасываем ошибку
  if (!response.ok) {
    throw new Error(`Request Error: ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}
