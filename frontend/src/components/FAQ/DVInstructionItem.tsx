"use client"; // Указываем, что компонент работает на клиенте

import { DVInstruction } from "@/types/dtos"; // Импорт типов
import { useState, useEffect } from "react"; // Импорт хуков React
import Image from "next/image"; // Импорт компонента для работы с изображениями
import MarkdownRenderer from "@/components/MarkdownRenderer/MarkdownRenderer"; // Импорт компонента для рендеринга Markdown

interface DVInstructionItemProps {
  instruction: DVInstruction; // Пропс, содержащий инструкцию
}

export default function DVInstructionItem({
  instruction,
}: DVInstructionItemProps) {
  const [isOpen, setIsOpen] = useState<boolean>(false); // Состояние открытия элемента
  const [imageSizes, setImageSizes] = useState<{ [key: string]: { width: number; height: number } }>({}); // Храним размеры изображений

  // Функция загрузки размеров изображений
  const loadImageSize = (src: string) => {
    return new Promise<{ width: number; height: number }>((resolve) => {
      const img = new window.Image();
      img.src = src;
      img.onload = () => {
        resolve({ width: img.width, height: img.height });
      };
    });
  };

  useEffect(() => {
    const loadSizes = async () => {
      const sizes: { [key: string]: { width: number; height: number } } = {};
      for (const row of instruction.rows) {
        // Загружаем размеры изображений, если они еще не загружены
        if (row.column1_image && !sizes[row.column1_image]) {
          sizes[row.column1_image] = await loadImageSize(row.column1_image);
        }
        if (row.column2_image && !sizes[row.column2_image]) {
          sizes[row.column2_image] = await loadImageSize(row.column2_image);
        }
        if (row.column3_image && !sizes[row.column3_image]) {
          sizes[row.column3_image] = await loadImageSize(row.column3_image);
        }
      }
      setImageSizes(sizes);
    };
    loadSizes();
  }, [instruction.rows]);

  // Проверяем, есть ли контент в строках инструкции
  const hasRowsContent = instruction.rows.some(
    (row) =>
      row.column1_text ||
      row.column1_image ||
      row.column2_text ||
      row.column2_image ||
      row.column3_text ||
      row.column3_image
  );

  return (
    <div className={`accordion-item ${isOpen ? "open" : ""}`}> {/* Аккордеон */}
      <div className="accordion-item-top" onClick={() => setIsOpen(true)}> {/* Заголовок */}
        <div className="accordion-item__question"> {/* Вопрос */}
          <MarkdownRenderer content={instruction.title} />
          <svg>
            <use
              xlinkHref={`static/svg/sprite.svg#${
                isOpen ? "icon-question-open" : "icon-question"
              }`}
            ></use>
          </svg>
        </div>
        <svg className="carriage-bottom">
          <use xlinkHref="/static/svg/sprite.svg#icon-carriage"></use>
        </svg>
      </div>
      <div
        className={`accordion-item-bottom ${isOpen ? "active" : ""}`}
        style={isOpen ? { maxHeight: "100%" } : {}}
      >
        {isOpen && hasRowsContent && (
          <div className="accordion-item-row"> {/* Контейнер строк инструкции */}
            {instruction.rows
            .slice() 
            .sort((a, b) => a.id - b.id) 
            .map(
              (row) =>
                (row.column1_text ||
                  row.column1_image ||
                  row.column2_text ||
                  row.column2_image ||
                  row.column3_text ||
                  row.column3_image) && (
                  <div key={row.id} className="accordion-item-rows">
                    {row.column1_text && (
                      <div className="accordion-item-rows__text">
                        <MarkdownRenderer content={row.column1_text} />
                      </div>
                    )}
                    {row.column1_image && (
                      <div className="accordion-item-rows__img">
                        {imageSizes[row.column1_image] && (
                          <Image
                            src={row.column1_image}
                            alt={`Row ${row.id} Column 1`}
                            width={imageSizes[row.column1_image].width}
                            height={imageSizes[row.column1_image].height}
                          />
                        )}
                      </div>
                    )}
                    {row.column2_text && (
                      <div className="accordion-item-rows__text">
                        <MarkdownRenderer content={row.column2_text} />
                      </div>
                    )}
                    {row.column2_image && (
                      <div className="accordion-item-rows__img">
                        {imageSizes[row.column2_image] && (
                          <Image
                            src={row.column2_image}
                            alt={`Row ${row.id} Column 2`}
                            width={imageSizes[row.column2_image].width}
                            height={imageSizes[row.column2_image].height}
                          />
                        )}
                      </div>
                    )}
                    {row.column3_text && (
                      <div className="accordion-item-rows__text">
                        <MarkdownRenderer content={row.column3_text} />
                      </div>
                    )}
                    {row.column3_image && (
                      <div className="accordion-item-rows__img">
                        {imageSizes[row.column3_image] && (
                          <Image
                            src={row.column3_image}
                            alt={`Row ${row.id} Column 3`}
                            width={imageSizes[row.column3_image].width}
                            height={imageSizes[row.column3_image].height}
                          />
                        )}
                      </div>
                    )}
                  </div>
                )
            )}
          </div>
        )}
        <div className="button-open" onClick={() => setIsOpen(false)}> {/* Кнопка закрытия */}
          <svg className="carriage-top">
            <use xlinkHref="static/svg/sprite.svg#icon-carriage"></use>
          </svg>
        </div>
      </div>
    </div>
  );
}
