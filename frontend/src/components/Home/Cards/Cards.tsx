import { MainPageButtonBlock } from "@/types/dtos";
import { useTranslations } from "next-intl";
import Link from "next/link";
import React from "react";
import ColoredImage from "@/services/colorer";

interface CardsProps {
  cards: MainPageButtonBlock[]; // Пропс с массивом карточек
}

export default function Cards({ cards }: CardsProps) {
  const t = useTranslations("HomePage"); // Получение переведенных строк для главной страницы

  return (
    <div className="localhost-main-cards"> {/* Контейнер для всех карточек */}
      <div className="localhost-main-cards__wrapper"> {/* Обертка карточек */}
        {cards.map((card) => (
          <div className="localhost-main-card" key={card.id}> {/* Карточка */}
            <div className="localhost-main-card__info"> {/* Информация в карточке */}
              <div className="localhost-main-card__title">{card.title}</div> {/* Заголовок карточки */}
              <div className="text-m">{card.description}</div> {/* Описание карточки */}
              <Link className="button" href={card.link}> {/* Кнопка с ссылкой */}
                {t("cards.button")}
              </Link>
            </div>
            <div className="localhost-main-card__img"> {/* Блок изображения карточки */}
              {card.background_image && (
                <ColoredImage
                  src={card.background_image}
                  width={200}
                  height={200}
                  colorVar="--specific-svg"
                />
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
} 
