Installation
============

First, install the package using pip::

    pip install django-allcaptcha


Then, add ``allcaptcha`` to your Django ``INSTALLED_APPS`` list.

django-allcaptcha ships with Javascript. You need to run ``collectstatic`` when deploying to production.

By default, Hcaptcha will be used.

Set ``CAPTCHA_PROVIDER`` in your settings to override this.

For Hcaptcha, set your keys::

    HCAPTCHA_SECRET_KEY
    HCAPTCHA_SITE_KEY

For Recaptcha V2::

    RECAPTCHA_V2_SECRET_KEY
    RECAPTCHA_V2_SITE_KEY

And Recaptcha V3::

    RECAPTCHA_V3_SECRET_KEY
    RECAPTCHA_V3_SITE_KEY

For all available options, see :doc:`settings`
