"use client"; // Указываем, что компонент рендерится на клиенте

import { FAQ } from "@/types/dtos"; // Импорт типа данных FAQ
import Image from "next/image"; // Импорт компонента Next.js для работы с изображениями
import React, { useState } from "react"; // Импорт React и хука состояния
import FAQsvg from "@/../public/static/svg/faq.svg"; // Импорт SVG-иконки
import MarkdownRenderer from "@/components/MarkdownRenderer/MarkdownRenderer"; // Импорт компонента для рендеринга Markdown
import Loader from "../Loader/Loader";

interface FAQDesktopProps {
  questionsAndAnswers: FAQ[]; // Массив вопросов и ответов
}

export default function FAQDesktop({ questionsAndAnswers }: FAQDesktopProps) {
  const [selectedId, setSelectedId] = useState<number | null>(null); // Состояние для хранения выбранного вопроса
  const [imageLoading, setImageLoading] = useState<boolean>(false);

  // Функция переключения выбранного вопроса
  const handleSelect = (id: number) => {
    setSelectedId((prev) => (prev === id ? null : id)); // Если уже выбран, снимаем выделение, иначе выбираем
    setImageLoading(true); // При смене вопроса снова показываем лоадер
  };

  const selectedFAQ = questionsAndAnswers.find((item) => item.id === selectedId); // Находим выбранный вопрос

  return (
    <div className="tabs faq"> {/* Основной контейнер FAQ */}
      <div className="tabs-tablist" role="tablist" aria-label="Questions"> {/* Список вопросов */}
        {questionsAndAnswers.map((item) => (
            <div
              key={item.id}
              className={`tabs-tablist__button ${
                selectedId === item.id ? "active" : "" // Подсвечиваем активный вопрос
              }`}
              role="tab"
              aria-selected={selectedId === item.id ? "true" : "false"} // Доступность
              id={`question-${item.id}`}
              onClick={() => handleSelect(item.id)} // Выбор вопроса
            >
            <MarkdownRenderer content={item.question} /> {/* Отображение вопроса с поддержкой Markdown */}
            <svg className="carriage-bottom"> {/* Иконка */}
              <use xlinkHref="/static/svg/sprite.svg#icon-carriage"></use>
            </svg>
          </div>
        ))}
      </div>
      {selectedFAQ ? ( // Если вопрос выбран, показываем его ответ
        <div className="tabs__content" role="tabpanel"> {/* Контейнер ответа */}
          {selectedFAQ.image ? (
            <div className="localhost-faq__img"> {/* Если есть изображение, показываем его */}
              {imageLoading && <Loader />}
              <Image
                src={selectedFAQ.image}
                alt="FAQ Image"
                width={610}
                height={250}
                priority={true}
                loading="eager"
                layout="intrinsic"
                onLoad={() => setImageLoading(false)} // Убираем лоадер после загрузки изображения
                onError={() => setImageLoading(false)} // Убираем лоадер даже если ошибка загрузки
                style={{ display: imageLoading ? "none" : "block" }} // Скрываем картинку, пока лоадер активен
              />
            </div>
          ) : (
            <div className="localhost-faq__img"> {/* Если изображения нет, показываем заглушку */}
              <svg>
                <use xlinkHref="static/svg/sprite.svg#icon-plug"></use>
              </svg>
            </div>
          )}
          <div className="localhost-faq__text"> {/* Блок с текстом ответа */}
            <MarkdownRenderer content={selectedFAQ.answer} />
          </div>
        </div>
      ) : (
        <div
          className="tabs__content main" // Заглушка, если ни один вопрос не выбран
          role="tabpanel"
          aria-labelledby="main"
        >
          <FAQsvg viewBox="0 0 372 193" /> {/* SVG-изображение FAQ */}
        </div>
      )}
    </div>
  );
}