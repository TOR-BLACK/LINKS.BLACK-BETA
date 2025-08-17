"use client"; // Указываем, что компонент работает на клиенте

import { Partnership } from "@/types/dtos"; // Импорт типа данных Partnership
import { useTranslations, useLocale } from "next-intl"; // Импорт хуков для работы с локализацией
import Image from "next/image"; // Компонент Next.js для изображений
import Link from "next/link"; // Компонент Next.js для навигации
import { useState, useEffect } from "react"; // Импорт хуков React
import MarkdownRenderer from "@/components/MarkdownRenderer/MarkdownRenderer"; // Компонент для рендеринга Markdown
import api from "@/lib/api"; // Импорт функции API-запросов
import Loader from "../Loader/Loader"; // Импорт компонента загрузки

interface PartnershipProps {
  partnerships: Partnership[]; // Пропс, содержащий массив объектов партнёрств
}

export default function PartnershipItems({ partnerships: initialPartnerships }: PartnershipProps) {
  const [partnerships, setPartnerships] = useState<Partnership[]>(initialPartnerships || []); // Состояние для списка партнёрств
  const [selected, setSelected] = useState<Partnership | null>(null); // Состояние для выбора активного элемента
  const [loading, setLoading] = useState<boolean>(false); // Состояние загрузки
  const [isMobile, setIsMobile] = useState(false); // Состояние, проверяющее мобильное устройство

  const t = useTranslations("PartnershipPage"); // Получение переводов
  const locale = useLocale(); // Получение текущей локали

  useEffect(() => {
    const fetchPartnerships = async () => {
      try {
        setLoading(true);
        const data = await api<Partnership[]>("/partnerships", {
          headers: { "Accept-Language": locale },
        });
        setPartnerships(data.sort((a, b) => a.title.localeCompare(b.title)) || []);
      } catch (error) {
        console.error("Ошибка загрузки данных партнёрств:", error);
        setPartnerships([]);
      } finally {
        setLoading(false);
      }
    };
  
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };
  
    checkIsMobile();
    window.addEventListener("resize", checkIsMobile);
  
    fetchPartnerships();
  
    return () => {
      window.removeEventListener("resize", checkIsMobile);
    };
  }, [locale]); 

  // Функция обработки выбора элемента
  const handleSelect = (item: Partnership) => {
    setSelected((prev) => (prev?.id === item.id ? null : item));
  };

  if (loading) {
    return <Loader />; // Отображение компонента загрузки
  }

  return (
    <div className="localhost-partnership-content"> {/* Контейнер основного блока партнёрств */}
      <div className="accordion main"> {/* Основной аккордеон */}
        {partnerships.map((item) => (
          <div
            key={item.id}
            className={`accordion-item ${selected?.id === item.id ? "open" : ""}`}
            onClick={isMobile ? () => handleSelect(item) : undefined}
          >
            <div className="accordion-item-top"> {/* Верхняя часть аккордеона */}
              {item.image && (
                <div className="accordion-item__img"> {/* Изображение партнёрства */}
                  <Image src={item.image} width={300} height={150} alt={item.title} />
                </div>
              )}
              <div className="accordion-item-infoWbutton">
                <div className="accordion-item-info">
                  <div className="accordion-item-info__title">{item.title}</div> {/* Название партнёрства */}
                  <div className="accordion-item-description">
                    <div className="accordion-item-short_description__text"> {/* Краткое описание */}
                      <MarkdownRenderer content={item.short_description || ""} />
                    </div>
                  </div>
                </div>
                <div className="accordion-item__buttons"> {/* Кнопка */}
                  <Link className="button-functional black" href={`/questionnaire/`}>
                    <svg>
                      <use href="/static/svg/sprite.svg#icon-notepad"></use>
                    </svg>
                    {t("items.button")}
                  </Link>
                </div>
              </div>
            </div>
            <div className="accordion-item-subtop"> {/* Кнопка раскрытия */}
              <div className="button-open" onClick={(e) => { e.stopPropagation(); handleSelect(item); }}>
                {t("items.MoreDetails")}
                <svg className="carriage-bottom">
                  <use xlinkHref="/static/svg/sprite.svg#icon-carriage"></use>
                </svg>
              </div>
            </div>

            <div className={`accordion-item-bottom ${selected?.id === item.id ? "active" : ""}`} style={selected?.id === item.id ? { maxHeight: "600px" } : {}}>
              <div className="accordion-item-content"> {/* Контейнер описания */}
                <div className="accordion-item-content__wrapper">
                  <div className="accordion-item-description__title">
                    <MarkdownRenderer content={item.description || ""} /> {/* Полное описание */}
                  </div>
                </div>
              </div>
              <div className="button-open" onClick={(e) => { e.stopPropagation(); handleSelect(item); }}>
                {t("items.Hide")}
                <svg className="carriage-top">
                  <use xlinkHref="/static/svg/sprite.svg#icon-carriage"></use>
                </svg>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
