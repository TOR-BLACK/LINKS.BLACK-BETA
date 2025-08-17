"use client"; // Указываем, что компонент работает на клиенте

import { useState } from "react"; // Импорт useState для управления состоянием
import ReactMarkdown from "react-markdown"; // Библиотека для рендеринга Markdown
import remarkGfm from "remark-gfm"; // Подключение плагина для поддержки GitHub Flavored Markdown
import styles from "./markdownrenderer.module.scss"; // Подключение модульных стилей
import { useTranslations } from "next-intl"; // Импорт хука для работы с локализацией

interface Props {
  content: string; // Пропс, содержащий строку с Markdown-контентом
}

// Компонент для копирования ссылки в буфер обмена
const CopyableLink: React.FC<{ text: string; link: string }> = ({ text, link }) => {
  const [copied, setCopied] = useState(false); // Состояние для отображения статуса копирования
  const [displayText, setDisplayText] = useState(text); // Состояние для отображаемого текста
  const t = useTranslations("MirrorPage"); // Получение перевода

  // Функция копирования текста в буфер обмена
  const copyToClipboard = () => {
    navigator.clipboard.writeText(link)
      .then(() => {
        setCopied(true);
        setDisplayText(`✔ ${t("copied")}`); // Показываем статус "Скопировано"
        setTimeout(() => {
          setCopied(false);
          setDisplayText(text);
        }, 2000); // Через 2 секунды возвращаем исходный текст
      })
      .catch((err) => console.error("Ошибка копирования: ", err)); // Логируем ошибку в консоль
  };

  return (
    <span
      onClick={copyToClipboard} // Клик для копирования
      className={copied ? styles.copied : styles.link} // Добавляем класс в зависимости от состояния
    >
      {displayText}
    </span>
  );
};

// Компонент обработки Markdown с возможностью копирования ссылок
const ProcessedMarkdown: React.FC<Props> = ({ content }) => {
  const renderContent = content.split(/\[([^\]]+)\]\(copy-link:([^\)]+)\)/g); // Разбиваем контент по кастомному синтаксису [text](copy-link:link)

  return (
    <div className={styles.markdownContainer}> {/* Контейнер для стилизованного Markdown */}
      {renderContent.map((part, index) =>
        index % 3 === 0 ? ( // Обычный Markdown-контент
          <ReactMarkdown remarkPlugins={[remarkGfm]} key={index}>
            {part}
          </ReactMarkdown>
        ) : index % 3 === 1 ? ( // Обработанный кастомный элемент с возможностью копирования
          <CopyableLink key={index} text={part} link={renderContent[index + 1]} />
        ) : null // Пропускаем ссылки, так как они уже обработаны
      )}
    </div>
  );
};

export default ProcessedMarkdown; // Экспортируем компонент
