"use client"; // Указываем, что компонент работает на клиенте

import { useState } from "react"; // Импорт хука useState для управления состоянием

interface InputRangeProps {
  text: string; // Текстовое описание диапазона
  defaultValue: number; // Значение по умолчанию
  min: number; // Минимальное значение диапазона
  max: number; // Максимальное значение диапазона
  step?: number; // Шаг изменения значения (по умолчанию 1)
  onChange: (value: number) => void; // Функция обратного вызова при изменении значения
}

export default function InputRange({
  text,
  defaultValue,
  min,
  max,
  step = 1, // Значение шага по умолчанию
  onChange,
}: InputRangeProps) {
  const [value, setValue] = useState<number>(defaultValue); // Локальное состояние для хранения текущего значения

  // Функция обработки изменений значения диапазона
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = Number(e.target.value); // Преобразуем значение в число
    setValue(newValue); // Обновляем локальное состояние
    onChange(newValue); // Вызываем переданную функцию обратного вызова
  };

  return (
    <div className="die range"> {/* Контейнер для ползунка */}
      <div className="die__wrapper"> {/* Верхняя часть: текст и текущее значение */}
        <div className="die__text">{text}</div> {/* Отображение текстового описания */}
        <div className="value">{value}</div> {/* Отображение текущего значения */}
      </div>
      <div className="die__bottom"> {/* Нижняя часть: сам ползунок */}
        <div className="input-range"> {/* Обертка для ползунка */}
          <input
            className="input-range__slider"
            type="range"
            min={min} // Устанавливаем минимальное значение
            max={max} // Устанавливаем максимальное значение
            step={step} // Устанавливаем шаг изменения
            value={value} // Привязываем текущее значение
            onChange={handleChange} // Обрабатываем изменение значения
            style={{
              background: `linear-gradient(90deg, var(--accent-1) ${
                (value * 100) / max
              }%, var(--gray64-black16) ${(value * 100) / max}%)`, // Настройка градиента
            }}
          />
        </div>
      </div>
    </div>
  );
}
