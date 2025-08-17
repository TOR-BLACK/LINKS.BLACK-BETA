"use client"; // Указываем, что компонент должен выполняться на клиенте (Next.js)

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import Breadcrumbs from "@/components/Breadcrumbs/Breadcrumbs";
import CopyButton from "@/components/CopyButton/CopyButton";
import api from "@/lib/api"; // Импорт функции API-запроса
import { Contact } from "@/types/dtos"; // Импорт интерфейса контактов
import Image from "next/image";
import Link from "next/link";
import Loader from "@/components/Loader/Loader"; // Компонент загрузки

// Главный компонент страницы контактов
export default function Contacts() {
  const locale = useLocale(); // Получаем текущий язык пользователя
  const [optContacts, setOptContacts] = useState<Contact[]>([]); // Состояние для хранения контактов отдела продаж
  const [employmenTcontacts, setEmploymenTcontacts] = useState<Contact[]>([]); // Состояние для хранения контактов отдела трудоустройства
  const [loading, setLoading] = useState<boolean>(true); // Флаг загрузки данных
  const t = useTranslations("ContactsPage"); // Функция перевода

  // useEffect для загрузки контактов с сервера при изменении локали
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); // Включаем индикатор загрузки

      try {
        // Запрос списка контактов с сервера
        const allContacts = await api<Contact[]>("/contacts", {
          headers: { "Accept-Language": locale }, // Передаем текущий язык
        });

        // Фильтруем контакты по отделам и сортируем их по id
        const optContacts = allContacts
          .filter((contact) => contact.department === "opt")
          .sort((a, b) => a.id - b.id);

        const employmenTcontacts = allContacts
          .filter((contact) => contact.department === "employment")
          .sort((a, b) => a.id - b.id);
        
        setOptContacts(optContacts); // Устанавливаем контакты отдела продаж
        setEmploymenTcontacts(employmenTcontacts); // Устанавливаем контакты отдела трудоустройства
      } catch (error) {
        console.error("Ошибка загрузки данных:", error); // Логируем ошибку
      } finally {
        setLoading(false); // Выключаем индикатор загрузки
      }
    };

    fetchData(); // Вызываем функцию загрузки данных
  }, [locale]); // Зависимость от локали (перезапрос при смене языка)

  // Если данные еще загружаются, отображаем спиннер загрузки
  if (loading) {
    return (
      <div className="localhost-contacts" id="contacts">
        <section>
          <div className="container">
            <Loader /> 
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="localhost-contacts" id="contacts">
      <section>
        <div className="container">
          {/* Навигационные "хлебные крошки" */}
          <Breadcrumbs page={t("breadcrumbs")} />

          {/* Заголовок страницы */}
          <div className="localhost-contacts-heading">
            <div className="localhost-contacts-heading__info">{t("heading")}</div>
          </div>

          <div className="localhost-contacts-content">
            {/* Блок контактов отдела продаж */}
            <div className="localhost-contacts-content__wrapper">
              <h2 className="localhost-contacts-content__heading">{t("sales")}</h2>
              {optContacts.map((contact) => (
                <div className="localhost-contacts-card" key={contact.id}>
                  <div className="localhost-contacts-card-employee">
                    {/* Отображение аватара, если есть */}
                    {contact.person_avatar && (
                      <div className="localhost-contacts-card-employee__avatar">
                        <Image
                          src={contact.person_avatar}
                          width={100}
                          height={100}
                          alt="Avatar"
                        />
                      </div>
                    )}
                    <div className="localhost-contacts-card-employee__name">
                      {contact.person}
                    </div>
                  </div>
                  
                  {/* Блок ссылок */}
                  <div className="localhost-contacts-card__links">
                    {/* Элемент-контакт */}
                    <div className="localhost-contacts-card-link">
                      <div className="localhost-contacts-card-link__wrapper">
                        <svg><use href="static/svg/sprite.svg#icon-element"></use></svg>
                        <div className="localhost-contacts-card-link__name">ELEMENT</div>
                      </div>
                      <div className="localhost-contacts-card-link__element">
                        {" "}
                        <div className="localhost-contacts-card-link__info">
                          <Link href="#">{contact.element}</Link>
                        </div>
                        <CopyButton text={contact.element} /> {/* Кнопка копирования */}
                      </div>
                    </div>

                    {/* Telegram-контакт (если активен) */}
                    {contact.is_telegram_active && (
                      <div className="localhost-contacts-card-link">
                        <div className="localhost-contacts-card-link__wrapper">
                          <svg><use xlinkHref="static/svg/sprite.svg#icon-telegram"></use></svg>
                          <div className="localhost-contacts-card-link__name">TELEGRAM</div>
                        </div>
                        <div className="localhost-contacts-card-link__element">
                          <div className="localhost-contacts-card-link__info">
                            <Link href="#">@{contact.telegram}</Link>
                          </div>
                          <CopyButton text={contact.telegram} />
                        </div>
                      </div>
                    )}

                    {/* Session-контакт */}
                    <div className="localhost-contacts-card-link">
                      <div className="localhost-contacts-card-link__wrapper">
                        <svg><use xlinkHref="static/svg/sprite.svg#icon-session"></use></svg>
                        <div className="localhost-contacts-card-link__name">SESSION</div>
                      </div>
                      <div className="localhost-contacts-card-link__element">
                        <div className="localhost-contacts-card-link__info">
                          <Link href="#">{contact.session}</Link>
                        </div>
                        <CopyButton text={contact.session} />
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Блок контактов по трудоустройству */}
            <div className="localhost-contacts-content__wrapper">
              <h2 className="localhost-contacts-content__heading">{t("work")}</h2>
              {employmenTcontacts.map((contact) => (
                <div className="localhost-contacts-card" key={contact.id}>
                  <div className="localhost-contacts-card-employee">
                    {contact.person_avatar && (
                      <div className="localhost-contacts-card-employee__avatar">
                        <Image
                          src={contact.person_avatar}
                          width={100}
                          height={100}
                          alt="Avatar"
                        />
                      </div>
                    )}
                    <div className="localhost-contacts-card-employee__name">
                      {contact.person}
                    </div>
                  </div>

                  {/* Блок ссылок */}
                  <div className="localhost-contacts-card__links_2">
                    <div className="localhost-contacts-card-link">
                      <div className="localhost-contacts-card-link__wrapper">
                        <svg><use href="static/svg/sprite.svg#icon-element"></use></svg>
                        <div className="localhost-contacts-card-link__name">ELEMENT</div>
                      </div>
                      <div className="localhost-contacts-card-link__element">
                        {" "}
                        <div className="localhost-contacts-card-link__info">
                          <Link href="#">{contact.element}</Link>
                        </div>
                        <CopyButton text={contact.element} />
                      </div>
                    </div>
                    {contact.is_telegram_active && (
                      <div className="localhost-contacts-card-link">
                        <div className="localhost-contacts-card-link__wrapper">
                          <svg><use xlinkHref="static/svg/sprite.svg#icon-telegram"></use></svg>
                          <div className="localhost-contacts-card-link__name">TELEGRAM</div>
                        </div>
                        <div className="localhost-contacts-card-link__element">
                          <div className="localhost-contacts-card-link__info">
                            <Link href="#">@{contact.telegram}</Link>
                          </div>
                          <CopyButton text={contact.telegram} />
                        </div>
                      </div>
                    )}
                    {/* <div className="localhost-contacts-card-link">
                      <div className="localhost-contacts-card-link__wrapper">
                        <svg>
                          <use xlinkHref="static/svg/sprite.svg#icon-session"></use>
                        </svg>
                        <div className="localhost-contacts-card-link__name">
                          SESSION
                        </div>
                      </div>
                      <div className="localhost-contacts-card-link__element">
                        <div className="localhost-contacts-card-link__info">
                          <Link href="#">@{contact.session}</Link>
                        </div>
                        <CopyButton text={contact.session} />
                      </div>
                    </div> */}
                  </div>
                </div>
              ))}

              {/* Дополнительная информация с кнопкой перехода */}
              <div className="localhost-contacts-heading">
                <div className="localhost-contacts-heading__info">
                  {t("info")} 
                  <a href="https://app.element.io/#/welcome" className="localhost-contacts-heading__info_button">
                    {t("elementbutton")}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
