"use client";

import { useState, useEffect } from "react";
import Breadcrumbs from "@/components/Breadcrumbs/Breadcrumbs";
import InputRange from "@/components/InputRange/InputRange";
import { useLocale, useTranslations } from "next-intl";
import Loader from "@/components/Loader/Loader";

// Определение интерфейсов для работы с API
interface Field {
  id: number; // Уникальный идентификатор поля
  field_type: string; // Тип поля (например, input_range, single_choice)
  label: string; // Название поля
  name: string; // Уникальное имя для идентификации
  default_value: string | number; // Значение по умолчанию
  min_value?: string | number; // Минимальное значение (если применимо)
  max_value?: string | number; // Максимальное значение (если применимо)
  step?: string | number; // Шаг для input_range (если применимо)
  choices?: { id: number; label: string; value: string | number }[]; // Варианты выбора (если applicable)
}

interface CalculatorResponse {
  formula: string; // Формула для расчета
  fields: Field[]; // Список полей формы
}

// Главный компонент страницы калькулятор
export default function CalculatorPage() {
  const t = useTranslations("CalculatorPage"); // Используем локализацию
  const locale = useLocale(); // Определяем текущий язык

  // Хранение состояний
  const [fields, setFields] = useState<Field[]>([]); // Список полей
  const [formula, setFormula] = useState<string>(""); // Формула расчета
  const [formValues, setFormValues] = useState<{ [key: string]: number }>({}); // Храним введенные значения
  const [totalSum, setTotalSum] = useState<number>(0); // Итоговая сумма
  const [loading, setLoading] = useState<boolean>(true); // Флаг загрузки данных
  
  // Запрос данных при загрузке страницы
  useEffect(() => {
    async function fetchCalculatorData() {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/calculators/9/`, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "5yef0eFrQ8eVda5fZuJexjJFHFWoPFvgjmn4xbk7UmpAum79xxn44If35g74mHOS",
            "Accept-Language": locale, // Отправляем текущий язык пользователя
          },
        });

        // Преобразуем ответ в JSON
        const data: CalculatorResponse = await response.json();

        // Исправляем возможные ошибки в названиях переменных формулы
        const correctedFormula = data.formula.replace(/delivery_count_per_mounth/g, "delivery_count_per_month");
        
        console.log(data.fields); // Логируем полученные поля

        setFields(data.fields || []); // Устанавливаем поля формы
        setFormula(correctedFormula); // Устанавливаем исправленную формулу
        initializeFormValues(data.fields || []); // Инициализируем значения формы
      } catch (error) {
        console.error("Error fetching calculator data:", error); // Логируем ошибку
      } finally {
        setLoading(false); // Выключаем состояние загрузки
      }
    }

    fetchCalculatorData();
  }, [locale]); // Перезапрос при изменении языка

  // Инициализация значений формы
  const initializeFormValues = (fields: Field[]) => {
    const initialValues: { [key: string]: number } = {};
    fields.forEach((field) => {
      if (field.name) {
        initialValues[field.name] = Number(field.default_value) || 0; // Приводим к числу
      }
    });
    setFormValues(initialValues);
  };

  // Обработчик изменения значений в форме
  const handleInputChange = (name: keyof typeof formValues, value: number) => {
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));
  };

  // Функция расчета общей суммы на основе формулы
  const calculateTotal = () => {
    if (formula) {
      try {
        console.log("Current formula:", formula);
        console.log("Form values:", formValues);

        // Заменяем переменные формулы значениями из формы
        const calculatedResult = eval(
          formula.replace(/[a-zA-Z_]+/g, (match) => {
            const value = formValues[match] ?? 0; // Подставляем значение переменной
            console.log(`Replacing ${match} with ${value}`);
            return String(value);
          })
        );

        setTotalSum(isNaN(calculatedResult) ? 0 : calculatedResult); // Обновляем сумму
        console.log("Calculated Result:", calculatedResult);
      } catch (error) {
        console.error("Error calculating formula:", error);
        setTotalSum(0); // Если ошибка - обнуляем результат
      }
    }
  };

  return (
    <div className="localhost-calculator">
      <section>
        <div className="container">
          {/* Навигационные "хлебные крошки" */}
          <Breadcrumbs page={t("breadcrumbs.second")} subPage={t("breadcrumbs.first")} subPageHref="/work" />
          <div className="localhost-calculator-content">
            {loading ? (
              <Loader /> // Показываем загрузчик, если данные еще загружаются
            ) : (
              <form className="localhost-calculator-form" onSubmit={(e) => { e.preventDefault(); calculateTotal(); }}>
                <div className="localhost-calculator-form-top">
                  {/* Отрисовка полей формы */}
                  {fields.map((field) => {
                    if (field.field_type === "input_range") {
                      return (
                        <InputRange
                          key={field.id}
                          text={field.label}
                          defaultValue={formValues[field.name]}
                          min={Number(field.min_value) || 0}
                          max={Number(field.max_value) || 100}
                          step={Number(field.step) || 1}
                          onChange={(value) => handleInputChange(field.name, value)}
                        />
                      );
                    } else if (field.field_type === "single_choice") {
                      return (
                        <div className="die radio" key={field.id}>
                          <div className="die__text">{field.label}</div>
                          <div className="radio column">
                            {field.choices?.map((choice) => (
                              <label className="radio__wrapper" key={choice.id}>
                                <input
                                  type="radio"
                                  name={field.name}
                                  value={choice.value}
                                  checked={formValues[field.name] === Number(choice.value)}
                                  onChange={() => handleInputChange(field.name, Number(choice.value))}
                                />
                                <span className="radio__checkmark"></span>
                                <span>{choice.label}</span>
                              </label>
                            ))}
                          </div>
                        </div>
                      );
                    }
                    return null;
                  })}
                </div>

                {/* Отображение итоговой суммы и кнопки расчета */}
                <div className="localhost-calculator-form-bottom">
                  <div className="die column">
                    <div className="die__wrapper">
                      <div className="die__text">{t("form.amountSum")}</div>
                      <div className="die__text">{totalSum} {t("form.currency")}</div>
                    </div>
                    <button type="submit" className="button">
                      {t("form.button")}
                    </button>
                  </div>
                </div>
              </form>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
