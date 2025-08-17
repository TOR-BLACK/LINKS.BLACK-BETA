"use server"; 

// Импортируем функции для работы с cookie в Next.js
import { cookies } from "next/headers";

// Импортируем тип `Locale` и значение `defaultLocale` из конфигурации локализации
import { Locale, defaultLocale } from "@/i18n/config";

// Название cookie, в котором будет храниться локаль пользователя
const COOKIE_NAME = "NEXT_LOCALE";

/**
 * Функция для получения локали пользователя из cookie.
 * Если cookie не установлено, возвращается локаль по умолчанию.
 */
export async function getUserLocale() {
  return cookies().get(COOKIE_NAME)?.value || defaultLocale; // Получаем значение cookie или используем локаль по умолчанию
}

/**
 * Функция для установки локали пользователя в cookie.
 * parameter locale - локаль, которую нужно установить (например, "en" или "ru").
 */
export async function setUserLocale(locale: Locale) {
  cookies().set(COOKIE_NAME, locale); // Устанавливаем cookie с новой локалью
}
