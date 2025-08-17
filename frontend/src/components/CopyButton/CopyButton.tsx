"use client"; // Указываем, что компонент работает на клиенте

import { useEffect, useState } from "react"; // Импортируем хуки React

export default function CopyButton({ text }: { text: string }) {
  const [isClicked, setIsClicked] = useState<boolean>(false); // Флаг, был ли клик по кнопке
  let timeoutId: NodeJS.Timeout | null = null; // Таймер для сброса состояния

  const handleClick = async () => {
    await navigator.clipboard.writeText(text); // Копируем текст в буфер обмена
    setIsClicked(true); // Устанавливаем флаг клика

    timeoutId = setTimeout(() => {
      setIsClicked(false); // Сбрасываем флаг через 2 секунды
    }, 2000);
  };

  useEffect(() => {
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId); // Очищаем таймер при размонтировании компонента
      }
    };
  }, [timeoutId]);

  return (
    <button className="button-copy" onClick={handleClick}> {/* Кнопка копирования */}
      <svg className={isClicked ? "icon-check" : ""}> {/* Меняем иконку при клике */}
        <use
          xlinkHref={`static/svg/sprite.svg#${
            isClicked ? "icon-check" : "icon-copy-2"
          }`} /* Подключаем соответствующую иконку */
        ></use>
      </svg>
    </button>
  );
}