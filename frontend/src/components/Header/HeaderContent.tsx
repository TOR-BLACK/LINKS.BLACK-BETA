"use client"; // Указываем, что компонент работает на клиенте

import HeaderLinks from "./HeaderLinks"; // Компонент с дополнительными ссылками в шапке
import ThemeToggle from "../Theme/ThemeToggle"; // Компонент переключения темы
import HeaderNav from "./HeaderNav"; // Основное меню навигации
import Link from "next/link"; // Компонент для внутренней навигации
import HeaderLanguage from "./HeaderLanguage"; // Компонент выбора языка
import { useTranslations } from "next-intl"; // Хук для локализации

export default function HeaderContent() {
  const t = useTranslations("Header"); // Получение переведённых строк для шапки

  return (
    <div className="header__container"> {/* Основной контейнер шапки */}
      <div className="header__top"> {/* Верхний блок шапки */}
        <div className="text-s">{t("headerInfo.supportInfo")}</div> {/* Информация о поддержке */}
        <HeaderLinks /> {/* Компонент с дополнительными ссылками */}
      </div>
      <div className="header__bottom"> {/* Нижний блок шапки */}
        <Link className="header__logo" href="/"> {/* Логотип с ссылкой на главную страницу */}
          <svg>
            <use xlinkHref="/static/svg/sprite.svg#logo"></use>
          </svg>
        </Link>
        <HeaderNav /> {/* Навигация по сайту */}
        <div className="header__buttons"> {/* Блок кнопок справа */}
          <ThemeToggle /> {/* Переключатель темы (светлая/тёмная) */}
          <Link className="button-circle mirror" href="/mirror"> {/* Кнопка перехода на зеркало сайта */}
            <svg className="button-circle__svg">
              <use xlinkHref="/static/svg/sprite.svg#icon-mirror"></use>
            </svg>
          </Link>
          <HeaderLanguage /> {/* Выбор языка */}
        </div>
      </div>
    </div>
  );
}
