from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseForbidden
from job.models import Job
from diploma.models import Diploma


def is_company(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if request.user.is_company or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
            # return HttpResponseForbidden("fsdfs")

    return wrap


def is_candidate(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if request.user.is_candidate or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


# from django.contrib.auth.decorators import user_passes_test

# is_company = user_passes_test(lambda user: user.is_company)
# is_candidate = user_passes_test(lambda user: user.is_candidate)


def is_job_owner(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        _job = Job.objects.get(pk=kwargs["pk"])
        if _job.company == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def is_diploma_owner(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        _diploma = Diploma.objects.get(pk=kwargs["pk"])
        if _diploma.candidate == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap