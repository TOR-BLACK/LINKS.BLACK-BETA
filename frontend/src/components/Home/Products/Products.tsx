"use client"; // Указываем, что компонент работает на клиенте

import { useState } from "react"; // Хук для управления состоянием
import ColoredImage from "@/services/colorer"; // Импорт компонента для цветных изображений
import Link from "next/link"; // Компонент Next.js для навигации
import { MainPageReputationLink } from "@/types/dtos"; // Тип данных для карточек продуктов

interface ProductsProps {
  products: MainPageReputationLink[]; // Пропс с массивом продуктов
}

export default function Products({ products }: ProductsProps) {
  const [hoveredCard, setHoveredCard] = useState<number | null>(null); // Состояние для отслеживания наведения
  const [pressedCard, setPressedCard] = useState<number | null>(null); // Состояние для отслеживания нажатия

  // Обработчик наведения на карточку
  const handleMouseEnter = (index: number) => setHoveredCard(index);
  const handleMouseLeave = () => setHoveredCard(null);

  // Обработчик нажатия на карточку
  const handleMouseDown = (index: number) => {
    setPressedCard(index);
  };

  // Обработчик отпускания кнопки мыши
  const handleMouseUp = () => {
    setPressedCard(null);
  };

  // Обработчик выхода курсора с карточки
  const handleMouseLeaveCard = () => {
    setPressedCard(null);
  };

  return (
    <div className="localhost-main-products"> {/* Контейнер всех карточек продуктов */}
      {products.map((product, index) => (
        <Link href={product.link} target="_blank" key={product.id}> {/* Ссылка на продукт */}
          <div
            className="localhost-main-products-card" // Карточка продукта
            onMouseEnter={() => handleMouseEnter(index)}
            onMouseLeave={() => {
              handleMouseLeave();
              handleMouseLeaveCard(); 
            }}
            onMouseDown={() => handleMouseDown(index)} 
            onMouseUp={handleMouseUp} 
            data-index={index}
          >
            {product.image && (
              <div className="localhost-main-products-card__img"> {/* Контейнер изображения */}
                <ColoredImage
                  src={product.image}
                  colorVar="--brown-gold" // Основной цвет
                  hoverColorVar="--dies" // Цвет при наведении
                  pressColorVar="--dies" // Цвет при нажатии
                  width={70}
                  height={70}
                  isHovered={hoveredCard === index} // Передаем состояние наведения
                  isPressed={pressedCard === index} // Передаем состояние нажатия
                />
              </div>
            )}
            <div className="localhost-main-products-card__title"> {/* Название продукта */}
              {product.title}
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
