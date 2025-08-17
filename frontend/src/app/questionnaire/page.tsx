import Breadcrumbs from "@/components/Breadcrumbs/Breadcrumbs";
import QuestionnaireForm from "@/components/QuestionnaireForm/QuestionnaireForm";
import { useTranslations } from "next-intl";

export default function Questionnaire() {
  const t = useTranslations("QuestionnairePage");

  return (
    <div className="localhost-questionnaire" id="questionnaire">
      <section>
        <div className="container">
          <Breadcrumbs
            page={t("breadcrumbs.second")}
            subPage={t("breadcrumbs.first")}
            subPageHref="/work"
          />
          <QuestionnaireForm base_url={process.env.VACANCIES_BASE_URL || 'https://localhost/info'}/>
        </div>
      </section>
    </div>
  );
}
