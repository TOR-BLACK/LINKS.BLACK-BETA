"use client"; // Указывает, что компонент должен выполняться на клиенте

import Colorer from "@/services/colorer"; // Импорт компонента для окрашивания иконки
import { useEffect, useState } from "react"; // Импорт хуков React

const ChatButton = () => {
  // Создаем состояние для определения, мобильное ли устройство
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    // Функция, проверяющая текущую ширину экрана
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    handleResize(); // Вызываем сразу при монтировании компонента
    
    // Добавляем обработчик изменения размера окна
    window.addEventListener("resize", handleResize);
    
    // Убираем обработчик при размонтировании компонента
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // Если устройство не мобильное, не рендерим компонент
  if (!isMobile) return null;

  return (
    <a
      href="#" // Ссылка-заглушка, можно заменить на реальную
      className="chat-button" // Класс для стилизации кнопки
    >
      <Colorer
        src="/static/svg/icons/icon-support-1.svg" // Путь к иконке
        colorVar="--white-black16" // Основной цвет
        hoverColorVar="--gold-white" // Цвет при наведении
        pressColorVar="--gold-white" // Цвет при нажатии
        width={30} // Ширина иконки
        height={30} // Высота иконки
      />
    </a>
  );
};

export default ChatButton; // Экспорт компонента для использования в других частях приложения

