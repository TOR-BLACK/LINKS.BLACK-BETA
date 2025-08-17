// В файле page.tsx (серверный компонент)

import { getLocale, getTranslations } from "next-intl/server";
import Vacancies from "@/components/Vacancies/Vacancies";
import Breadcrumbs from "@/components/Breadcrumbs/Breadcrumbs";
import { Vacancy1 } from "@/types/dtos";

export const revalidate = 60;

export default async function Work() {
  let vacancies: Vacancy1[] = [];

  try {
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
    if (!baseUrl) throw new Error("API base URL not defined");

    const locale = await getLocale();
    const is_test = process.env.VACANCIES_BASE_URL?.includes('dvd-test') ? 'true' : 'false';
    
    const response = await fetch(`${baseUrl}/vacancies-transalted/?lang=${locale}&test=${is_test}`);
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }
    vacancies = await response.json();
  } catch (error) {
    console.error(error);
  }

  const t = await getTranslations("WorkPage");

  return (
    <div className="localhost-work" id="work">
      <section>
        <div className="container">
          <Breadcrumbs page={t("breadcrumbs")} />
          <div className="localhost-work-heading">
            <div className="localhost-work-heading__info">{t("headingInfo")}</div>
          </div>
          <Vacancies vacancies={vacancies} job1_url={process.env.VACANCIES_BASE_URL || 'https://localhost/info'} job2_url={process.env.VACANCIES2_BASE_URL || 'https://localhost/info2'}/>
        </div>
      </section>
    </div>
  );
}
