# backend/utils/translator.py
import argostranslate.package
import argostranslate.translate
import os

# Pre-install language packages offline before using:
# python -m argostranslate.package install <package_file>
# Available packages: https://www.argosopentech.com/argospm/

# Example: English↔Hindi, English↔Marathi
LANG_PAIRS = [("en", "hi"), ("hi", "en"), ("en", "mr"), ("mr", "en")]

def install_language_pair(from_code, to_code):
    """Download and install a language pair if not installed"""
    packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        (p for p in packages if p.from_code == from_code and p.to_code == to_code),
        None
    )
    if package_to_install:
        argostranslate.package.install_from_path(package_to_install.download())

def translate_text(text: str, from_lang="en", to_lang="hi") -> str:
    try:
        return argostranslate.translate.translate(text, from_lang, to_lang)
    except Exception as e:
        print(f"[Translator] Fallback translation failed: {e}")
        return text

install_language_pair("en", "hi")
install_language_pair("hi", "en")
install_language_pair("en", "mr")
install_language_pair("mr", "en")