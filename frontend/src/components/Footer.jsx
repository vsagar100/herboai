import React from "react";
import { Leaf } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";

export default function Footer() {
  const [state] = useGlobalState();
  const f = translations[state.language].footer;

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
            <li>Home</li>
            <li>Plant Library</li>
            <li>AI Assistant</li>
          </ul>
        </div>

        {/* Support */}
        <div>
          <div className="font-semibold mb-2">{f.support}</div>
          <ul className="space-y-1 text-sm text-gray-600">
            <li>{f.contact}</li>
            <li>help@herboai.local</li>
          </ul>
        </div>

        {/* Legal */}
        <div>
          <div className="font-semibold mb-2">{f.legal}</div>
          <ul className="space-y-1 text-sm text-gray-600">
            <li>{f.disclaimer}</li>
            <li>{f.privacy}</li>
            <li>{f.terms}</li>
          </ul>
        </div>
      </div>
    </footer>
  );
}
