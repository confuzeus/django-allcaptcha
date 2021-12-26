from django import template
from allcaptcha import settings
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag
def get_sitekey():
    return settings.CAPTCHA_SITE_KEY


@register.simple_tag
def get_challenge_class():
    return settings.PROVIDER_CLASS_NAME


@register.simple_tag
def get_callback_name():
    return settings.PROVIDER_JS_CALLBACK


@register.inclusion_tag("allcaptcha/challenge.html")
def render_challenge(challenge_type="visible", text="submit") -> dict:
    if challenge_type == "visible" and (
        settings.PROVIDER == settings.RECAPTCHA_PROVIDER_NAME
        and settings.RECAPTCHA_VERSION == 3
    ):
        raise ValueError(_("Recaptcha V3 can't be visible."))
    ctx = {
        "challenge_type": challenge_type,
        "callback": settings.PROVIDER_JS_CALLBACK,
        "text": text,
    }
    if (
        settings.PROVIDER == settings.HCAPTCHA_PROVIDER_NAME
        or settings.PROVIDER == settings.RECAPTCHA_PROVIDER_NAME
    ):
        ctx.update(
            {
                "class_name": settings.PROVIDER_CLASS_NAME,
                "sitekey": settings.CAPTCHA_SITE_KEY,
            }
        )
    return ctx
