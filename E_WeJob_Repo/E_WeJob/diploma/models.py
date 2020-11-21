from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# Create your models here.

User = get_user_model()


class Diploma(models.Model):

    candidate = models.ForeignKey(
        User,
        verbose_name=_("candidate"),
        related_name="diploma",
        on_delete=models.CASCADE,
    )

    diplomaTitle = models.CharField(
        _("Diploma Title"),
        max_length=255,
    )

    def __str__(self):
        return self.diplomaTitle
