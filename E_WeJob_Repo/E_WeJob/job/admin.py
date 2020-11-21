from django.contrib import admin

from .models import Job
from .forms import JobForm

# Register your models here.
# admin.site.register(Job)


class CustomJobAdmin(admin.ModelAdmin):

    form = JobForm
    ordering = ("date",)
    list_display = (
        "company",
        "requiredEducationLevel",
        "title",
        "requiredExperienceYears",
        "salary",
        "date",
    )
    list_display_links = (
        "company",
        "title",
        "date",
    )
    list_filter = (
        "company",
        "requiredEducationLevel",
        "requiredExperienceYears",
    )
    search_fields = (
        "company",
        "requiredEducationLevel",
        "requiredExperienceYears",
    )


# Register your models here.


admin.site.register(Job, CustomJobAdmin)
