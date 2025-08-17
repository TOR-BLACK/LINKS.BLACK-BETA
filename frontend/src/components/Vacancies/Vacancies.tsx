"use client"; // Указываем, что компонент работает на клиенте

import { Vacancy1 } from "@/types/dtos"; // Импорт типа вакансий
import { useTranslations, useLocale } from "next-intl"; // Хуки для работы с локализацией
import Link from "next/link"; // Импорт Link для навигации
import { useState, useEffect } from "react"; // Импорт хуков React
import MarkdownRenderer from "@/components/MarkdownRenderer/MarkdownRenderer"; // Компонент рендеринга Markdown
import Loader from "@/components/Loader/Loader"; // Компонент загрузки
import Image from "next/image"; // Компонент Next.js для работы с изображениями

interface VacanciesProps {
  vacancies: Vacancy1[]; // Список вакансий
  job1_url: string;
  job2_url: string;
}

export default function Vacancies({ vacancies: initialVacancies, job1_url, job2_url }: VacanciesProps) {
  const [selected, setSelected] = useState<Vacancy1 | null>(null); // Выбранная вакансия
  const [vacancies, setVacancies] = useState<Vacancy1[]>([]); // Список вакансий
  const [loading, setLoading] = useState(true); // Состояние загрузки
  const [filter, setFilter] = useState<string>("all"); // Фильтр вакансий
  const [isMobile, setIsMobile] = useState(false); // Проверка мобильного устройства

  const t = useTranslations("WorkPage"); // Локализация
  const locale = useLocale(); // Получаем текущую локаль

  useEffect(() => {
    setLoading(true);
  
    if (initialVacancies.length > 0) {
      setVacancies(initialVacancies);
      setLoading(false);
    }
  
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };
  
    checkIsMobile();
    window.addEventListener("resize", checkIsMobile);
    return () => window.removeEventListener("resize", checkIsMobile);
  }, [initialVacancies, locale]);

  // Форматирование зарплаты в зависимости от локали
  const formatSalary = (salary: number) => {
    return new Intl.NumberFormat(locale, {
      style: "decimal",
      useGrouping: true,
    }).format(salary);
  };

  // Обработка выбора вакансии
  const handleSelect = (item: Vacancy1) => {
    if (item.id === selected?.id) return setSelected(null);
    setSelected(item);
  };

  // Фильтрация вакансий по выбранному формату работы
  const handleFilterChange = (category: string) => {
    setFilter(category);
  };

  const filteredVacancies = vacancies.filter((item) => {
    return filter === "all" || item.work_format === filter;
  });

  if (loading) {
    return <Loader />; // Показываем загрузку, пока загружаются вакансии
  }

  return (
    <div className="localhost-work-content" key={locale}> {/* Основной контейнер */}
      <div className="tabs">
        {/* Фильтр вакансий */}
        <div className="tabs-tablist work" role="tablist" aria-label="Vacancies">
          {["all", "online", "offline", "no_experience"].map((category) => (
            <div
              key={category}
              className={`tabs-tablist__button ${filter === category ? "active" : ""}`}
              role="tab"
              aria-selected={filter === category}
              onClick={() => handleFilterChange(category)}
            >
              {category === "all" && (
                <svg>
                  <use href="/static/svg/sprite.svg#icon-all"></use>
                </svg>
              )}
              {category === "no_experience" && (
                <svg>
                  <use href="/static/svg/sprite.svg#icon-no_experience"></use>
                </svg>
              )}
              {category === "online" && (
                <svg>
                  <use href="/static/svg/sprite.svg#icon-online"></use>
                </svg>
              )}
              {category === "offline" && (
                <svg>
                  <use href="/static/svg/sprite.svg#icon-offline"></use>
                </svg>
              )}
              {t(`filters.${category}`)}
            </div>
          ))}
        </div>

        {/* Список вакансий */}
        <div className="tabs__content" role="tabpanel" aria-labelledby="allVacancies">
          <div className="accordion main">
            {filteredVacancies.map((item) => {
              item.description = item.description.replaceAll("\n", "<br/>")
              console.log(item)
              return (
              <div
                className={`accordion-item ${selected?.id === item.id ? "open" : ""}`}
                key={item.id}
                onClick={isMobile ? () => handleSelect(item) : undefined}
              >
                <div className="accordion-item-top"> {/* Верхний блок вакансии */}
                  {item.image_url && (
                    <div className="accordion-item__img">
                      <Image src={`${job2_url}/${item.image_url}`} width={300} height={150} alt="Work Image" />
                    </div>
                  )}
                  <div className="accordion-item-infoWbutton">
                    <div className="accordion-item-info">
                      <div className="accordion-item-info__title">{item.name}</div>
                      <div className="accordion-item-info__salary">
                        {t("salary.from")} {formatSalary(Number(item.salary))}₽{" "}
                        {t("salary.perMonth")}
                      </div>
                      <div className="accordion-item-description">
                        <div className="accordion-item-description__text">
                          <MarkdownRenderer
                            content={
                              item.description
                                ? item.description.length > 100
                                  ? `${item.description.slice(0, 100)}...`
                                  : item.description
                                : ""
                            }
                          />
                        </div>
                      </div>
                    </div>
                    <div className="accordion-item__buttons">
                      <div className="accordion-item__buttons_main">
                        <Link
                          className="button-functional black"
                          href={`${job1_url}/validateLogin.html?vacancy=${item.id}`}
                        >
                          <svg>
                            <use href="/static/svg/sprite.svg#icon-notepad"></use>
                          </svg>
                          {t("buttons.response")}
                        </Link>
                        {Boolean(item.calc_showed) && (
                          <Link className="button-functional black" href="/calculator">
                            <svg>
                              <use href="/static/svg/sprite.svg#icon-notepad"></use>
                            </svg>
                            {t("buttons.calculator")}
                          </Link>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="accordion-item-subtop"> {/* Кнопка раскрытия вакансии */}
                  <div className="button-open" onClick={() => handleSelect(item)}>
                    {t("buttons.MoreDetails")}
                    <svg
                      className="carriage-bottom"
                      xmlns="http://www.w3.org/2000/svg"
                      width="15"
                      height="15"
                      viewBox="0 0 15 15"
                      fill="none"
                    >
                      <use xlinkHref="/static/svg/sprite.svg#icon-carriage"></use>
                    </svg>
                  </div>
                </div>
                {/* Полное описание вакансии */}
                <div
                  className={`accordion-item-bottom ${selected?.id === item.id ? "active" : ""}`}
                  style={selected?.id === item.id ? { maxHeight: "100%" } : {}}
                >
                  <div className="accordion-item-content">
                    <div className="accordion-item-content__text">
                      <MarkdownRenderer content={item.description} />
                    </div>
                  </div>
                  <div className="button-open" onClick={() => handleSelect(item)}>
                    {t("buttons.Hide")}
                    <svg
                      className="carriage-top"
                      xmlns="http://www.w3.org/2000/svg"
                      width="15"
                      height="15"
                      viewBox="0 0 15 15"
                      fill="none"
                    >
                      <use xlinkHref="/static/svg/sprite.svg#icon-carriage"></use>
                    </svg>
                  </div>
                </div>
              </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  );
}