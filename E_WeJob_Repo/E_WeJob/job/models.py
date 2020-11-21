from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from diploma.models import Diploma


# Create your models here.

User = get_user_model()


class Job(models.Model):
    company = models.ForeignKey(
        User,
        verbose_name=_("company"),
        related_name="company",
        on_delete=models.CASCADE,
    )

    requiredEducationLevel = models.ForeignKey(
        Diploma,
        verbose_name=_("diploma"),
        related_name="requiredEducationLevel",
        on_delete=models.SET_NULL,
        null=True,
    )

    title = models.CharField(
        _("Job Title"),
        max_length=255,
    )
    requiredExperienceYears = models.IntegerField(_(" required experience years"))
    salary = models.IntegerField(_("salary"))

    def __str__(self):
        return str(self.title) + " by " + str(self.company)
