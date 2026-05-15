import os

class Config:
    # Point to your created DB (from the v2.1 schema you loaded)
    DB_PATH = os.environ.get("HERBOAI_DB_PATH", os.path.abspath("../db/new_herboai.db"))
    # Global pagination defaults
    DEFAULT_PAGE_SIZE = int(os.environ.get("HERBOAI_PAGE_SIZE", "20"))
    MAX_PAGE_SIZE = int(os.environ.get("HERBOAI_MAX_PAGE_SIZE", "500"))
    MEDIA_ROOT = os.environ.get("HERBOAI_MEDIA_ROOT", os.path.abspath("static/plant_images"))

    # When True, admin CRUD auto-translates to hi/mr.
    # When False, English is still indexed, but hi/mr auto-translation is skipped.
    ENABLE_I18N_TRANSLATION = os.environ.get("HERBOAI_ENABLE_I18N", "false").lower() in ("true", "1", "yes")

