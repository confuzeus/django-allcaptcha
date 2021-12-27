Settings
========

django-allcaptcha comes with several settings.

Some come with sane defaults while others need to be set manually.

**PROVIDER**

    **Type:** str

    **Default:** hcaptcha

    The provider to activate.

    Can be one of the following:

    - hcaptcha
    - recaptcha

HCaptcha specific settings
--------------------------

**HCAPTCHA_URL**

    **Type:** str

    **Default:** https://hcaptcha.com/siteverify

    The URL where HCaptcha challenge tokens will be sent for verification.

**HCAPTCHA_SECRET_KEY**

    **Type:** str

    **Default:** None

    Your secret key.

**HCAPTCHA_SITE_KEY**

    **Type:** str

    **Default:** None

    Your site key.

**HCAPTCHA_JS**

    **Type:** str

    **Default**: https://js.hcaptcha.com/1/api.js

    The Javascript file containing HCaptcha APIs.

**HCAPTCHA_JS_CALLBACK**

    **Type:** str

    **Default:** onHcaptchaSubmit

    The callback function to execute after the user completes the invisible challenge.


Recaptcha specific settings
---------------------------

***RECAPTCHA_URL**

    **Type:** str

    **Default:** https://www.google.com/recaptcha/api/siteverify

    The URL where ReCaptcha challenge tokens will be sent for verification.

**RECAPTCHA_V2_SECRET_KEY**

    **Type:** str

    **Default:** None

    Your V2 secret key.

**RECAPTCHA_V2_SITE_KEY**

    **Type:** str

    **Default:** None

    Your V2 site key.

**RECAPTCHA_V3_SECRET_KEY**

    **Type:** str

    **Default:** None

    Your V3 secret key.

**RECAPTCHA_V3_SITE_KEY**

    **Type:** str

    **Default:** None

    Your V3 site key.

**RECAPTCHA_JS**

    **Type:** str
    **Default:** https://www.google.com/recaptcha/api.js

    The Javascript file containing Recaptcha APIs.

** RECAPTCHA_JS_CALLBACK**

    **Type:** str

    **Default:** onRecaptchaSubmit

    The callback function to execute after the user completes the invisible or V3 challenge.

**RECAPTCHA_VERSION**

    **Type**: int

    **Default**: 2

    The version of Recaptcha to use.

**RECAPTCHA_MIN_SCORE**

    **Type**: float

    **Default:** 0.6

    The minimum score for a Recaptcha V3 challenge to be considered successful.
