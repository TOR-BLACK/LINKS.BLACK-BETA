"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";
import Loader from "@/components/Loader/Loader";
import Breadcrumbs from "@/components/Breadcrumbs/Breadcrumbs";
import MarkdownRenderer from "@/components/MarkdownRenderer/MarkdownRenderer";
import { useLocale, useTranslations } from "next-intl";
import { APIResponse, ResourcePolicy } from "@/types/dtos";

export default function PrivacyPolicyPage() {
  const [policies, setPolicies] = useState<ResourcePolicy[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const t = useTranslations("PrivacyPolicyPage");
  const locale = useLocale();

  useEffect(() => {
    const fetchPolicies = async () => {
      setLoading(true);
      try {
        const response = await api<APIResponse>("/resource-policy", {
          headers: { "Accept-Language": locale },
        });
        setPolicies(response.results.sort((a, b) => a.position - b.position));
      } catch (error) {
        console.error("Ошибка загрузки данных:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchPolicies();
  }, [locale]);

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="localhost-policy" id="policy">
      <section>
        <div className="container">
          <Breadcrumbs page={t("breadcrumbs")} />
          <div className="localhost-privacy-heading">
            <h1 className="h1">{t("heading")}</h1>
          </div>

          <div className="localhost-privacy-content">
            <div className="localhost-privacy-content_text">
              {policies.map((policy) => (
                <div key={policy.position}>
                  <h2>{(policy.position) + ". " + policy.heading}</h2>
                  <MarkdownRenderer content={policy.content} />
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
