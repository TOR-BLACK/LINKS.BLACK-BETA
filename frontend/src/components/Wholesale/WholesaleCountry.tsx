"use client";

import { useState, useEffect, ChangeEvent, useCallback, useRef } from "react";
import { useTranslations, useLocale } from "next-intl";
import MarkdownRenderer from "../MarkdownRenderer/MarkdownRenderer";
import { City, Country, ProductList, ProductItem } from "@/types/dtos";
import Image from "next/image";
import Loader from "../Loader/Loader";
import Custom404 from "@/app/not-found";
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
import Swal from "sweetalert2";

interface WholesaleCountryProps {
  country: Country;
}

export default function WholesaleCountry({ country }: WholesaleCountryProps) {
  // Состояния для управления данными о продуктах, городах и фильтрацией
  const [filteredCities, setFilteredCities] = useState<City[]>([]);
  const [fullCityList, setFullCityList] = useState<City[]>([]);   
  const [selectedItems, setSelectedItems] = useState<number[]>([]);
  const [allProducts, setAllProducts] = useState<ProductList[]>([]);
  const [filteredProducts, setFilteredProducts] = useState<ProductList[]>([]);
  const [productType, setProductType] = useState<string>("in_stock");
  const [priceStates, setPriceStates] = useState<{ [key: number]: boolean }>({});
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const [lastUpdate, setLastUpdate] = useState<string>('');

  const t = useTranslations("WholesalePage");
  const locale = useLocale();

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement | null>(null);

  // Функция для переключения меню
  const toggleDropdown = () => {
    setIsDropdownOpen((prev) => !prev);
  };

  // Закрытие меню при клике вне его
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);
  
  // Получение списка продуктов из API
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true); 

        const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
        if (!baseUrl) throw new Error("API base URL not defined");

        const response = await fetch(`${baseUrl}/opt/products?country=${country.id}`, {
          headers: { "Accept-Language": locale },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch products: ${response.statusText}`);
        }

        const data: { results: ProductList[] } = await response.json();
        setAllProducts(data.results || []);
        const initialPriceStates = data.results.reduce((acc, product) => {
          acc[product.id] = true;
          return acc;
        }, {} as { [key: number]: boolean });
        setPriceStates(initialPriceStates);
      } catch (error) {
        console.error("Error fetching products:", error);
        setError(error instanceof Error ? error.message : "Unknown error occurred");
      } finally {
        setLoading(false); 
      }
    };

    fetchProducts();
  }, [country.id, locale]);
  
  // Формирование списка городов на основе доступных товаров
  useEffect(() => {
    const cities = new Map<number, City>();
    allProducts.forEach((product) => {
      product.items?.forEach((aggregate) => {
        if (aggregate.city) {
          cities.set(aggregate.city.id, aggregate.city);
        }
      });
    });

    const uniqueCities = Array.from(cities.values());
    setFullCityList(uniqueCities);
    setFilteredCities(uniqueCities);
    setSelectedItems(uniqueCities.map((city) => city.id));
  }, [allProducts]);

  // Фильтрация продуктов по городу и статусу наличия
  useEffect(() => {
    const filtered = allProducts.filter(
      (product) =>
        product.items?.some((aggregate) =>
          aggregate.items?.some(
            (item) =>
              selectedItems.includes(aggregate.city.id) &&
              item.availability_status === productType
          )
        )
    );
    setFilteredProducts(filtered);
  }, [allProducts, productType, selectedItems]);

  // Форматирование даты последнего обновления товаров
  useEffect(() => {
    const findLatestUpdatedAt = (): Date | null => {
      let latestDate: Date | null = null;
  
      filteredProducts.forEach(product => {
        product.items?.forEach(aggregate => {
          aggregate.items?.forEach(item => {
            if (
              selectedItems.includes(aggregate.city.id) &&
              item.availability_status === productType
            ) {
              const itemDate = new Date(item.updated_at);
              if (!latestDate || itemDate > latestDate) {
                latestDate = itemDate;
              }
            }
          });
        });
      });
  
      return latestDate;
    };
  
    // Форматирование даты последнего обновления товаров
    const latestDate = findLatestUpdatedAt();
  
    if (latestDate) {
      const formatDate = (date: Date): string => {
        const day = date.getDate().toString().padStart(2, "0");
        const month = (date.getMonth() + 1).toString().padStart(2, "0"); 
        const year = date.getFullYear();
        const hours = date.getHours().toString().padStart(2, "0");
        const minutes = date.getMinutes().toString().padStart(2, "0");
  
        return `${day}.${month}.${year} ${t("year")} ${hours}:${minutes}`;
      };
  
      setLastUpdate(formatDate(latestDate));
    } else {
      setLastUpdate("");
    }
  }, [filteredProducts, selectedItems, productType, t]);
  
  // Функция для поиска городов
  const handleSearchChange = (event: ChangeEvent<HTMLInputElement>) => {
    const searchValue = event.target.value.toLowerCase();
    if (!searchValue) {
      setFilteredCities(fullCityList);
    } else {
      setFilteredCities(
        fullCityList.filter((city) => city.name?.toLowerCase().includes(searchValue))
      );
    }
  };

  const handleCheckboxChange = (event: ChangeEvent<HTMLInputElement>) => {
    const cityId = parseInt(event.target.value, 10);

    setSelectedItems((prev) => {
      if (filteredCities.length === 1) {
        return prev.includes(cityId) ? [] : [cityId];
      }

      if (prev.length === filteredCities.length) {
        return [cityId];
      }

      if (prev.includes(cityId)) {
        return prev.filter((id) => id !== cityId);
      } else {
        return [...prev, cityId];
      }
    });
  };

  const handleCheckboxChangeAll = useCallback(
    (event: ChangeEvent<HTMLInputElement>) => {
      setSelectedItems(event.target.checked ? filteredCities.map((city) => city.id) : []);
    },
    [filteredCities]
  );

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return <Custom404 />;
  }

  const renderItems = (aggregate: { items?: ProductItem[] }) => {
    const itemsForSelectedType = aggregate.items?.filter(
      (item) => item.availability_status === productType
    );

    if (itemsForSelectedType && itemsForSelectedType.length > 0) {
      return itemsForSelectedType.map((item) => (
        <li key={item.id} className="localhost-wholesale-block__product-item__list-item">
          {item.count} {t("weight")}. - {Intl.NumberFormat(locale).format(item.price)} ₽
        </li>
      ));
    } else {
      return <p>{t("items.notFound")}</p>;
    }
  };

  const togglePrice = (productId: number) => {
    setPriceStates((prev) => ({
      ...prev,
      [productId]: !prev[productId],
    }));
  };

  const handleDownload = () => {
    const selectedProducts = filteredProducts.flatMap(product => {
      if (!product.items) return [];
  
      return product.items.flatMap(aggregate => {
        if (!aggregate.items) return [];
  
        return aggregate.items
          .filter(item => selectedItems.includes(aggregate.city.id) && item.availability_status === productType)
          .map(item => ({
            "Название продукта": product.title,
            "Описание продукта": product.description || "",
            "Город": aggregate.city.name,
            "Количество": item.count,
            "Цена (₽)": item.price,
            "Статус": item.availability_status === "in_stock" ? "В наличии" : "Предзаказ",
          }));
      });
    });
  
    if (selectedProducts.length === 0) {
      Swal.fire({
        toast: true,
        position: 'bottom',
        icon: 'error',
        iconColor: 'var(--accent-1)',
        title: `${t("items.notFound")}`,
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        customClass: {
          popup: 'popup-error-toast',
          icon: 'popup-error-icon',
          title: 'popup-error-title',
          timerProgressBar: 'popup-error-timer-bar',
        },
      });
      return;
    }
    const [dateOnly] = lastUpdate.split(" ");
    const groupedData = filteredProducts.map(product => {
      const rows = product.items?.flatMap(aggregate => {
        if (!aggregate.items) return [];
        return aggregate.items
          .filter(item => selectedItems.includes(aggregate.city.id) && item.availability_status === productType)
          .map(item => ({
            "Город": aggregate.city.name,
            "Количество": item.count,
            "Цена (₽)": item.price,
            "Статус": item.availability_status === "in_stock" ? "В наличии" : "Предзаказ",
            "Дата обновления": dateOnly,
          }));
      });
  
      if (!rows || rows.length === 0) return null;
  
      return {
        "Название продукта": product.title,
        "Описание продукта": product.description || "",
        rows,
      };
    }).filter((productGroup): productGroup is Exclude<typeof productGroup, null> => productGroup !== null);
  
    const excelData = groupedData.flatMap(productGroup => {
      const headerRow = {
        "Название продукта": productGroup["Название продукта"],
        "Описание продукта": productGroup["Описание продукта"],
        "Город": "",
        "Количество": "",
        "Цена (₽)": "",
        "Статус": "",
        "Дата обновления": "",
      };
  
      const cityRows = productGroup.rows.map(row => ({
        "Название продукта": "",
        "Описание продукта": "",
        ...row,
      }));
  
      return [headerRow, ...cityRows];
    });
  
    const worksheet = XLSX.utils.json_to_sheet(excelData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Продукты");
  
    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
  
    saveAs(blob, `products_${country.name}_${new Date().toISOString()}.xlsx`);
    Swal.fire({
      toast: true,
      position: 'bottom',
      iconHtml: `<svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: transparent; display: block;" width="24" height="24" viewBox="0 0 50 50">
            <circle
              cx="25"
              cy="25"
              r="20"
              stroke="var(--accent-1)"
              stroke-width="4"
              fill="none"
              stroke-dasharray="31.415, 31.415"
              stroke-linecap="round"
              transform="rotate(122.79 25 25)">
              <animateTransform
                attributeName="transform"
                type="rotate"
                repeatCount="indefinite"
                dur="0.75s"
                values="0 25 25;360 25 25"
                keyTimes="0;1"/>
            </circle>
          </svg>`,
      iconColor: 'var(--accent-1)',
      title: `${t("items.download")}`, 
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      didOpen: () => {
        const percentageText = document.getElementById("progress-percentage");
        let percentage = 0;
        const interval = setInterval(() => {
          if (percentageText) {
            percentage++;
            percentageText.textContent = `${percentage}%`;
            if (percentage >= 100) clearInterval(interval);
          }
        }, 30);
      },
      customClass: {
        popup: 'popup-download-toast',
        icon: 'popup-download-icon',
        title: 'popup-download-title',
        timerProgressBar: 'popup-download-timer-bar',
      },
    });
    return;
  };
  
  const handleCopy = async (format: "bbcode" | "markdown") => {
    try {
      const selectedProducts = filteredProducts.flatMap(product => {
        if (!product.items || !Array.isArray(product.items)) return [];
  
        return product.items.flatMap(aggregate => {
          if (!aggregate.items || !Array.isArray(aggregate.items)) return [];
  
          return aggregate.items
            .filter(item =>
              selectedItems.includes(aggregate.city?.id) &&
              item.availability_status === productType
            )
            .map(item => ({
              productType: productType, 
              productName: product.title,        
              cityName: aggregate.city?.name,   
              count: item.count,                 
              price: item.price,
              imageUrl: product.images && product.images.length > 0 ? product.images[0].image : "",
            }));
        });
      });
  
      if (selectedProducts.length === 0) {
        Swal.fire({
          toast: true,
          position: 'bottom',
          icon: 'error',
          iconColor: 'var(--accent-1)',
          title: `${t("items.notFound")}`,
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true,
          customClass: {
            popup: 'popup-error-toast', 
            icon: 'popup-error-icon',
            title: 'popup-error-title', 
            timerProgressBar: 'popup-error-timer-bar'
          }
        });
        return;  
      }
  
      const groupedProducts = selectedProducts.reduce((acc, item) => {
        if (!acc[item.productName]) {
          acc[item.productName] = { 
            imageUrl: item.imageUrl ?? "", 
            cities: {} 
          };
        }
        if (!acc[item.productName].cities[item.cityName]) acc[item.productName].cities[item.cityName] = [];
        acc[item.productName].cities[item.cityName].push({
          count: item.count,
          price: item.price,
        });
        return acc;
      }, {} as Record<string, { imageUrl: string, cities: Record<string, { count: number; price: number }[]> }>);
  
      const [dateOnly] = lastUpdate.split(" ");
  
      let textToCopy = "";
  
      if (format === "bbcode") {
        textToCopy += "[IMG]https://localhost/f/VFhcUkBTRlFF/Logo%201%20(1).png[/IMG]\n\n";
        
        for (const [productName, data] of Object.entries(groupedProducts)) {
          textToCopy += `[B]${productName} - ${dateOnly}[/B]\n[IMG]${data.imageUrl}[/IMG]\n`;
  
          for (const [cityName, records] of Object.entries(data.cities)) {
            const cityDetails = records
              .map(({ count, price }) => `${count} ${t("weight")}. - ${Intl.NumberFormat(locale).format(price)} ₽`)
              .join(" / ");
            textToCopy += `[B]${cityName}:[/B] ${cityDetails}\n`;
          }
  
          textToCopy += "[IMG]https://localhost/f/VFhcUkBTRlFF/Line%201%20(1).png[/IMG]";
        }
  
        textToCopy += "\nЗаĸлючаем сделĸи: [B]В[/B] [B]личных сообщениях[/B] / [B]Rutor[/B] / [B]Kraken[/B] / [B]Гарант[/B] \n [B]Постоянным ĸлиентам предоставляются сĸидĸи![/B] \nАĸтуальное наличие товаров всегда можно отслеживать на нашем сайте в разделе ОПТ: [URL='http://localhost']localhost[/URL]";
  
      } else if (format === "markdown") {
        textToCopy += `![Logo](https://localhost/f/VFhcUkBTRlFF/Logo%201%20(1).png)\n\n`;
    
        for (const [productName, data] of Object.entries(groupedProducts)) {
            textToCopy += `## ${productName} - ${dateOnly}\n`;
            if (data.imageUrl) {
                textToCopy += `![Product Image](${data.imageUrl})\n\n`;
            }
    
            for (const [cityName, records] of Object.entries(data.cities)) {
                const cityDetails = records
                    .map(({ count, price }) => `${count} ${t("weight")} - ${Intl.NumberFormat(locale).format(price)} ₽`)
                    .join(" / ");
                textToCopy += `- **${cityName}**: ${cityDetails}\n`;
            }
    
            textToCopy += "---\n";
        }
    
        textToCopy += `**Заключаем сделки**: **В личных сообщениях** / **Rutor** / **Kraken** / **Гарант**\n`;
        textToCopy += `**Постоянным клиентам предоставляются скидки!**\n`;
        textToCopy += `Актуальное наличие товаров всегда можно отслеживать на нашем сайте в разделе ОПТ: [localhost](http://localhost)`;
    }
    
  
      await navigator.clipboard.writeText(textToCopy);
      Swal.fire({
        toast: true,
        position: 'bottom',
        icon: 'success',
        iconColor: 'var(--accent-1)',
        title: `${t("items.success")}`,
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        customClass: {
          popup: 'popup-success-toast', 
          icon: 'popup-success-icon',
          title: 'popup-success-title',
          timerProgressBar: 'popup-success-timer-bar',
        }
      });
    } catch {
      Swal.fire({
        toast: true,
        position: 'bottom',
        icon: 'error',
        iconColor: 'var(--accent-1)',
        title: `${t("items.notFound")}`,
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        customClass: {
          popup: 'popup-error-toast', 
          icon: 'popup-error-icon',
          title: 'popup-error-title', 
          timerProgressBar: 'popup-error-timer-bar'
        }
      });
    }
  };

  return (  
    <div className="tabs__content" role="tabpanel" aria-labelledby="russia">
      <div className="localhost-wholesale-block">
        <div className="localhost-wholesale-block__left">
          <div className="localhost-wholesale-block__filter">
            <div className="checkbox">
              <input
                type="checkbox"
                id="selectAll"
                onChange={handleCheckboxChangeAll}
                checked={selectedItems.length === filteredCities.length}
              />
              <label className="checkbox__label" htmlFor="selectAll">{t("checkboxes.selectAll")}</label>
            </div>
            <div className="input-wrapper search">
              <input
                className="input search"    
                placeholder={t("items.searchPlaceholder")}
                onChange={handleSearchChange}
              />
            </div>
          </div>
          <div className="localhost-wholesale-block__checkboxes">
            {filteredCities.map((city) => (
              <div className="checkbox" key={city.id}>
                <input
                  type="checkbox"
                  id={`city-${city.id}`}
                  value={city.id}
                  checked={selectedItems.includes(city.id)}
                  onChange={handleCheckboxChange}
                />
                <label className="checkbox__label" htmlFor={`city-${city.id}`}>
                  {city.name}
                </label>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="tabs">
        <div
          className="tabs-tablist availability"
          role="tablist"
          aria-label="Availability"
        >
          <div
            className="tabs-tablist__button"
            role="tab"
            aria-selected={productType === "in_stock"}
            onClick={() => setProductType("in_stock")}
          >
            {t("filters.in_stock")}
          </div>
          <div
            className="tabs-tablist__button"
            role="tab"
            aria-selected={productType === "preorder"}
            onClick={() => setProductType("preorder")}
          >
            {t("filters.preorder")}
          </div>
        </div>
        <div className="last-update">
          {t("items.lastUpdate")}: {lastUpdate}
        </div>
      </div>
      
      <div className="localhost-wholesale__buttons">
    <button className="button-functional" name="download" onClick={handleDownload}>
      <svg>
        <use xlinkHref="static/svg/sprite.svg#icon-download"></use>
      </svg>
      {t("links.excel")}
    </button>

    <div className="copy-dropdown" ref={dropdownRef}>
      <button className="button-functional" name="copy-dropdown" onClick={toggleDropdown}>
        <svg>
          <use xlinkHref="static/svg/sprite.svg#icon-copy-1"></use>
        </svg>
        {t("links.copy")}
      </button>

      <div className={`dropdown-menu ${isDropdownOpen ? "show" : ""}`}>
        <button className="dropdown-item" onClick={() => handleCopy("bbcode")}>{t("items.bbcode")}</button>
        <button className="dropdown-item" onClick={() => handleCopy("markdown")}>Markdown</button>
      </div>
    </div>
  </div>

        
      {filteredProducts.length > 0 ? (
        <ul className="localhost-wholesale-block__products">
          {filteredProducts.map((product) => (
            <li key={product.id} className="localhost-wholesale-block__product">
              <div className="localhost-wholesale-block__product-top">
                <div className="localhost-wholesale-block__product-info">
                  <h2 className="localhost-wholesale-block__product-info__title">
                    {product.title}
                  </h2>
                  <div className="localhost-wholesale-block__product-info__description">
                    <MarkdownRenderer content={product.description || ""} />
                  </div>
                </div>
                {product.images && (
                  <div className="localhost-wholesale-block__product-images">
                    {product.images.map((image) => (
                      <div
                        className="localhost-wholesale-block__product-image-container"
                        key={image.id}
                      >
                        <Image
                          className="localhost-wholesale-block__product-image"
                          src={image.image || ""}
                          alt={product.title}
                          width={300}
                          height={500}
                        />
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="localhost-wholesale-block__product-info__buttons">
                <button className="button" onClick={() => togglePrice(product.id)}>
                  <svg
                    className={`carriage-bottom ${
                      priceStates[product.id] ? "rotated" : ""
                    }`}
                  >
                    <use href="/static/svg/sprite.svg#icon-carriage"></use>
                  </svg>
                  {priceStates[product.id]
                    ? t("functions.collapse")
                    : t("functions.price")}
                </button>
                <button className="button"
                  onClick={() => window.open(`${product.buy_url}`, '_blank')}
                >
                  <svg>
                    <use href="/static/svg/sprite.svg#icon-buy"></use>
                  </svg>
                  
                  {t("functions.buy")}
                </button>
              </div>
              
              {priceStates[product.id] && product.items ? (
                <div className="localhost-wholesale-block__product-bottom">
                  {product.items.length > 0 ? (
                    product.items
                      .filter((aggregate) => selectedItems.includes(aggregate.city.id))
                      .map((aggregate) => (
                        <div
                          key={aggregate.city.id}
                          className="localhost-wholesale-block__product-item"
                        >
                          <ul className="localhost-wholesale-block__product-item__city">
                            <svg
                              className="icon"
                              xmlns="http://www.w3.org/2000/svg"
                              width="7"
                              height="7"
                              viewBox="0 0 7 7"
                              fill="none"
                            >
                              <circle cx="3.5" cy="3.5" r="3.5" fill="var(--text)" />
                            </svg>
                            <svg className="icon-tablet" xmlns="http://www.w3.org/2000/svg" width="12" height="11" viewBox="0 0 12 11" fill="none">
                              <g clipPath="url(#clip0_395_3266)">
                                <path fillRule="evenodd" clipRule="evenodd" d="M5.97134 4.04828V2.49304L4.97014 2.07854C4.87762 2.04026 4.7737 2.04026 4.68118 2.07854C4.25033 2.25701 2.97101 2.78665 2.44181 3.00579C2.37275 3.03436 2.31372 3.08278 2.27219 3.14493C2.23066 3.20709 2.2085 3.28017 2.20852 3.35493V3.9212C2.20851 3.99594 2.18635 4.06899 2.14482 4.13112C2.10329 4.19325 2.04427 4.24165 1.97522 4.27021L0.233313 4.99153C0.164251 5.02009 0.105215 5.06852 0.0636816 5.13067C0.0221483 5.19282 -1.43391e-05 5.26591 6.96037e-09 5.34067V10.5H2.23948V5.48816C2.23947 5.33868 2.28378 5.19256 2.36682 5.06828C2.44986 4.944 2.56788 4.84716 2.70596 4.79002L4.94544 3.86277C5.03702 3.82479 5.13519 3.80524 5.23433 3.80524C5.33347 3.80524 5.43164 3.82479 5.52322 3.86277L5.97134 4.04828ZM7.45514 4.66267C7.47158 4.61208 7.5036 4.568 7.54661 4.53673C7.58963 4.50546 7.64144 4.48862 7.69461 4.48861H8.29618C8.32926 4.4886 8.36201 4.4951 8.39256 4.50776C8.42312 4.52041 8.45088 4.53896 8.47427 4.56236C8.49766 4.58575 8.51621 4.61352 8.52886 4.64409C8.54151 4.67466 8.54802 4.70742 8.54801 4.7405V5.43575C8.54802 5.46884 8.54152 5.5016 8.52886 5.53217C8.51621 5.56274 8.49766 5.59051 8.47428 5.61391C8.45089 5.6373 8.42312 5.65585 8.39257 5.66851C8.36201 5.68116 8.32926 5.68766 8.29618 5.68765H8.2292V10.5H11.5833V1.8051C11.5833 1.73034 11.5612 1.65726 11.5197 1.59511C11.4781 1.53296 11.4191 1.48453 11.35 1.45596C10.8209 1.2368 9.54152 0.707051 9.11067 0.528714C9.01815 0.490429 8.91423 0.490429 8.82171 0.528714C8.39074 0.707051 7.11154 1.23682 6.58223 1.45596C6.5132 1.48455 6.45419 1.53299 6.41269 1.59514C6.37118 1.65729 6.34903 1.73036 6.34905 1.8051V4.2046L7.45514 4.66267ZM10.4896 4.7405C10.4896 4.6737 10.463 4.60965 10.4158 4.56241C10.3686 4.51518 10.3046 4.48863 10.2378 4.48861H9.63608C9.56931 4.48863 9.50528 4.51518 9.45806 4.56241C9.41084 4.60965 9.3843 4.6737 9.38428 4.7405V5.43575C9.3843 5.50255 9.41084 5.56661 9.45806 5.61384C9.50528 5.66108 9.56931 5.68762 9.63608 5.68765H10.2378C10.3046 5.68762 10.3686 5.66108 10.4158 5.61384C10.463 5.56661 10.4896 5.50255 10.4896 5.43575V4.7405ZM8.54799 2.49177C8.548 2.45869 8.5415 2.42592 8.52884 2.39536C8.51619 2.36479 8.49764 2.33701 8.47426 2.31362C8.45087 2.29023 8.42311 2.27167 8.39255 2.25902C8.36199 2.24637 8.32924 2.23986 8.29617 2.23988H7.69459C7.62781 2.2399 7.56378 2.26645 7.51656 2.31368C7.46935 2.36092 7.44281 2.42497 7.44278 2.49177V3.18702C7.44281 3.25382 7.46935 3.31788 7.51656 3.36511C7.56378 3.41235 7.62781 3.43889 7.69459 3.43892H8.29617C8.32924 3.43893 8.36199 3.43242 8.39254 3.41977C8.4231 3.40711 8.45087 3.38856 8.47425 3.36517C8.49764 3.34177 8.51619 3.314 8.52884 3.28343C8.54149 3.25287 8.548 3.22011 8.54799 3.18702V2.49177Z" fill="var(--text)"/>
                                <path fillRule="evenodd" clipRule="evenodd" d="M7.85147 5.48817C7.85147 5.41343 7.8293 5.34038 7.78777 5.27825C7.74624 5.21612 7.68722 5.16772 7.61818 5.13916C7.089 4.92 5.80966 4.39025 5.37881 4.21192C5.33301 4.1929 5.28392 4.18311 5.23433 4.18311C5.18474 4.18311 5.13565 4.1929 5.08985 4.21192C4.65888 4.39025 3.37968 4.92002 2.85037 5.13916C2.78135 5.16775 2.72236 5.21616 2.68086 5.27828C2.63935 5.34041 2.61719 5.41345 2.61719 5.48817V10.5H7.85147V5.48817ZM4.81613 8.42371C4.81615 8.39063 4.80964 8.35787 4.79698 8.32731C4.78432 8.29675 4.76575 8.26899 4.74235 8.24561C4.71898 8.22222 4.69123 8.20365 4.66068 8.19099C4.63013 8.17833 4.59739 8.17181 4.56432 8.17181H3.96275C3.89597 8.17184 3.83194 8.19838 3.78472 8.24562C3.7375 8.29285 3.71097 8.35691 3.71094 8.42371V9.11896C3.71097 9.18575 3.7375 9.24981 3.78472 9.29704C3.83194 9.34428 3.89597 9.37083 3.96275 9.37085H4.56432C4.63117 9.37085 4.69515 9.34427 4.74235 9.29705C4.76575 9.27367 4.78431 9.24591 4.79697 9.21535C4.80963 9.18479 4.81614 9.15204 4.81613 9.11896V8.42371ZM6.75759 8.42371C6.7576 8.39062 6.75109 8.35786 6.73844 8.32729C6.72579 8.29672 6.70724 8.26895 6.68385 8.24556C6.66047 8.22216 6.6327 8.20361 6.60214 8.19095C6.57159 8.1783 6.53883 8.1718 6.50576 8.17181H5.90419C5.83741 8.17184 5.77338 8.19838 5.72616 8.24562C5.67894 8.29285 5.65241 8.35691 5.65238 8.42371V9.11896C5.65241 9.18575 5.67894 9.24981 5.72616 9.29704C5.77338 9.34428 5.83741 9.37083 5.90419 9.37085H6.50576C6.53883 9.37086 6.57158 9.36436 6.60214 9.3517C6.6327 9.33905 6.66046 9.32049 6.68385 9.2971C6.70724 9.27371 6.72578 9.24594 6.73844 9.21537C6.75109 9.1848 6.7576 9.15204 6.75759 9.11896V8.42371ZM4.81613 6.17498C4.81616 6.14189 4.80965 6.10913 4.79699 6.07857C4.78433 6.04801 4.76576 6.02025 4.74235 5.99688C4.71898 5.97349 4.69123 5.95492 4.66068 5.94226C4.63013 5.9296 4.59739 5.92308 4.56432 5.92308H3.96275C3.89597 5.9231 3.83194 5.94965 3.78472 5.99689C3.7375 6.04412 3.71097 6.10818 3.71094 6.17498V6.87009C3.71093 6.90318 3.71743 6.93594 3.73008 6.96651C3.74273 6.99707 3.76128 7.02485 3.78466 7.04824C3.80805 7.07164 3.83581 7.09019 3.86637 7.10285C3.89693 7.11551 3.92967 7.12202 3.96275 7.12201H4.56432C4.63117 7.12201 4.69515 7.09556 4.74235 7.04832C4.76576 7.02493 4.78433 6.99714 4.79699 6.96656C4.80965 6.93598 4.81616 6.90319 4.81613 6.87009V6.17498ZM6.75759 6.17498C6.75759 6.1081 6.73114 6.0441 6.68392 5.99688C6.6367 5.94966 6.57261 5.92308 6.50576 5.92308H5.90419C5.83741 5.9231 5.77338 5.94965 5.72616 5.99689C5.67894 6.04412 5.65241 6.10818 5.65238 6.17498V6.87009C5.65237 6.90318 5.65887 6.93594 5.67152 6.96651C5.68417 6.99707 5.70272 7.02485 5.7261 7.04824C5.74949 7.07164 5.77725 7.09019 5.80781 7.10285C5.83836 7.11551 5.87111 7.12202 5.90419 7.12201H6.50576C6.57261 7.12201 6.6367 7.09556 6.68392 7.04832C6.73114 7.00108 6.75759 6.93697 6.75759 6.87009V6.17498Z" fill="var(--text)"/>
                              </g>
                              <defs>
                                <clipPath id="clip0_395_3266">
                                  <rect width="11.5833" height="10" fill="white" transform="translate(0 0.5)"/>
                                </clipPath>
                              </defs>
                            </svg>
                            <li>{aggregate.city.name}</li>
                          </ul>
                          <ul className="localhost-wholesale-block__product-item__list">
                            {renderItems(aggregate)}
                          </ul>
                        </div>
                      ))
                  ) : (
                    <p>{t("items.notFound")}</p>
                  )}
                </div>
              ) : null}
            </li>
          ))}
        </ul>
      ) : (
        <p>{t("items.notFound")}</p>
      )}
    </div>
  );
}
