from django.contrib import admin

from .models import Diploma
from .forms import DiplomaForm

# Register your models here.


class CustomDiplomaAdmin(admin.ModelAdmin):

    form = DiplomaForm
    # ordering = ("requiredEducationLevel",)
    list_display = (
        "user",
        "diplomaTitle",
    )
    list_display_links = (
        "user",
        "diplomaTitle",
    )
    list_filter = (
        "user",
        "diplomaTitle",
    )
    search_fields = (
        "user",
        "diplomaTitle",
    )


# Register your models here.

admin.site.register(Diploma, CustomDiplomaAdmin)
