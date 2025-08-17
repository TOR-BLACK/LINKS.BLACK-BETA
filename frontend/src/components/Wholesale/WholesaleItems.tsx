"use client";

import { Country } from "@/types/dtos";
import { useEffect, useState } from "react";
import WholesaleCountry from "./WholesaleCountry";
import { useLocale } from "next-intl";
// import { useTranslations } from "next-intl";

interface WholesaleItemsProps {
  countries: Country[];
}

export default function WholesaleItems({ countries }: WholesaleItemsProps) {
  const [selected, setSelected] = useState<Country | null>(null);

  const locale = useLocale();
  // const t = useTranslations("WholesalePage");
  useEffect(() => {
    if (countries.length > 0) {
      setSelected(countries[0]); // Первая страна выбрана при возврате всех стран удаляем данную функцию 
    }
  }, [countries, locale]);
  return (
    <div className="localhost-wholesale-content">
      <div className="tabs">
        <div className="tabs-tablist" role="tablist" aria-label="Country map">
          {/* Закомментированы кнопки и логика, связанные с выбором стран */}
          {/* <div
            className="tabs-tablist__button"
            role="tab"
            aria-selected={selected === null ? true : false}
            id="allCountries"
            onClick={() => setSelected(null)}
          >
            {t("countries.allCountries")}
          </div> */}

          {/* рендер списка стран */}
          {countries.map((country) => (
            <div
              key={country.id} 
              className="tabs-tablist__button"
              role="tab"
              aria-selected={selected?.id === country.id}
              id={country.code}
              onClick={() => setSelected(country)}
            >
              {country.name}
            </div>
          ))}
        </div>

        {/* Закомментированы все части, касающиеся карты и кнопок */}
        {/* {selected === null ? (
          <div
            className="tabs__content"
            role="tabpanel"
            aria-labelledby="allCountries"
          >
            <div className="localhost-wholesale-block main">
              <div className="localhost-wholesale-block__center">
                <div className="localhost-wholesale-block__map">
                  <Image
                    src="/static/svg/map-world.svg"
                    alt="Img: map-world"
                    width={436}
                    height={270}
                  />
                </div>
              </div>
            </div>
            <div className="localhost-wholesale__buttons">
              <button className="button-functional" name="download">
                <svg>
                  <use xlinkHref="static/svg/sprite.svg#icon-download"></use>
                </svg>
                {t("links.excel")}
              </button>
              <button className="button-functional" name="copy">
                <svg>
                  <use xlinkHref="static/svg/sprite.svg#icon-copy-1"></use>
                </svg>
                {t("links.copy")}
              </button>
            </div>
          </div>
        ) : ( */}
        
        {/* WholesaleCountry когда подключим оставляем только <WholesaleCountry country={selected} />*/}
        {selected && <WholesaleCountry country={selected} />}
      </div>
    </div>
  );
}
