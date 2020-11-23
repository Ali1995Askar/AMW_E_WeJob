from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# Create your models here.

User = get_user_model()


class Diploma(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        related_name="diplomas",
        related_query_name="diplomas",
        on_delete=models.CASCADE,
    )

    diplomaTitle = models.CharField(
        _("Diploma Title"),
        max_length=255,
    )

    def __str__(self):
        return self.diplomaTitle
