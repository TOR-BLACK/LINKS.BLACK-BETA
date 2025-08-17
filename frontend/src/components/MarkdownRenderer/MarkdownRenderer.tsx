import React from 'react'; // Импорт React
import ReactMarkdown from 'react-markdown'; // Библиотека для рендеринга Markdown
import remarkGfm from 'remark-gfm'; // Плагин для поддержки расширенного синтаксиса GitHub Flavored Markdown
import rehypeRaw from 'rehype-raw'; // Плагин для обработки HTML внутри Markdown
import styles from './markdownrenderer.module.scss'; // Подключение модульных стилей

interface MarkdownRendererProps {
  content: string; // Пропс, содержащий строку с Markdown-контентом
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  return (
    <div className={styles['markdown-content']}> {/* Контейнер для стилизации Markdown-контента */}
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}  // Подключаем поддержку GFM (GitHub Flavored Markdown)
        rehypePlugins={[rehypeRaw]}  // Позволяем обработку HTML внутри Markdown
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer; // Экспортируем компонент