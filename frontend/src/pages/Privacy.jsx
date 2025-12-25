import React from "react";
import { ShieldCheck } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import StaticPageLayout from "../components/StaticPageLayout";

export default function Privacy() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  return (
    <StaticPageLayout
      title={t.footer.privacy}
      subtitle={t.privacyPage.subtitle}
      icon={<ShieldCheck className="w-6 h-6" />}
    >
      <p>{t.privacyPage.p1}</p>
      <p>{t.privacyPage.p2}</p>
      <p>{t.privacyPage.p3}</p>
    </StaticPageLayout>
  );
}
