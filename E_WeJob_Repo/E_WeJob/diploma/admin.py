from django.contrib import admin

from .models import Diploma
from .forms import DiplomaForm

# Register your models here.


class CustomDiplomaAdmin(admin.ModelAdmin):

    form = DiplomaForm
    # ordering = ("requiredEducationLevel",)
    list_display = (
        "candidate",
        "diplomaTitle",
    )
    list_display_links = (
        "candidate",
        "diplomaTitle",
    )
    list_filter = (
        "candidate",
        "diplomaTitle",
    )
    search_fields = (
        "candidate",
        "diplomaTitle",
    )


# Register your models here.

admin.site.register(Diploma, CustomDiplomaAdmin)
