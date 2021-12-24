from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _


def raise_for_attr(attr: str):
    raise ImproperlyConfigured(_(f"Please specify {attr}"))


HCAPTCHA_PROVIDER_NAME = "hcaptcha"

HCAPTCHA_URL = getattr(settings, "HCAPTCHA_URL", "https://hcaptcha.com/siteverify")

HCAPTCHA_SECRET_KEY = getattr(settings, "HCAPTCHA_SECRET_KEY", None)
HCAPTCHA_SITE_KEY = getattr(settings, "HCAPTCHA_SITE_KEY", None)

HCAPTCHA_JS = getattr(settings, "HCAPTCHA_JS", "https://js.hcaptcha.com/1/api.js")

if not HCAPTCHA_SECRET_KEY:
    raise_for_attr("HCAPTCHA_SECRET_KEY")

if not HCAPTCHA_SITE_KEY:
    raise_for_attr("HCAPTCHA_SITE_KEY")

PROVIDER = getattr(settings, "CAPTCHA_PROVIDER", HCAPTCHA_PROVIDER_NAME)

if PROVIDER == HCAPTCHA_PROVIDER_NAME:
    CAPTCHA_SITE_KEY = HCAPTCHA_SITE_KEY
    CAPTCHA_SECRET_KEY = HCAPTCHA_SECRET_KEY
    PROVIDER_URL = HCAPTCHA_URL
    PROVIDER_JS = HCAPTCHA_JS
else:
    raise ImproperlyConfigured(
        _(f'Provider  "{PROVIDER}" hasn\'t been implemented yet.')
    )
