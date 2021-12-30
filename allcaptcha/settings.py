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
HCAPTCHA_JS_CALLBACK = getattr(settings, "HCAPTCHA_JS_CALLBACK", "onHcaptchaSubmit")

RECAPTCHA_PROVIDER_NAME = "recaptcha"

RECAPTCHA_URL = getattr(
    settings, "RECAPTCHA_URL", "https://www.google.com/recaptcha/api/siteverify"
)

RECAPTCHA_V2_SECRET_KEY = getattr(settings, "RECAPTCHA_V2_SECRET_KEY", None)
RECAPTCHA_V2_SITE_KEY = getattr(settings, "RECAPTCHA_V2_SITE_KEY", None)

RECAPTCHA_V3_SECRET_KEY = getattr(settings, "RECAPTCHA_V3_SECRET_KEY", None)
RECAPTCHA_V3_SITE_KEY = getattr(settings, "RECAPTCHA_V3_SITE_KEY", None)

RECAPTCHA_JS = "https://www.google.com/recaptcha/api.js"
RECAPTCHA_JS_CALLBACK = getattr(settings, "RECAPTCHA_JS_CALLBACK", "onRecaptchaSubmit")

RECAPTCHA_VERSION = getattr(settings, "RECAPTCHA_VERSION", 2)

if RECAPTCHA_VERSION == 3:
    RECAPTCHA_MIN_SCORE = getattr(settings, "RECAPTCHA_MIN_SCORE", 0.6)

PROVIDER = getattr(settings, "CAPTCHA_PROVIDER", HCAPTCHA_PROVIDER_NAME)

CHALLENGE_THEME = getattr(settings, "CAPTCHA_CHALLENGE_THEME", "light")

CHALLENGE_SIZE = getattr(settings, "CAPTCHA_CHALLENGE_SIZE", "normal")

if PROVIDER == HCAPTCHA_PROVIDER_NAME:
    if not HCAPTCHA_SECRET_KEY:
        raise_for_attr("HCAPTCHA_SECRET_KEY")

    if not HCAPTCHA_SITE_KEY:
        raise_for_attr("HCAPTCHA_SITE_KEY")
    CAPTCHA_SITE_KEY = HCAPTCHA_SITE_KEY
    CAPTCHA_SECRET_KEY = HCAPTCHA_SECRET_KEY
    PROVIDER_URL = HCAPTCHA_URL
    PROVIDER_CLASS_NAME = "h-captcha"
    PROVIDER_JS = HCAPTCHA_JS
    PROVIDER_JS_CALLBACK = HCAPTCHA_JS_CALLBACK
elif PROVIDER == RECAPTCHA_PROVIDER_NAME:
    PROVIDER_JS = RECAPTCHA_JS
    PROVIDER_JS_CALLBACK = RECAPTCHA_JS_CALLBACK
    PROVIDER_URL = RECAPTCHA_URL
    PROVIDER_CLASS_NAME = "g-recaptcha"
    if RECAPTCHA_VERSION == 2:
        if not RECAPTCHA_V2_SECRET_KEY:
            raise_for_attr("RECAPTCHA_V2_SECRET_KEY")

        if not RECAPTCHA_V2_SITE_KEY:
            raise_for_attr("RECAPTCHA_V2_SITE_KEY")
        CAPTCHA_SITE_KEY = RECAPTCHA_V2_SITE_KEY
        CAPTCHA_SECRET_KEY = RECAPTCHA_V2_SECRET_KEY

    else:
        if not RECAPTCHA_V3_SECRET_KEY:
            raise_for_attr("RECAPTCHA_V3_SECRET_KEY")

        if not RECAPTCHA_V3_SITE_KEY:
            raise_for_attr("RECAPTCHA_V3_SITE_KEY")
        CAPTCHA_SITE_KEY = RECAPTCHA_V3_SITE_KEY
        CAPTCHA_SECRET_KEY = RECAPTCHA_V3_SECRET_KEY

else:
    raise ImproperlyConfigured(
        _(f'Provider  "{PROVIDER}" hasn\'t been implemented yet.')
    )
