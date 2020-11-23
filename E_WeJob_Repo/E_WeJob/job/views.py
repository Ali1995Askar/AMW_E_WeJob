from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
from utils.decorators import is_company, is_job_owner
from .models import Job
from .forms import JobForm
from user.models import User
from diploma.models import Diploma


@method_decorator(login_required(), name="dispatch")
@method_decorator(is_company, name="dispatch")
class JobCreateView(generic.CreateView):
    model = Job
    form_class = JobForm
    template_name = "job/job_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("job:detail", kwargs={"pk": self.object.pk})


@method_decorator(login_required(), name="dispatch")
@method_decorator(is_company, name="dispatch")
@method_decorator(is_job_owner, name="dispatch")
class JobUpdateView(generic.UpdateView):
    model = Job
    form_class = JobForm
    template_name = "job/job_update.html"

    def get_success_url(self):
        return reverse("job:detail", kwargs={"pk": self.get_object().pk})


@method_decorator(login_required(), name="dispatch")
@method_decorator(is_company, name="dispatch")
@method_decorator(is_job_owner, name="dispatch")
class JobDeleteView(generic.DeleteView):
    model = Job

    def get_success_url(self):
        return reverse("job:all")


class JobDetailView(generic.DetailView):
    model = Job

    def get_suitable_users(self, **kwargs):
        instance = self.get_object()
        requiredEducationLevel = instance.requiredEducationLevel
        requiredExperienceYears = instance.requiredExperienceYears
        users = User.objects.filter(user_type=User.CANDIDATE)
        suitable_users = []

        for user in list(users):
            if user.profile.experienceYears >= requiredExperienceYears:
                diplomas = user.diplomas.filter(
                    diplomaTitle=requiredEducationLevel.diplomaTitle
                )
                print(user, diplomas)
                if diplomas:
                    suitable_users += [user]
        return suitable_users

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context["suitable_users"] = self.get_suitable_users()
        # print(self.get_suitable_users())

        return context


class JobListView(generic.ListView):
    model = Job


class MyJobView(generic.ListView):
    model = Job
    template_name = "job/job_dashborad.html"

    def get_queryset(self):
        queryset = super(MyJobView, self).get_queryset()
        queryset = queryset.filter(company=self.request.user)
        return queryset
