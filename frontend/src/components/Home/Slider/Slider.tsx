"use client"; // Указываем, что компонент работает на клиенте

import React, { useEffect, useRef } from "react"; // Импорт React и хуков
import { Swiper, SwiperRef, SwiperSlide } from "swiper/react"; // Импорт Swiper и его компонентов

import "swiper/css"; // Подключение базовых стилей Swiper
import "swiper/css/effect-fade"; // Стили для эффекта Fade
import "swiper/css/navigation"; // Стили для навигации
import "swiper/css/pagination"; // Стили для пагинации

import { EffectFade, Navigation, Pagination } from "swiper/modules"; // Импорт модулей Swiper
import { MainPageSlider } from "@/types/dtos"; // Импорт типов данных
import Image from "next/image"; // Компонент Next.js для изображений
import ColoredImage from "@/services/colorer"; // Компонент для окрашивания изображений

interface SliderProps {
  slides: MainPageSlider[]; // Пропс, содержащий массив слайдов
}

export default function Slider({ slides }: SliderProps) {
  const swiperRef = useRef<SwiperRef | null>(null); // Ссылка на Swiper

  // Функция для корректировки ширины навигации слайдера
  const adjustNavigationWidth = () => {
    const rightSlide = document.querySelector(
      ".swiper-slide__right"
    ) as HTMLElement;
    const navigation = document.querySelector(
      ".swiper__navigation"
    ) as HTMLElement;

    if (rightSlide && navigation) {
      const rightSlideWidth = rightSlide.offsetWidth;
      const navigationWidth = rightSlideWidth - 70;
      navigation.style.width = `${navigationWidth}px`;
    }
  };

  useEffect(() => {
    adjustNavigationWidth(); // Вызываем функцию при монтировании
    window.addEventListener("resize", adjustNavigationWidth); // Добавляем обработчик ресайза
    return () => window.removeEventListener("resize", adjustNavigationWidth); // Удаляем обработчик при размонтировании
  }, []);

  return (
    <div className="localhost-main-slider"> {/* Контейнер для слайдера */}
      <Swiper
        ref={swiperRef}
        className="swiper-main"
        effect={"fade"} // Добавляем эффект затухания
        pagination={{ // Настройки пагинации
          el: ".swiper-pagination",
          dynamicBullets: true,
          dynamicMainBullets: 1,
          clickable: true,
        }}
        navigation={{ // Настройки навигации (кнопки вперед/назад)
          nextEl: ".swiper__btn--next",
          prevEl: ".swiper__btn--prev",
        }}
        modules={[EffectFade, Navigation, Pagination]} // Подключаем модули Swiper
      >
        {slides.map((slide) => (
          <SwiperSlide key={slide.id}> {/* Один слайд */}
            <div className="swiper-slide__left"> {/* Левая часть с изображением */}
              {slide.image ? ( 
                <div className="swiper-slide__img">
                  <Image
                    src={slide.image as string}
                    alt="Slider Image"
                    width={240}
                    height={280}
                  />
                </div>
              ) : null}
            </div>
            <div className="swiper-slide__right"> {/* Правая часть с контентом */}
              <div className="swiper-slide__content">
                <div className="swiper-slide__background"> {/* Фоновое изображение */}
                  <ColoredImage
                    src="static/svg/map-world-gray.svg"
                    width={423.59}
                    height={213.11}
                    colorVar="--dies"
                  />
                </div>
                <h2 className="swiper-slide__title">{slide.title}</h2> {/* Заголовок слайда */}
                <div className="swiper-slide__info">
                  <p className="text-m">{slide.description}</p> {/* Описание слайда */}
                </div>
              </div>
            </div>
          </SwiperSlide>
        ))}
        <div className="swiper__navigation"> {/* Контейнер навигации */}
          <div className="swiper__btn swiper__btn--prev"> {/* Кнопка "назад" */}
            <svg>
              <use xlinkHref="/static/svg/sprite.svg#icon-carriage"></use>
            </svg>
          </div>
          <div className="swiper__btn swiper__btn--next"> {/* Кнопка "вперед" */}
            <svg>
              <use xlinkHref="/static/svg/sprite.svg#icon-carriage-right"></use>
            </svg>
          </div>
          <div className="swiper-pagination"></div> {/* Пагинация */}
        </div>
      </Swiper>
    </div>
  );
}
