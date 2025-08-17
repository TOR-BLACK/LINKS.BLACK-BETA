import { useRef, useEffect, useCallback } from "react";

// Определяем интерфейс пропсов компонента
interface ColorerProps {
  src: string; // Путь к изображению
  colorVar: string; // Основная переменная цвета (CSS-переменная)
  hoverColorVar?: string; // Цвет при наведении
  pressColorVar?: string; // Цвет при нажатии
  width?: number; // Ширина холста
  height?: number; // Высота холста
  isHovered?: boolean; // Флаг наведения
  isPressed?: boolean; // Флаг нажатия
}

// Функциональный компонент `Colorer`
const Colorer = ({
  src, // Путь к изображению
  colorVar, // Основной цвет
  hoverColorVar, // Цвет при наведении
  pressColorVar, // Цвет при нажатии
  width = 1000, // Значение ширины по умолчанию
  height = 1000, // Значение высоты по умолчанию
  isHovered = false, // Значение наведения по умолчанию
  isPressed = false, // Значение нажатия по умолчанию
}: ColorerProps) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null); // Создаём реф для холста

  // Функция для отрисовки изображения с цветовой заливкой
  const drawImageWithColor = useCallback(
    (color: string) => {
      const canvas = canvasRef.current; // Получаем холст
      const ctx = canvas?.getContext("2d"); // Получаем контекст рисования

      if (!canvas || !ctx) return; // Если холст или контекст отсутствует, прекращаем выполнение

      const img = new window.Image(); // Создаем объект изображения
      img.src = src; // Устанавливаем источник изображения

      img.onload = () => {
        canvas.width = width; // Устанавливаем ширину холста
        canvas.height = height; // Устанавливаем высоту холста

        ctx.clearRect(0, 0, canvas.width, canvas.height); // Очищаем холст
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height); // Рисуем изображение

        ctx.globalCompositeOperation = "source-atop"; // Устанавливаем режим наложения
        ctx.fillStyle = color; // Устанавливаем цвет заливки
        ctx.fillRect(0, 0, canvas.width, canvas.height); // Закрашиваем изображение
      };
    },
    [src, width, height] // useCallback зависим от src, width и height
  );

  // useEffect для обновления изображения при изменении переменной цвета
  useEffect(() => {
    const computedStyle = getComputedStyle(document.documentElement); // Получаем стили корневого элемента

    // Функция для обновления цвета в зависимости от состояния
    const updateColor = () => {
      let resolvedColor = computedStyle.getPropertyValue(colorVar).trim(); // Получаем основной цвет

      // Приоритетное изменение цвета при нажатии или наведении
      if (isPressed && pressColorVar) {
        resolvedColor = computedStyle.getPropertyValue(pressColorVar).trim();
      } else if (isHovered && hoverColorVar) {
        resolvedColor = computedStyle.getPropertyValue(hoverColorVar).trim();
      }

      // Если цвет определён, рисуем изображение с ним
      if (resolvedColor) {
        drawImageWithColor(resolvedColor);
      }
    };

    updateColor(); // Вызываем функцию обновления цвета

    // Создаем `MutationObserver` для отслеживания изменений стилей
    const observer = new MutationObserver(() => {
      updateColor(); // Обновляем цвет при изменениях стилей
    });

    observer.observe(document.documentElement, {
      attributes: true, // Отслеживаем изменения атрибутов
      subtree: true, // Отслеживаем все вложенные элементы
      attributeFilter: ["style", "class"], // Ограничиваем отслеживание только стилями и классами
    });

    return () => {
      observer.disconnect(); // Отключаем наблюдатель при размонтировании компонента
    };
  }, [colorVar, hoverColorVar, pressColorVar, drawImageWithColor, isHovered, isPressed]); // useEffect зависим от изменений этих значений

  // Рендерим `canvas`
  return <canvas ref={canvasRef} style={{ display: "block" }} />;
};

export default Colorer; // Экспортируем компонент
