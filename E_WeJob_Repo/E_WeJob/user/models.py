from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    first_name = None
    last_name = None

    COMPANY = "Company"
    CANDIDATE = "Candidate"

    USER_TYPES = (
        (CANDIDATE, "Candidate"),
        (COMPANY, _("Company")),
    )

    user_type = models.CharField(
        _("User type"), max_length=15, choices=USER_TYPES, default="", blank=True
    )

    class Meta(AbstractUser.Meta):
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def is_company(self):
        return self.user_type == self.COMPANY

    @property
    def is_candidate(self):
        return self.user_type == self.CANDIDATE

    @property
    def profile(self):
        if self.is_company:
            return self.company_profile
        if self.is_candidate:
            return self.candidate_profile

    @property
    def type(self):
        return self.user_type


class CompanyProfile(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name=_("company"),
        related_name="company_profile",
        on_delete=models.CASCADE,
    )
    cName = models.CharField(_("Company Name"), max_length=25, blank=True)
    tel = models.CharField(_("telephone"), max_length=25, blank=True)

    def __str__(self):
        return self.cName


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name=_("candidate"),
        related_name="candidate_profile",
        on_delete=models.CASCADE,
    )
    fullName = models.CharField(_("full Name"), max_length=25, blank=True)
    tel = models.CharField(_("telephone"), max_length=25, blank=True)
    experienceYears = models.IntegerField(_("experience Years"))

    def __str__(self):
        return self.fullName


class Message(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        related_name="messages",
        on_delete=models.CASCADE,
    )
    subject = models.CharField(verbose_name="subject", max_length=255)
    message = models.TextField(
        verbose_name="description",
    )
    date = models.DateTimeField(auto_now_add=True)