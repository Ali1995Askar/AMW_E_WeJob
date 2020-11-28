from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import CompanyProfile, CandidateProfile, Message

from django.contrib.auth.admin import UserAdmin
from .forms import (
    UserCreationForm,
    UserChangeForm,
    CompanyProfileForm,
    CandidateProfileForm,
    MessageForm,
)


User = get_user_model()


admin.site.register(CompanyProfile)
admin.site.register(CandidateProfile)


class Company(admin.StackedInline):
    model = CompanyProfile
    can_delete = False
    verbose_name_plural = "Company Profiles"
    fk_name = "user"
    list_display = ("cName",)
    form = CompanyProfileForm


class Candidate(admin.StackedInline):
    model = CandidateProfile
    can_delete = False
    verbose_name_plural = "Candidate Profiles"
    fk_name = "user"
    list_display = ("fullName",)
    form = CandidateProfileForm


class CustomMessageAdmin(admin.ModelAdmin):
    def save_model(self, request, message, form, change):
        message.user = request.user
        message.save()

    form = MessageForm
    ordering = ("date",)
    list_display = (
        "user",
        "subject",
        "date",
    )
    list_display_links = (
        "user",
        "subject",
    )
    list_filter = (
        "user",
        "date",
    )
    search_fields = (
        "user",
        "subject",
    )


class CustomUserAdmin(UserAdmin):
    def Name(self, user):

        profile = user.profile

        if profile is None:
            return "Admin"
        elif user.is_company:
            return profile.cName
        elif user.is_candidate:
            return profile.fullName

    readonly_fields = ("user_type",)
    list_display = (
        "Name",
        "user_type",
    )
    list_display_links = ("Name",)
    list_filter = (
        "user_type",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "CompanyProfile__cName",
        "CandidateProfile__fullName",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "user_type",
                )
            },
        ),
    )

    def get_inline_instances(self, request, obj=None):

        if not obj:
            return list()

        if obj.is_company:
            self.inlines = (Company,)

        if obj.is_candidate:
            self.inlines = (Candidate,)

        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Message, CustomMessageAdmin)
