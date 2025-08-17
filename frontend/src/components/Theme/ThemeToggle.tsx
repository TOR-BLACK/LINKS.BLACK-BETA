"use client"; // Указываем, что компонент работает на клиенте

import { useTheme } from "next-themes"; // Хук для работы с темами из next-themes
import { useEffect, useState } from "react"; // Импорт хуков useEffect и useState

export default function ThemeToggle() {
  const [mounted, setMounted] = useState<boolean>(false); // Состояние для отслеживания монтирования компонента
  const { setTheme, resolvedTheme } = useTheme(); // Получаем текущую тему и функцию её изменения

  useEffect(() => setMounted(true), []); // Устанавливаем флаг, когда компонент смонтирован

  // Пока компонент не смонтирован, отображаем заглушку с иконкой тёмной темы
  if (!mounted)
    return (
      <div className="button-circle theme">
        <svg className="button-circle__svg">
          <use xlinkHref="/static/svg/sprite.svg#icon-theme-dark"></use>
        </svg>
      </div>
    );

  // Если текущая тема - "dark", отображаем кнопку для переключения на "light"
  if (resolvedTheme === "dark") {
    return (
      <div className="button-circle theme" onClick={() => setTheme("light")}> {/* Устанавливаем светлую тему при клике */}
        <svg className="button-circle__svg">
          <use xlinkHref="/static/svg/sprite.svg#icon-theme-light"></use>
        </svg>
      </div>
    );
  }

  // Если текущая тема - "light", отображаем кнопку для переключения на "dark"
  if (resolvedTheme === "light") {
    return (  
      <div className="button-circle theme" onClick={() => setTheme("dark")}> {/* Устанавливаем тёмную тему при клике */}
        <svg className="button-circle__svg">
          <use xlinkHref="/static/svg/sprite.svg#icon-theme-dark"></use>
        </svg>
      </div>
    );
  }
}
