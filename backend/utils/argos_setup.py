import argostranslate.package

def install_languages():
    print("🔄 Updating Argos Translate package index...")
    argostranslate.package.update_package_index()

    available_packages = argostranslate.package.get_available_packages()

    def install_pair(from_code, to_code):
        pkg = next((p for p in available_packages if p.from_code == from_code and p.to_code == to_code), None)
        if pkg:
            print(f"⬇ Downloading {from_code} → {to_code} package...")
            download_path = pkg.download()
            argostranslate.package.install_from_path(download_path)
        else:
            print(f"⚠ Package {from_code} → {to_code} not found in index.")

    # English ↔ Hindi
    install_pair("en", "hi")
    install_pair("hi", "en")

    # English ↔ Marathi
    install_pair("en", "mr")
    install_pair("mr", "en")

    print("✅ All language packages installed.")

if __name__ == "__main__":
    install_languages()
