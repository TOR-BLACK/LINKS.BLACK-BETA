"use client"; // Указываем, что компонент работает на клиенте

import Link from "next/link"; // Компонент для клиентской навигации
import CopyButton from "../CopyButton/CopyButton"; // Кнопка для копирования текста в буфер обмена
import { useTranslations } from "next-intl"; // Хук для работы с локализацией
import { useEffect, useState } from "react"; // Импорт React-хуков
import { Contact } from "@/types/dtos"; // Тип данных для контактов
import api from "@/lib/api"; // Функция для работы с API
import Colorer from "@/services/colorer"; // Компонент для управления цветами

export default function HeaderLinks() {
  const t = useTranslations("Header"); // Получаем переводы для шапки
  const [isHovered, setIsHovered] = useState(false); // Состояние наведения на кнопку
  const [isPressed, setIsPressed] = useState(false); // Состояние нажатия на кнопку
  const [contacts, setContacts] = useState<Contact[]>([]); // Список контактов

  useEffect(() => {
    const fetchContacts = async () => { 
      try {
        const response = await api<Contact[]>(`/contacts`); // Запрос контактов с API
        setContacts(response);
      } catch {
      } 
    };

    fetchContacts();
  }, []);

  // Фильтруем контакты по отделу
  const filterContactsByDepartment = (department: "opt" | "employment") =>
    contacts.filter((contact) => contact.department === department);  

  const departments: ("opt" | "employment")[] = ["opt", "employment"];

  return (
    <div className="header__links"> {/* Контейнер ссылок в шапке */}
      {departments.map((department) => (
        <div key={department} className="link-button-wrapper"> {/* Блок для отдела */}
          <div className="link-button"> {/* Кнопка отдела */}
            {department === "opt"
              ? t("headerInfo.salesDepartmentButton")
              : t("headerInfo.employmentDepartmentButton")}
            <svg className="link-button__icon">
              <use xlinkHref="/static/svg/sprite.svg#icon-cursor-click"></use>
            </svg>
          </div>
  
          <div className="link-button-menu"> {/* Меню контактов отдела */}
            {filterContactsByDepartment(department).map((contact) => (
              <div key={contact.id} className="link-button-menu__item"> {/* Один контакт */}
                <Link
                  href={`https://element.io/${contact.element}`}
                  className="link-button-menu__link"
                  onClick={async () => {
                    await navigator.clipboard.writeText(contact.element); // Копируем контакт в буфер
                  }}
                >
                  <svg className="link-button__icon">
                    <use xlinkHref="/static/svg/sprite.svg#icon-element"></use>
                  </svg>
                  <span>{contact.element}</span>
                </Link>
                <CopyButton text={contact.element} />
                {department !== "employment" && (
                  <a
                    href={`https://getsession.org/${contact.session}`}
                    className="link-button-menu__link"
                  >
                    <svg className="link-button__icon">
                      <use href="/static/svg/sprite.svg#icon-session"></use>
                    </svg>
                    <span>{contact.session}</span>
                  </a>
                )}
                {department !== "employment" && <CopyButton text={contact.session} />}

                {contact.is_telegram_active && (
                  <a
                    href={`https://t.me/${contact.telegram}`}
                    className="link-button-menu__link"
                  >
                    <svg className="link-button__icon">
                      <use href="/static/svg/sprite.svg#icon-telegram"></use>
                    </svg>
                    <span>@{contact.telegram}</span>
                  </a>
                )}
                {contact.is_telegram_active && <CopyButton text={contact.telegram} />}
              </div>
            ))}
          </div>

        </div>
      ))}
  
      <a 
          className="link-button brown" // Кнопка поддержки
          href="#"
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          onMouseDown={() => setIsPressed(true)}  
          onMouseUp={() => setIsPressed(false)}
        >   
          {t("headerInfo.supportButton")}
          <div className="link-button__icon"> 
            <Colorer
              src={"/static/svg/icons/icon-support-1.svg"}
              colorVar="--white-black16"
              hoverColorVar="--gold-white"
              pressColorVar="--gold-white"
              width={16}
              height={16}
              isHovered={isHovered}
              isPressed={isPressed}
            />
          </div>  
        </a>
    </div>
  );
}
