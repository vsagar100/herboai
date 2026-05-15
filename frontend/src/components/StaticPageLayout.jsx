import React from "react";

export default function StaticPageLayout({ title, subtitle, icon, children }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-lime-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-white/90 rounded-3xl shadow-xl border border-emerald-100 p-8 md:p-12">
          <div className="flex items-start gap-4 mb-8">
            <div className="bg-emerald-100 p-3 rounded-2xl text-emerald-700">
              {icon}
            </div>
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
                {title}
              </h1>
              {subtitle ? (
                <p className="text-gray-600 mt-2">{subtitle}</p>
              ) : null}
            </div>
          </div>
          <div className="space-y-4 text-gray-700 leading-relaxed">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
