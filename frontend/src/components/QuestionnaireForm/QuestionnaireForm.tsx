"use client"; // Указываем, что компонент работает на клиенте

import { useLocale } from "next-intl"; // Импорт хука для получения текущей локали
import { useEffect, useState } from "react"; // Импорт хуков useEffect и useState
import api from "@/lib/api"; // Импорт API-запросов
import Loader from "@/components/Loader/Loader"; // Импорт компонента загрузки
import Link from "next/link"; // Импорт Link для навигации
import { Contact } from "@/types/dtos"; // Импорт типа данных Contact
import Image from "next/image"; // Импорт компонента для работы с изображениями
import CopyButton from "../CopyButton/CopyButton"; // Импорт кнопки копирования

interface QuestionnaireProps {
  base_url: string;
}

export default function QuestionnaireForm({ base_url }: QuestionnaireProps) {
  const [employmenTcontacts, setEmploymenTcontacts] = useState<Contact[]>([]); // Состояние для хранения списка контактов отдела трудоустройства
  const [loading, setLoading] = useState<boolean>(true); // Состояние загрузки данных
  const [showIframe, setShowIframe] = useState<boolean>(false); // Состояние для отображения анкеты

  const locale = useLocale(); // Получаем текущую локаль

  useEffect(() => {
    // Функция загрузки контактов трудоустройства
    const fetchContacts = async () => {
      setLoading(true);
      try {
        const allContacts = await api<Contact[]>("/contacts", {
          headers: { "Accept-Language": locale },
        });
        // Фильтруем контакты по департаменту 'employment'
        const employmentContacts = allContacts
          .filter((contact) => contact.department === "employment")
          .sort((a, b) => a.id - b.id);

        setEmploymenTcontacts(employmentContacts);
      } catch (error) {
        console.error("Error fetching contacts:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchContacts(); // Вызываем функцию загрузки при монтировании компонента
  }, [locale]); // Зависимость от локали

  return (
    <div className="localhost-questionnaire__content"> {/* Контейнер анкеты */}
      {loading ? (
        <Loader /> // Отображаем загрузку во время запроса данных
      ) : (
        <form className="localhost-questionnaire-form"> {/* Форма подачи анкеты */}
            <div className="localhost-contacts" id="contacts"> {/* Блок с контактами отдела трудоустройства */}
              <section>
                <div className="container">
                  <div className="localhost-contacts-content">
                    <div className="localhost-contacts-content__wrapper">
                      <h2 className="localhost-contacts-content__heading">СВЯЖИТЕСЬ С НАШИМ ОТДЕЛОМ ТРУДОУСТРОЙСТВА ПО КОНТАКТАМ НИЖЕ</h2>
                      {employmenTcontacts.map((contact) => (
                        <div className="localhost-contacts-card" key={contact.id}> {/* Карточка контакта */}
                          <div className="localhost-contacts-card-employee"> {/* Данные сотрудника */}
                            {contact.person_avatar && (
                              <div className="localhost-contacts-card-employee__avatar"> {/* Фото сотрудника */}
                                <Image
                                  src={contact.person_avatar}
                                  width={100}
                                  height={100}
                                  alt="Avatar"
                                />
                              </div>
                            )}
                            <div className="localhost-contacts-card-employee__name">
                              {contact.person} {/* Имя сотрудника */}
                            </div>
                          </div>
                          <div className="localhost-contacts-card__links_2"> {/* Блок с контактами */}
                            <div className="localhost-contacts-card-link"> {/* Контакт в Element */}
                              <div className="localhost-contacts-card-link__wrapper">
                                <svg>
                                  <use href="static/svg/sprite.svg#icon-element"></use>
                                </svg>
                                <div className="localhost-contacts-card-link__name">ELEMENT</div>
                              </div>
                              <div className="localhost-contacts-card-link__element"> {/* Информация и кнопка копирования */}
                                <div className="localhost-contacts-card-link__info">
                                  <Link href="#">{contact.element}</Link>
                                </div>
                                <div
                                  onClick={(e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                  }}
                                >
                                  <CopyButton text={contact.element} />
                                </div>
                              </div>
                            </div>
                            {contact.is_telegram_active && (
                            <div className="localhost-contacts-card-link"> {/* Контакт в Telegram */}
                              <div className="localhost-contacts-card-link__wrapper">
                                <svg>
                                  <use xlinkHref="static/svg/sprite.svg#icon-telegram"></use>
                                </svg>
                                <div className="localhost-contacts-card-link__name">TELEGRAM</div>
                              </div>
                              
                              <div className="localhost-contacts-card-link__element"> {/* Информация и кнопка копирования */}
                                <div className="localhost-contacts-card-link__info">
                                  <Link href="#">@{contact.telegram}</Link>
                                </div>
                                <div onClick={(e) => e.preventDefault()}>
                                  <CopyButton text={contact.telegram} />
                                </div>
                              </div>
                              
                            </div>
                            )}
                          </div>
                        </div>
                      ))}
                      <div className="localhost-contacts-heading"> {/* Подзаголовок перед анкетой */}
                        <div className="localhost-contacts-heading__info">
                          ЗАПОЛНИТЕ АНКЕТУ НИЖЕ И МЫ В АВТОМАТИЧЕСКОМ РЕЖИМЕ СВЯЖЕМ ВАС
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </section>
            </div>
            <button
              type="button"
              className="button iframe-toggle" // Кнопка показа анкеты
              onClick={() => setShowIframe((prev) => !prev)}
            >
              {showIframe ? "Закрыть анкету" : "Подать заявление"} {/* Изменяем текст в зависимости от состояния */}
            </button>
            {showIframe && (
              <div className="iframe-wrapper"> {/* Контейнер для iframe */}
                <iframe
                  src={base_url}
                  title="Анкета трудоустройства"
                  className="iframe-content"
                ></iframe>
              </div>
            )}
        </form>
      )}
    </div>
  );
}
