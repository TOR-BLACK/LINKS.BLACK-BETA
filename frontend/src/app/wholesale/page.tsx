import Breadcrumbs from "@/components/Breadcrumbs/Breadcrumbs";
import WholesaleItems from "@/components/Wholesale/WholesaleItems";
import api from "@/lib/api";
import { Country } from "@/types/dtos";
import { getTranslations } from "next-intl/server";

export default async function Wholesale() {
  let countries: Country[] = [];

  try {
    const allCountries = await api<Country[]>("/opt/countries");

    countries = allCountries.sort((a, b) => a.id - b.id);
  } catch (error) {
    console.error(error);
  }

  const t = await getTranslations("WholesalePage");

  return (
    <div className="localhost-wholesale" id="wholesale">
      <section>
        <div className="container">
          <Breadcrumbs page={t("breadcrumbs")} />
          <div className="localhost-wholesale-heading">
            <div className="localhost-wholesale-heading__info">
              {t("headingInfo")}
            </div>
          </div>

          <WholesaleItems countries={countries} />
        </div>
      </section>
    </div>
  );
}
