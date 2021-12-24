from django.core.exceptions import ValidationError
from django.forms import BaseForm
from django.utils.translation import gettext_lazy as _
from allcaptcha.utils import get_captcha_response, valid_response

from . import settings


class CaptchaFormMixin(BaseForm):
    def __init__(self, *args, **kwargs):
        super(CaptchaFormMixin, self).__init__(*args, **kwargs)
        self.captcha_response = get_captcha_response(self)

    def clean(self):
        is_valid = valid_response(self.captcha_response)
        if is_valid:
            return super(CaptchaFormMixin, self).clean()
        raise ValidationError(_("Anti spam verification failed. Please try again."))

    class Media:
        js = (settings.PROVIDER_JS, "allcaptcha/allcaptcha.min.js")
