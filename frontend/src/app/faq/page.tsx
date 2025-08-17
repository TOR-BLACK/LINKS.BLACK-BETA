"use client"; // Указываем, что этот компонент должен выполняться на клиенте (Next.js)

import { useState, useEffect } from "react";
import api from "@/lib/api"; // Импорт функции API-запроса
import Loader from "@/components/Loader/Loader"; // Компонент загрузки
import { DVInstruction, FAQ } from "@/types/dtos"; // Импорт интерфейсов данных
import Breadcrumbs from "@/components/Breadcrumbs/Breadcrumbs"; // Навигационные "хлебные крошки"
import FAQDesktop from "@/components/FAQ/FAQDesktop"; // Компонент FAQ для десктопа
import FAQMobile from "@/components/FAQ/FAQMobile"; // Компонент FAQ для мобильных устройств
import DVInstructions from "@/components/FAQ/DVInstructions"; // Компонент с инструкциями
import { useLocale, useTranslations } from "next-intl"; // Локализация

// Главный компонент страницы FAQ
export default function FAQPage() {
  // Хранение вопросов и ответов
  const [questionsAndAnswers, setQuestionsAndAnswers] = useState<FAQ[]>([]);
  // Хранение инструкций
  const [instructions, setInstructions] = useState<DVInstruction[]>([]);
  // Флаг загрузки
  const [loading, setLoading] = useState<boolean>(true);
  const t = useTranslations("FaqPage"); // Функция перевода
  const locale = useLocale(); // Определение текущей локали

  // useEffect для загрузки данных при изменении локали
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); // Включаем индикатор загрузки
      try {
        // Запрашиваем FAQ и инструкции с сервера
        const allQuestionsAndAnswers = await api<FAQ[]>("/faq");
        const allInstructions = await api<DVInstruction[]>("/dv-instructions");

        // Сортируем полученные данные перед сохранением в состояние
        setQuestionsAndAnswers(
          allQuestionsAndAnswers.sort((a, b) => a.position - b.position) // Сортируем вопросы по позиции
        );
        setInstructions(allInstructions.sort((a, b) => a.id - b.id)); // Сортируем инструкции по ID
      } catch (error) {
        console.error(error); // Логируем ошибку, если запрос не удался
      } finally {
        setLoading(false); // Выключаем индикатор загрузки
      }
    };

    fetchData(); // Вызываем функцию загрузки данных
  }, [locale]); // Зависимость от локали (повторный запрос при смене языка)

  // Если данные еще загружаются, показываем Loader
  if (loading) {
    return <Loader />;
  }

  return (
    <div className="localhost-faq" id="faq">
      <section>
        <div className="container">
          {/* Навигационные "хлебные крошки" */}
          <Breadcrumbs page={t("breadcrumbs")} />

          {/* Заголовок страницы */}
          <div className="localhost-faq-heading">
            <h1 className="h1">{t("heading")}</h1>
          </div>

          {/* Основное содержимое страницы FAQ */}
          <div className="localhost-faq-content">
            {/* FAQ для десктопных устройств */}
            <FAQDesktop questionsAndAnswers={questionsAndAnswers} />
            {/* FAQ для мобильных устройств */}
            <FAQMobile questionsAndAnswers={questionsAndAnswers} />
            {/* Дополнительная информация */}
            <div className="localhost-faq__info">{t("info")}</div>
            {/* Раздел с инструкциями */}
            <DVInstructions instructions={instructions} />
          </div>
        </div>
      </section>
    </div>
  );
}
