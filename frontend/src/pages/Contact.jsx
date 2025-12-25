import React from "react";
import { Mail, MapPin, Clock } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import StaticPageLayout from "../components/StaticPageLayout";

export default function Contact() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  return (
    <StaticPageLayout
      title={t.footer.contact}
      subtitle={t.contactPage.subtitle}
      icon={<Mail className="w-6 h-6" />}
    >
      <p>{t.contactPage.intro}</p>
      <div className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-2xl border border-emerald-100 bg-emerald-50 p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-emerald-700">
            <Mail className="w-4 h-4" />
            {t.contactPage.emailLabel}
          </div>
          <a
            className="mt-2 inline-block text-gray-800 hover:text-emerald-700"
            href="mailto:help@herboai.local"
          >
            help@herboai.local
          </a>
        </div>
        <div className="rounded-2xl border border-emerald-100 bg-emerald-50 p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-emerald-700">
            <Clock className="w-4 h-4" />
            {t.contactPage.responseTimeLabel}
          </div>
          <p className="mt-2 text-gray-700">{t.contactPage.responseTimeValue}</p>
        </div>
        <div className="rounded-2xl border border-emerald-100 bg-emerald-50 p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-emerald-700">
            <MapPin className="w-4 h-4" />
            {t.contactPage.campusLabel}
          </div>
          <p className="mt-2 text-gray-700">{t.contactPage.campusValue}</p>
        </div>
      </div>
    </StaticPageLayout>
  );
}
