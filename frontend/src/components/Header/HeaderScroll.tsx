"use client"; // Указываем, что компонент работает на клиенте

import { useEffect, useState } from "react"; // Импорт хуков React
import HeaderContent from "./HeaderContent"; // Импорт компонента с содержимым заголовка

export default function HeaderScroll() {
  const [isScrolled, setIsScrolled] = useState(false); // Состояние, отслеживающее, прокручен ли экран

  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY; // Получаем текущую позицию прокрутки
      if (scrollPosition > 150) {
        setIsScrolled(true); // Если прокрутка больше 150px, устанавливаем состояние
      } else {
        setIsScrolled(false); // Иначе сбрасываем состояние
      }
    };

    window.addEventListener("scroll", handleScroll); // Добавляем слушатель события прокрутки
    return () => {
      window.removeEventListener("scroll", handleScroll); // Удаляем слушатель при размонтировании
    };
  }, []);

  return (
    <header className={`header header-scroll ${isScrolled ? "show" : ""}`}> {/* Добавляем класс при прокрутке */}
      <HeaderContent /> {/* Вставляем содержимое заголовка */}
    </header>
  );
}
