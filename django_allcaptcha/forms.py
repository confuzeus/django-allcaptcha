from django import forms

from allcaptcha.mixins import CaptchaFormMixin


class AForm(CaptchaFormMixin, forms.Form):
    name = forms.CharField()
