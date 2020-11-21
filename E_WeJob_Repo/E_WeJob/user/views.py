# Create your views here.
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    DetailView,
)
from .forms import (
    UserCreationForm,
    CompanyProfileForm,
    CandidateProfileForm,
    MessageForm,
)
from .models import CompanyProfile, CandidateProfile, Message

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "pk"
    slug_url_kwarg = "pk"


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["username", "email"]

    def get_success_url(self):
        return reverse("user:detail", kwargs={"pk": self.request.user.pk})

    def get_object(self):
        return User.objects.get(id=self.request.user.pk)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Info successfully updated")
        )
        return super().form_valid(form)


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("user:detail", kwargs={"pk": self.request.user.pk})


class CompanyCreationView(CreateView):
    template_name = "registration/company_sign_up.html"
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse("user:detail", kwargs={"pk": self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super(CompanyCreationView, self).get_context_data(**kwargs)
        context["company_profile_form"] = CompanyProfileForm
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_type = User.COMPANY
        self.object.save()
        profile = CompanyProfile.objects.create(
            user=self.object,
            cName=self.request.POST.get("cName"),
            tel=self.request.POST.get("tel"),
        )
        profile.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class CandidateCreationView(CreateView):
    template_name = "registration/candidate_sign_up.html"
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse("user:detail", kwargs={"pk": self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super(CandidateCreationView, self).get_context_data(**kwargs)
        context["candidate_profile_form"] = CandidateProfileForm

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_type = User.CANDIDATE
        self.object.save()

        profile = CandidateProfile.objects.create(
            user=self.object,
            fullName=self.request.POST.get("fullName"),
            tel=self.request.POST.get("tel"),
            experienceYears=self.request.POST.get("experienceYears"),
        )

        profile.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class UserContactView(LoginRequiredMixin, CreateView):
    login_required = True
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse("index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())