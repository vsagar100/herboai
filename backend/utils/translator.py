import os
import argostranslate.package
import argostranslate.translate

# One-time installation directory (inside project)
ARGOS_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "argos_packages")
os.makedirs(ARGOS_DATA_DIR, exist_ok=True)

# Point Argos to our custom dir
argostranslate.package.install_from_path = lambda p: argostranslate.package.install_from_path(p, ARGOS_DATA_DIR)


def ensure_package(from_code: str, to_code: str):
    """
    Ensure Argos Translate package is installed for given language pair.
    Downloads from Argos repo if not found.
    """
    installed = argostranslate.translate.get_installed_languages()

    # Already available?
    for lang in installed:
        if lang.code == from_code:
            for to_lang in lang.translations:
                if to_lang.language.code == to_code:
                    return True

    # Not installed → fetch and install
    print(f"[Translator] Installing package {from_code}->{to_code} ...")
    available_packages = argostranslate.package.get_available_packages()
    package = next((p for p in available_packages
                    if p.from_code == from_code and p.to_code == to_code), None)
    if not package:
        print(f"[Translator] Package {from_code}->{to_code} not available!")
        return False
    download_path = package.download(ARGOS_DATA_DIR)
    argostranslate.package.install_from_path(download_path)
    return True


def translate_text(text: str, from_code="en", to_code="hi") -> str:
    """
    Translate text offline using Argos Translate.
    Falls back to returning original if translation not available.
    """
    if not text:
        return text

    try:
        ensure_package(from_code, to_code)
        return argostranslate.translate.translate(text, from_code, to_code)
    except Exception as e:
        print(f"[Translator] Fallback (no translation {from_code}->{to_code}): {e}")
        return text
