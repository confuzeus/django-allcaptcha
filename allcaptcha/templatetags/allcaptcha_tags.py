from django import template
from allcaptcha import settings

register = template.Library()


@register.simple_tag
def get_sitekey():
    return settings.CAPTCHA_SITE_KEY


@register.simple_tag
def get_challenge_class():
    klass = ""
    if settings.PROVIDER == settings.HCAPTCHA_PROVIDER_NAME:
        klass = "h-captcha"
    return klass


@register.inclusion_tag("challenge.html")
def render_challenge() -> dict:
    ctx = {}
    if settings.PROVIDER == settings.HCAPTCHA_PROVIDER_NAME:
        ctx.update({"class_name": "h-captcha", "sitekey": settings.CAPTCHA_SITE_KEY})
    return ctx
