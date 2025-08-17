"use client"; // Указываем, что компонент работает на клиенте

import { FAQ } from "@/types/dtos"; // Импорт типа данных FAQ
import Image from "next/image"; // Импорт компонента Next.js для работы с изображениями
import { useState } from "react"; // Импорт хука состояния
import MarkdownRenderer from "@/components/MarkdownRenderer/MarkdownRenderer"; // Импорт компонента для рендеринга Markdown-контента
import Loader from "../Loader/Loader";

interface FAQMobileProps {
  questionsAndAnswers: FAQ[]; // Пропс, содержащий массив вопросов и ответов
}

export default function FAQMobile({ questionsAndAnswers }: FAQMobileProps) {
  const [selected, setSelected] = useState<FAQ | null>(null); // Состояние для хранения выбранного вопроса
  const [imageLoading, setImageLoading] = useState<boolean>(false);

  // Функция выбора или скрытия ответа на вопрос
  const handleSelect = (item: FAQ) => {
    if (item.id === selected?.id) return setSelected(null); // Если клик по уже открытому вопросу, закрываем его
    setSelected(item); // Иначе выбираем новый вопрос
    setImageLoading(true); // При смене вопроса снова показываем лоадер
  };

  return (
    <div className="accordion faq"> {/* Основной контейнер аккордеона FAQ */}
      {questionsAndAnswers.map((item) => (
        <div
          className={`accordion-item ${selected?.id === item.id ? "open" : ""}`} // Если вопрос выбран, добавляем класс "open"
          key={item.id}
        >
          <div className="accordion-item-top" onClick={() => handleSelect(item)}> {/* Заголовок вопроса */}
            <div className="accordion-item__question">
              <MarkdownRenderer content={(item.question)} /> {/* Вопрос с поддержкой Markdown */}
            </div>
            <svg className="carriage-bottom"> {/* Иконка */}
              <use xlinkHref="/static/svg/sprite.svg#icon-carriage"></use>
            </svg>
          </div>
          <div
            className={`accordion-item-bottom ${
              selected?.id === item.id ? "active" : "" // Если выбран, добавляем "active"
            }`}
            style={selected?.id === item.id ? { maxHeight: "100%" } : {}} // Открываем/закрываем блок с ответом
          >
            <div className="accordion-item-content"> {/* Контейнер ответа */}
              <div className="accordion-item-content__wrapper">
                {selected?.image ? (
                  <div className="accordion-item-content__img"> {/* Если есть изображение, показываем его */}
                    {imageLoading && <Loader />}
                    <Image src={selected.image} alt="FAQ Image" width={300} height={120} priority={true} loading="eager" layout="intrinsic" onLoad={() => setImageLoading(false)} onError={() => setImageLoading(false)} style={{ display: imageLoading ? "none" : "block" }} />
                  </div>
                ) : (
                  <div className="localhost-faq__img"> {/* Заглушка, если нет изображения */}
                    <svg>
                      <use xlinkHref="static/svg/sprite.svg#icon-plug"></use>
                    </svg>
                  </div>
                )}
                <div className="accordion-item-content__text"> {/* Контейнер для текста ответа */}
                  <MarkdownRenderer content={item.answer} />
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
