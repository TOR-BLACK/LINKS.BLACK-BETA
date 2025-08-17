"use client"; // Указываем, что компонент работает на клиенте

import { useTranslations } from "next-intl"; // Хук для работы с локализацией
import Link from "next/link"; // Компонент для внутренней навигации без перезагрузки страницы
import { useEffect, useRef, useState } from "react"; // Импорт React-хуков
import { usePathname } from "next/navigation"; // Хук для получения текущего пути

export default function HeaderMobile() {
  const [isOpen, setIsOpen] = useState<boolean>(false); // Состояние открытия меню
  const dropdownRef = useRef<HTMLLIElement>(null); // Ссылка на контейнер меню
  const t = useTranslations("Header"); // Получаем переводы для заголовка
  const pathname = usePathname(); // Получаем текущий путь

  // Проверяем, активен ли путь
  const isActive = (path: string) => pathname === path;

  useEffect(() => {
    // Закрываем меню при клике вне него
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, [dropdownRef]);

  return (
    <div className="header-mobile"> {/* Контейнер мобильного меню */}
      <div className="header-mobile__container">
        <nav className="header-mobile-navbar-menu"> {/* Навигационное меню */}
          <ul className="header-mobile-navbar-menu-ul"> {/* Список ссылок */}
            <li className={`header-mobile-navbar-menu-ul__li ${isActive("/") ? "active" : ""}`}> {/* Главная страница */}
              <Link href="/">
                <svg>
                  <use xlinkHref="static/svg/sprite.svg#icon-home"></use>
                </svg>
                {t("headerNav.home")}
              </Link>
            </li>
            <li className={`header-mobile-navbar-menu-ul__li ${isActive("/wholesale") ? "active" : ""}`}> {/* Оптовые покупки */}
              <Link href="/wholesale">
                <svg>
                  <use xlinkHref="static/svg/sprite.svg#icon-wholesale"></use>
                </svg>
                {t("headerNav.wholesale")}
              </Link>
            </li>
            <li className={`header-mobile-navbar-menu-ul__li ${isActive("/work") ? "active" : ""}`}> {/* Работа */}
              <Link href="/work">
                <svg>
                  <use xlinkHref="static/svg/sprite.svg#icon-diplomat"></use>
                </svg>
                {t("headerNav.work")}
              </Link>
            </li>
            <li className={`header-mobile-navbar-menu-ul__li ${isActive("/contacts") ? "active" : ""}`}> {/* Контакты */}
              <Link href="/contacts">
                <svg>
                  <use xlinkHref="static/svg/sprite.svg#icon-chat"></use>
                </svg>
                {t("headerNav.contacts")}
              </Link>
            </li>
            <li className="header-mobile-navbar-menu-ul__li burger" ref={dropdownRef}> {/* Бургер-меню */}
              <button className={`button-burger ${isOpen ? "open" : ""}`} onClick={() => setIsOpen(!isOpen)}> {/* Кнопка открытия меню */}
                <span></span>
                <span></span>
                <span></span>
              </button>
              {t("headerNav.menuButton")}
              <div className={`button-burger-menu ${isOpen ? "active" : ""}`}> {/* Выпадающее меню */}
                <div className="button-burger-menu-ul">
                  <div className={`button-burger-menu-ul__li ${isActive("#") ? "active" : ""}`}> {/* Telegram */}
                    <Link href="#" onClick={() => setIsOpen(false)}>
                      <svg>
                        <use xlinkHref="static/svg/sprite.svg#icon-telegram-filling"></use>
                      </svg>
                      {t("headerNav.telegramButton")}
                    </Link>
                  </div>
                  <div className={`button-burger-menu-ul__li ${isActive("/mirror") ? "active" : ""}`}> {/* Зеркала */}
                    <Link href="/mirror" onClick={() => setIsOpen(false)}>
                      <svg>
                        <use xlinkHref="static/svg/sprite.svg#icon-mirror"></use>
                      </svg>
                      {t("headerNav.mirrors")}
                    </Link>
                  </div>
                  <div className={`button-burger-menu-ul__li ${isActive("/faq") ? "active" : ""}`}> {/* FAQ */}
                    <Link href="/faq" onClick={() => setIsOpen(false)}>
                      <svg>
                        <use xlinkHref="static/svg/sprite.svg#icon-gear"></use>
                      </svg>
                      {t("headerNav.faq")}
                    </Link>
                  </div>
                  <div className={`button-burger-menu-ul__li ${isActive("/partnership") ? "active" : ""}`}> {/* Партнерство */}
                    <Link href="/partnership" onClick={() => setIsOpen(false)}>
                      <svg>
                        <use xlinkHref="static/svg/sprite.svg#icon-handshake"></use>
                      </svg>
                      {t("headerNav.partnership")}
                    </Link>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
}