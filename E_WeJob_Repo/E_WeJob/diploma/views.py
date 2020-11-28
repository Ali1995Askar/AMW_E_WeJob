from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from utils.decorators import is_candidate, is_diploma_owner

# Create your views here.

from .models import Diploma
from .forms import DiplomaForm


@method_decorator(login_required(), name="dispatch")
@method_decorator(is_candidate, name="dispatch")
class DiplomaCreateView(generic.CreateView):
    model = Diploma
    form_class = DiplomaForm
    template_name = "diploma/diploma_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("user:redirect")


@method_decorator(login_required(), name="dispatch")
@method_decorator(is_candidate, name="dispatch")
@method_decorator(is_diploma_owner, name="dispatch")
class DiplomaUpdateView(generic.UpdateView):
    model = Diploma
    form_class = DiplomaForm
    template_name = "diploma/diploma_update.html"

    def get_success_url(self):
        return reverse("user:redirect")


@method_decorator(login_required(), name="dispatch")
@method_decorator(is_candidate, name="dispatch")
@method_decorator(is_diploma_owner, name="dispatch")
class DiplomaDeleteView(generic.DeleteView):
    model = Diploma

    def get_success_url(self):
        return reverse("user:redirect")


class DiplomaDetailView(generic.DetailView):
    model = Diploma


class DiplomaListView(generic.ListView):
    model = Diploma
