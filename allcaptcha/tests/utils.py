from django import forms

from allcaptcha.mixins import CaptchaFormMixin


class ACaptchaedForm(CaptchaFormMixin, forms.Form):
    pass
