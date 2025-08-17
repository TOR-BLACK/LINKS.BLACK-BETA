"use client"; // Указываем, что компонент работает на клиенте

import { Locale } from "@/i18n/config"; // Импорт доступных локалей
import { setUserLocale } from "@/services/locale"; // Функция для установки выбранной локали
import { useLocale } from "next-intl"; // Хук для получения текущей локали
import Image from "next/image"; // Импорт компонента Next.js для работы с изображениями
import { useEffect, useRef, useState, useTransition } from "react"; // Импорт React-хуков

// Список доступных языков с названиями и флагами
const languages = [
  { title: "Русский", lang: "ru", flag: "/static/svg/icons/icon-flag-russia.svg" },
  { title: "English", lang: "en", flag: "/static/svg/icons/icon-flag-england.svg" },
  { title: "中文", lang: "zh", flag: "/static/svg/icons/icon-flag-china.svg" },
  { title: "Português", lang: "pt", flag: "/static/svg/icons/icon-flag-portugal.svg" },
  { title: "Español", lang: "es", flag: "/static/svg/icons/icon-flag-spain.svg" },
  { title: "हिन्दी", lang: "hi", flag: "/static/svg/icons/icon-flag-India.svg" },
  { title: "العربية", lang: "ar", flag: "/static/svg/icons/icon-flag-uae.svg" },
  { title: "Қазақша", lang: "kk", flag: "/static/svg/icons/icon-flag-kazakhstan.svg" },
  { title: "Հայկական", lang: "hy", flag: "/static/svg/icons/icon-flag-armenia.svg" },
  { title: "Azərbaycan", lang: "az", flag: "/static/svg/icons/icon-flag-azerbaijan.svg" },
  { title: "Română", lang: "ro", flag: "/static/svg/icons/icon-flag-romania.svg" },
  { title: "Кыргыз тили", lang: "ky", flag: "/static/svg/icons/icon-flag-kyrgyzstan.svg" },
  { title: "O'zbekiston", lang: "uz", flag: "/static/svg/icons/icon-flag-uzbekistan.svg" },
  { title: "Тоҷикӣ", lang: "tg", flag: "/static/svg/icons/icon-flag-tadjikistan.svg" },
  { title: "Türk", lang: "tr", flag: "/static/svg/icons/icon-flag-turkey.svg" },
  { title: "Українська", lang: "uk", flag: "/static/svg/icons/icon-flag-ukraine.svg" },
];

export default function HeaderLanguage() {
  const locale = useLocale(); // Получаем текущий язык
  const [isOpen, setIsOpen] = useState<boolean>(false); // Состояние открытия меню выбора языка
  const [isPending, startTransition] = useTransition(); // Состояние транзакции для смены языка
  const dropdownRef = useRef<HTMLDivElement>(null); // Ссылка на выпадающее меню

  // Обработчик закрытия меню при клике вне него
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        !isPending
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, [dropdownRef, isPending]);

  // Функция смены языка
  const handleSelectLanguage = (value: string) => {
    const locale = value as Locale;
    startTransition(() => {
      setUserLocale(locale); // Устанавливаем новый язык
      setIsOpen(false); // Закрываем меню
    });
  };

  return (
    <div className="button-circle-lang-wrapper" ref={dropdownRef}> {/* Обёртка для выпадающего меню */}
      <button className="button-circle-lang" onClick={() => setIsOpen(!isOpen)}> {/* Кнопка для открытия меню */}
        <svg className="button-circle__svg"> {/* Иконка глобуса */}
          <use href="/static/svg/sprite.svg#icon-languages"></use>
        </svg>
        <div className="text-xs" style={{ textTransform: "uppercase" }}> {/* Отображение текущего языка */}
          {locale}
        </div>
      </button>
      <div className={`button-circle-lang-menu ${isOpen ? "active" : ""}`}> {/* Меню выбора языка */}
        {languages.map((item) => (
          <div
            className={`button-circle-lang-menu-item ${
              item.lang === locale ? "active" : "" // Подсвечиваем текущий язык
            }`}
            key={item.lang}
            onClick={() => handleSelectLanguage(item.lang)}
          >
            <div className="button-circle-lang-menu-item__flag"> {/* Отображение флага */}
              <Image src={item.flag} width={20} height={20} alt="Flag" />
            </div>
            <div className="button-circle-lang-menu-item__text"> {/* Отображение названия языка */}
              {item.title}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
