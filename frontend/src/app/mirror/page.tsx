"use client"; 

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import Breadcrumbs from "@/components/Breadcrumbs/Breadcrumbs";
import api from "@/lib/api";
import { Project } from "@/types/dtos";
import Link from "next/link";
import Loader from "@/components/Loader/Loader"; 
import ProcessedMarkdown from "@/components/MarkdownRenderer/ProcessedMarkdownRenderer";
import CopyButton from "@/components/CopyButton/CopyButton";


export default function Mirror() {
  const locale = useLocale(); 
  const [mirrors, setMirrors] = useState<Project[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); 

      try {
        const allMirrors = await api<Project[]>("/projects", {
          headers: { "Accept-Language": locale },
        });

        const sortedMirrors = allMirrors.sort((a, b) => a.id - b.id);

        setMirrors(sortedMirrors);
      } catch (error) {
        console.error("Ошибка загрузки данных:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData(); 
  }, [locale]); 

  const t = useTranslations("MirrorPage");

  if (loading) {
    return (
      <div className="localhost-mirror" id="mirror">
        <section>
          <div className="container">
            <Loader /> 
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="localhost-mirror" id="mirror">
      <section>
        <div className="container">
          <Breadcrumbs page={t("breadcrumbs")} />
          <div className="localhost-mirror-heading">
            <div className="localhost-mirror-heading__info">{t("heading")}</div>
          </div>
          <div className="localhost-mirror-content">
            {mirrors.map((mirror) => (
              <div className="localhost-mirror-content__wrapper" key={mirror.id}>
                <div className="localhost-mirror-content__heading">
                  {mirror.title}
                </div>
                <div className="localhost-mirror-content__info">
                  <ProcessedMarkdown content={mirror.description} />
                </div>
                <div className="localhost-mirror-content__links">
                  {mirror?.links?.map((link) => (
                    <div
                      className="localhost-mirror-content-link"
                      key={link.link}
                    >
                      <div className="localhost-mirror-content-link__info">
                        <div
                          className={`localhost-mirror-content-link__status ${
                            link.is_active ? "" : "dont-work"
                          }`}
                        ></div>
                        <div className="localhost-mirror-content-link__address">
                          <span>{link.link}</span>
                        </div>
                      </div>
                      <div className="button-container">
                        <a className={`button ${link.is_active ? "" : "disabled"} copy`}><CopyButton text={link.link} /></a>
                        
                        <Link
                          className={`button ${link.is_active ? "" : "disabled"}`}
                          href={`https://${link.link}`}
                          target="_blank"
                        >
                          {t("button")}
                        </Link> 
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
