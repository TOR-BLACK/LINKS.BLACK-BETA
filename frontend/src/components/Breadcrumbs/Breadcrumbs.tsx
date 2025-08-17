import { useTranslations } from "next-intl"; // Хук для локализации
import Link from "next/link"; // Компонент Next.js для навигации без перезагрузки

export default function Breadcrumbs({
  page,
  subPage,
  subPageHref,
}: {
  page: string; // Название текущей страницы
  subPage?: string; // Название подстраницы (опционально)
  subPageHref?: string; // Ссылка на подстраницу (опционально)
}) {
  const t = useTranslations("Header"); // Получение переведенных строк из пространства имён "Header"
  
  return (
    <div className="breadcrumbs"> {/* Контейнер для хлебных крошек */}
      <ul>
        <li className="main"> {/* Главная страница */}
          <a href="/">{t("headerNav.home")}</a> {/* Ссылка на главную страницу */}
          <svg>
            <use href="static/svg/sprite.svg#icon-breadcrumbs-vector"></use> {/* Иконка-разделитель */}
          </svg>
        </li>
        {subPage && subPageHref && ( // Если переданы подстраница и её ссылка, отображаем
          <li className="between"> {/* Подстраница (если есть) */}
            <Link href={subPageHref}>{subPage}</Link> {/* Ссылка на подстраницу */}
            <svg>
              <use href="static/svg/sprite.svg#icon-breadcrumbs-vector"></use> {/* Иконка-разделитель */}
            </svg>
          </li>
        )}
        <li>{page}</li> {/* Текущая страница без ссылки */}
      </ul>
    </div>
  );
}
