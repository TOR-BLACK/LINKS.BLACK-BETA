"use client";

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import Cards from "@/components/Home/Cards/Cards";
import Products from "@/components/Home/Products/Products";
import Slider from "@/components/Home/Slider/Slider";
import api from "@/lib/api";
import {
  MainPageButtonBlock,
  MainPageReputationLink,
  MainPageSlider,
} from "@/types/dtos";
import Loader from "@/components/Loader/Loader"; 

export default function Home() {
  const locale = useLocale(); 
  const [slider_slides, setSliderSlides] = useState<MainPageSlider[]>([]);
  const [cards, setCards] = useState<MainPageButtonBlock[]>([]);
  const [products, setProducts] = useState<MainPageReputationLink[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const t = useTranslations("HomePage");

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); 

      try {
        const [sliderResponse, cardsResponse, productsResponse] = await Promise.all([
          api<MainPageSlider[]>("/main/slider", { headers: { "Accept-Language": locale } }),
          api<MainPageButtonBlock[]>("/main/button-block/", { headers: { "Accept-Language": locale } }),
          api<MainPageReputationLink[]>("/main/reputation-links/", { headers: { "Accept-Language": locale } }),
        ]);

        setSliderSlides(sliderResponse.sort((a, b) => a.id - b.id));
        setCards(cardsResponse.sort((a, b) => a.id - b.id));
        setProducts(productsResponse.sort((a, b) => a.id - b.id));
      } catch (error) {
        console.error("Ошибка загрузки данных:", error);
      } finally {
        setLoading(false); 
      }
    };

    fetchData(); 
  }, [locale]); 

  if (loading) {
    return (
      <div className="localhost-main" id="main">
        <section>
          <div className="container">
            <Loader /> 
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="localhost-main" id="main">
      <section>
        <div className="container">
          <div className="localhost-main-content">
            <Slider slides={slider_slides} />
            <Cards cards={cards} />
            <div className="localhost-main__info">
              <div className="text-m">
                <span className="color-accent">Da Vinci WebGram Market </span>
                {t("mainInfo")}
              </div>
            </div>
            <Products products={products} />
          </div>
        </div>
      </section>
    </div>
  );
}
