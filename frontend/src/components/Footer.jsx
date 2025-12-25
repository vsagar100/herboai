import React from "react";
import { Link } from "react-router-dom";
import { Leaf } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";

export default function Footer() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;
  const f = t.footer;

  return (
    <footer className="bg-white border-t">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 grid md:grid-cols-4 gap-8">
        {/* Brand */}
        <div>
          <div className="flex items-center gap-2 mb-2">
            <div className="bg-green-100 p-2 rounded-full">
              <Leaf className="w-5 h-5 text-green-600" />
            </div>
            <div className="font-semibold">HerboAI</div>
          </div>
          <p className="text-sm text-gray-600">{f.tagline}</p>
        </div>

        {/* Quick links */}
        <div>
          <div className="font-semibold mb-2">{f.quickLinks}</div>
          <ul className="space-y-1 text-sm text-gray-600">
            <li>
              <Link className="hover:text-green-600" to="/">
                {t.nav.home}
              </Link>
            </li>
            <li>
              <Link className="hover:text-green-600" to="/library">
                {t.nav.library}
              </Link>
            </li>
            <li>
              <Link className="hover:text-green-600" to="/chat">
                {t.nav.chat}
              </Link>
            </li>
          </ul>
        </div>

        {/* Support */}
        <div>
          <div className="font-semibold mb-2">{f.support}</div>
          <ul className="space-y-1 text-sm text-gray-600">
            <li>
              <Link className="hover:text-green-600" to="/contact">
                {f.contact}
              </Link>
            </li>
            <li>
              <a className="hover:text-green-600" href="mailto:help@herboai.local">
                help@herboai.local
              </a>
            </li>
          </ul>
        </div>

        {/* Legal */}
        <div>
          <div className="font-semibold mb-2">{f.legal}</div>
          <ul className="space-y-1 text-sm text-gray-600">
            <li>
              <Link className="hover:text-green-600" to="/disclaimer">
                {f.disclaimer}
              </Link>
            </li>
            <li>
              <Link className="hover:text-green-600" to="/privacy">
                {f.privacy}
              </Link>
            </li>
            <li>
              <Link className="hover:text-green-600" to="/terms">
                {f.terms}
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </footer>
  );
}
