import Breadcrumbs from "@/components/Breadcrumbs/Breadcrumbs";
import PartnershipItems from "@/components/Partnership/PartnershipItems";
import api from "@/lib/api";
import { Partnership } from "@/types/dtos";
import { getTranslations } from "next-intl/server";

export const revalidate = 60;

export default async function PartnershipPage() {
  let partnership: Partnership[] = [];

  try {
    const allPartnership = await api<Partnership[]>("/partnerships");

    partnership = allPartnership.sort((a, b) => a.id - b.id);
  } catch (error) {
    console.error(error);
  }

  const t = await getTranslations("PartnershipPage");

  return (
    <div className="localhost-partnership" id="partnership">
      <section>
        <div className="container">
          <Breadcrumbs page={t("breadcrumbs")} />
          <div className="localhost-partnership-heading">
            <div className="localhost-partnership-heading-cell">
              <div className="localhost-partnership-heading-cell__title">
                <span className="color-accent">
                  {t("headingInfo.first.markered")}
                </span>{" "}
                {t("headingInfo.first.beforeBrText")}
                <br />{" "}
                {t("headingInfo.first.afterBrText")}
              </div>
              <svg>
                <use xlinkHref="/static/svg/sprite.svg#icon-calendar"></use>
              </svg>
            </div>
            <div className="localhost-partnership-heading-cell">
              <div className="localhost-partnership-heading-cell__title">
                <span className="color-accent">
                  {t("headingInfo.second.markered")}
                </span>{" "}
                <br />
                {t("headingInfo.second.afterBrText")}
              </div>
              <svg>
                <use xlinkHref="/static/svg/sprite.svg#icon-transactions"></use>
              </svg>
            </div>
            <div className="localhost-partnership-heading-cell">
              <div className="localhost-partnership-heading-cell__title">
                <span className="color-accent">
                  {t("headingInfo.third.markered")}
                </span>
                <br />
                {t("headingInfo.third.afterBrText")}
              </div>
              <svg>
                <use xlinkHref="/static/svg/sprite.svg#delivery"></use>
              </svg>
            </div>
          </div>
          <PartnershipItems partnerships={partnership} />
        </div>
      </section>
    </div>
  );
}
