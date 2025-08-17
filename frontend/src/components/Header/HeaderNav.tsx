"use client"; // Указываем, что компонент работает на клиенте

import { useTranslations } from "next-intl"; // Хук для работы с локализацией
import Link from "next/link"; // Компонент для клиентской навигации
import { usePathname } from "next/navigation"; // Хук для получения текущего пути

export default function HeaderNav() {
  const pathname = usePathname(); // Получаем текущий путь
  const t = useTranslations("Header"); // Загружаем переводы для заголовка

  return (
    <nav className="navbar-menu"> {/* Контейнер навигационного меню */}
      <ul className="navbar-menu-ul"> {/* Список ссылок */}
        <li className={`navbar-menu-ul__li ${pathname === "/" ? "active" : ""}`}> {/* Главная страница */}
          <Link href="/">{t("headerNav.home")}</Link>
        </li>
        <li className={`navbar-menu-ul__li ${pathname === "/wholesale" ? "active" : ""}`}> {/* Оптовые покупки */}
          <Link href="/wholesale">{t("headerNav.wholesale")}</Link>
        </li>
        <li className={`navbar-menu-ul__li ${pathname === "/work" ? "active" : ""}`}> {/* Работа */}
          <Link href="/work">{t("headerNav.work")}</Link>
        </li>
        <li className={`navbar-menu-ul__li ${pathname === "/partnership" ? "active" : ""}`}> {/* Партнерство */}
          <Link href="/partnership">{t("headerNav.partnership")}</Link>
        </li>
        <li className={`navbar-menu-ul__li ${pathname === "/faq" ? "active" : ""}`}> {/* FAQ */}
          <Link href="/faq">{t("headerNav.faq")}</Link>
        </li>
        <li className={`navbar-menu-ul__li ${pathname === "/contacts" ? "active" : ""}`}> {/* Контакты */}
          <Link href="/contacts">{t("headerNav.contacts")}</Link>
        </li>
      </ul>
    </nav>
  );
}
