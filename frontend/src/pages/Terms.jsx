import React from "react";
import { FileText } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import StaticPageLayout from "../components/StaticPageLayout";

export default function Terms() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  return (
    <StaticPageLayout
      title={t.footer.terms}
      subtitle={t.termsPage.subtitle}
      icon={<FileText className="w-6 h-6" />}
    >
      <p>{t.termsPage.p1}</p>
      <p>{t.termsPage.p2}</p>
      <p>{t.termsPage.p3}</p>
    </StaticPageLayout>
  );
}
