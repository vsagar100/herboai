import React from "react";
import { AlertTriangle } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import StaticPageLayout from "../components/StaticPageLayout";

export default function Disclaimer() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  return (
    <StaticPageLayout
      title={t.disclaimer.title}
      subtitle={t.disclaimer.subtitle}
      icon={<AlertTriangle className="w-6 h-6" />}
    >
      <p>{t.disclaimer.content}</p>
      <p>{t.disclaimer.extra}</p>
    </StaticPageLayout>
  );
}
