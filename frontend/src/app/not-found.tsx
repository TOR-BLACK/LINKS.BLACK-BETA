import { useTranslations } from "next-intl";

export default function Custom404() {
  const t = useTranslations("NotFound");
  return (
    <div
      className="container localhost-faq-heading"
      style={{
        minHeight: "70vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <h1 className="h1">{t("message")}</h1>
    </div>
  );
}
