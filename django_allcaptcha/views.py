from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from django_allcaptcha.forms import AForm


def form_view(request):
    form = None
    ctx = {}
    if request.method == "POST":
        form = AForm(request.POST)

        if form.is_valid():
            messages.success(request, "Form was valid!")
            return redirect("/")

        messages.error(request, "Form was invalid!")

    if form is None:
        form = AForm()
    ctx.update({"form": form})
    return TemplateResponse(request, "form.html", ctx)
