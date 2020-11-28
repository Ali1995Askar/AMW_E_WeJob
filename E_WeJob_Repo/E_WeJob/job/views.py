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
from rest_framework import filters
import django_filters.rest_framework
from rest_framework import viewsets
from job.api.serializers import JobSerializer
from rest_framework import permissions, renderers, viewsets
from job.api.filters import JobFilter


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


@method_decorator(login_required(), name="dispatch")
@method_decorator(is_company, name="dispatch")
@method_decorator(is_job_owner, name="dispatch")
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

        return context


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumber(PageNumberPagination):
    page_size = 4

    def get_paginated_response(self, data):
        return Response(
            {
                "current_page": self.page,
                # "range": self.page,
                "count": len(data),
                # "countItemsOnPage": self.page_size,
                # "lastPage": self.page.paginator.num_pages,
                "current": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class JobListView(viewsets.ReadOnlyModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = JobFilter
    ordering_fields = ["requiredExperienceYears", "salary"]
    template_name = "job/job_list.html"
    pagination_class = CustomPageNumber


@method_decorator(login_required(), name="dispatch")
@method_decorator(is_company, name="dispatch")
class MyJobView(generic.ListView):
    model = Job
    template_name = "job/job_dashborad.html"

    def get_queryset(self):
        queryset = super(MyJobView, self).get_queryset()
        queryset = queryset.filter(company=self.request.user)
        return queryset
