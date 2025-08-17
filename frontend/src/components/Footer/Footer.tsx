"use client"; // Указываем, что компонент работает на клиенте

import { useTranslations } from "next-intl"; // Хук для работы с локализацией
import Link from "next/link"; // Компонент для клиентской навигации без перезагрузки страницы
import Swal from "sweetalert2"; // Импорт библиотеки для создания всплывающих уведомлений

export default function Footer() {
  const t = useTranslations("Footer"); // Получаем переводы для футера

  // Функция для отображения всплывающего окна с информацией о связи с руководством
  const showManagersPopup = () => {
    Swal.fire({
        position: 'center', 
        title: `Вы можете напрямую связаться с руководством Da Vinci через отдел продаж. Если ваши причины для связи будут признаны обоснованными, отдел продаж организует вашу связь с руководством.`,
        showConfirmButton: false,
        timer: 15000, // Всплывающее окно исчезнет через 15 секунд
        timerProgressBar: true, // Показываем индикатор времени
        backdrop: 'rgba(0, 0, 0, 0.4)', // Затемнённый фон за всплывающим окном
        html: `
            <a href="/contacts" class="button">
                Связаться с нами
            </a>
        `,
        customClass: {
            popup: 'popup-managers-toast',
            title: 'popup-managers-title',
            timerProgressBar: 'popup-managers-timer-bar'
        }
    });
  };

  return (
    <footer className="footer"> {/* Основной контейнер футера */}
      <div className="footer__container">
        <div className="footer-content">
          <div className="footer-content__top"> {/* Верхняя часть футера */}
            <Link className="footer__logo" href="/"> {/* Логотип */}
              <svg>
                <use xlinkHref="/static/svg/sprite.svg#logo"></use>
              </svg>
            </Link>
            <div className="footer__info"> {/* Блоки с информацией */}
              <div className="footer-cell"> {/* Блок для покупателей */}
                <h3 className="footer-cell__title">{t("buyersBlock.title")}</h3>
                <ul className="footer-cell__links">
                  <li className="footer-cell__link">
                    <Link href="/wholesale">{t("buyersBlock.wholesale")}</Link>
                  </li>
                  <li className="footer-cell__link">
                    <Link href="/contacts">{t("buyersBlock.contacts")}</Link>
                  </li>
                </ul>
              </div>
              <div className="footer-cell"> {/* Блок партнёрства */}
                <h3 className="footer-cell__title">
                  {t("partnershipBlock.title")}
                </h3>
                <ul className="footer-cell__links">
                  <li className="footer-cell__link">
                    <Link href="/work">{t("partnershipBlock.vacancies")}</Link>
                  </li>
                  <li className="footer-cell__link">
                    <Link href="/partnership">
                      {t("partnershipBlock.partnership")}
                    </Link>
                  </li>
                  <li className="footer-cell__link">
                    <Link href="/contacts">
                      {t("partnershipBlock.contacts")}
                    </Link>
                  </li>
                  <li className="footer-cell__link">
                    <div onClick={showManagersPopup} className="popup-button"> {/* Кнопка для вызова всплывающего окна */}
                      <Link href="">
                        {t("partnershipBlock.managers")}
                      </Link>
                    </div>
                  </li>
                </ul>
              </div>
              <div className="footer-cell"> {/* Блок с информацией */}
                <h3 className="footer-cell__title">
                  {t("informationBlock.title")}
                </h3>
                <ul className="footer-cell__links">
                  <li className="footer-cell__link">
                    <Link href="/policy">
                      {t("informationBlock.rulesAndPolicies")}
                    </Link>
                  </li>
                  <li className="footer-cell__link">
                    <Link href="/faq">{t("informationBlock.faq")}</Link>
                  </li>
                  <li className="footer-cell__link">
                    <Link href="/contacts">
                      {t("partnershipBlock.contacts")}
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div className="footer-content__bottom"> {/* Нижняя часть футера */}
            <div className="text-s">{t("copyright")}</div>
          </div>
        </div>
      </div>
    </footer>
  );
}
