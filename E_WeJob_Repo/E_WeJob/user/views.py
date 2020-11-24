# Create your views here.
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.views import generic
from django.utils.decorators import method_decorator

from utils.decorators import is_candidate
from . import forms
from .models import CompanyProfile, CandidateProfile, Message
from job.models import Job

User = get_user_model()


@method_decorator(is_candidate, name="dispatch")
class UserDetailView(LoginRequiredMixin, generic.DetailView):

    model = User
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get_suitable_jobs(self, **kwargs):
        instance = self.get_object()
        EducationLevel = instance.diplomas.all()
        ExperienceYears = instance.profile.experienceYears
        jobs = Job.objects.all()
        suitable_jobs = []

        for job in list(jobs):
            if job.requiredExperienceYears <= ExperienceYears:
                diplomas = instance.diplomas.filter(
                    diplomaTitle=job.requiredEducationLevel
                )

                if diplomas:
                    suitable_jobs += [job]
        return suitable_jobs

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)

        context["suitable_jobs"] = self.get_suitable_jobs()
        return context


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):

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


class UserRedirectView(LoginRequiredMixin, generic.RedirectView):

    permanent = False

    def get_redirect_url(self):
        if self.request.user.is_candidate:
            return reverse("user:detail", kwargs={"pk": self.request.user.pk})
        if self.request.user.is_company:
            return reverse(
                "job:my-jobs", kwargs={"username": self.request.user.username}
            )
        if self.request.user.is_superuser:
            return reverse("admin:index")


class CompanyCreationView(generic.CreateView):
    template_name = "registration/company_sign_up.html"
    form_class = forms.UserCreationForm

    def get_success_url(self):
        return reverse("job:my-jobs", kwargs={"username": self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super(CompanyCreationView, self).get_context_data(**kwargs)
        context["company_profile_form"] = forms.CompanyProfileForm
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


class CandidateCreationView(generic.CreateView):
    template_name = "registration/candidate_sign_up.html"
    form_class = forms.UserCreationForm

    def get_success_url(self):
        return reverse("user:detail", kwargs={"pk": self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super(CandidateCreationView, self).get_context_data(**kwargs)
        context["candidate_profile_form"] = forms.CandidateProfileForm

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


class UserContactView(LoginRequiredMixin, generic.CreateView):
    login_required = True
    model = Message
    form_class = forms.MessageForm

    def get_success_url(self):
        return reverse("index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())