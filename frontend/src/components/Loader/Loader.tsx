"use client"; // Указываем, что компонент работает на клиенте

import React from 'react'; // Импорт React
import './Loader.scss'; // Подключение стилей для загрузчика

interface LoaderProps {
  size?: number; // Размер загрузчика (по умолчанию 50px)
  height?: number; // Высота контейнера загрузчика в vh (по умолчанию 50vh)
}

const Loader: React.FC<LoaderProps> = ({
  size = 50, // Устанавливаем размер по умолчанию
  height = 50 // Устанавливаем высоту контейнера по умолчанию
}) => {
  return (
    <div 
      className="loader-container" 
      role="status" // Указываем, что это статусный элемент
      aria-live="polite" // Делаем доступным для экранных дикторов
      style={{ '--loader-height': `${height}vh` } as React.CSSProperties} // Динамическая установка высоты контейнера
    >
      <div
        className="loader" // Основной элемент загрузчика
        style={{
          '--loader-size': `${size}px`, // Устанавливаем размер
          '--loader-border-width': `${size / 6}px`, // Устанавливаем ширину границы (1/6 от размера)
        } as React.CSSProperties} // Приведение типов для CSS-переменных
      >
      </div>
    </div>
  );
};

export default Loader; // Экспортируем компонент Loader
