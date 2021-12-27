Tutorial
========

Learn how to quickly setup allcaptcha in your Django templates.

First, you need to a ``Form`` that inherits from ``CaptchaFormMixin``::

    from django import forms
    from allcaptcha.mixins import CaptchaFormMixin

    class MySecureForm(CaptchaFormMixin, forms.Form)
        email = forms.EmailField()


Then, you're simply going to instantiate and include the form
instance in your template context as usual.

In your template, you need to make sure you include the bundled Javascript
like so::

    {{ form.media.js }}

You should preferably include this right before the closing ``body`` tag after
all other HTML elements have been rendered.

In your ``form`` tag, you need to render the Captcha challenge::

        {% load allcaptcha_tags %}

        <form method="post" action=".">
            {% csrf_token %}
            {{ form }}
            {% render_challenge %}
            <button type="submit">Send</button>
        </form>

The ``render_challenge`` template tag will render a visible Hcaptcha or
Recapptcha V2 challenge by default.

If you want to render an invisible challenge instead, do this::

        {% load allcaptcha_tags %}

        <form method="post" action=".">
            {% csrf_token %}
            {{ form }}
            {% render_challenge "invisible" "Submit" %}
        </form>

This will render a button that will trigger the invisible challenge on click.

The text on this button will read *Submit*.

Manual validation
-----------------

Instead of using the ``CaptchaFormMixin``, you can manually validate any
challenge response by calling the ``valid_response`` function::

    from allcaptcha.utils import valid_response

    success = valid_response("my-challenge-response")

This function will return either True or False depending on whether the
response was valid or not.

Manual rendering
----------------

The steps above will allow to quickly integrate captcha into any ``Form``.

However, you might want to manually render your challenges and call your
own Javascript functions upon challenge completion.

In that case, take a look at the :doc:`template-tags` reference to see
all the available templates that will allow you to render your own HTML
elements to trigger challenges.
