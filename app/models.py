from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    user_id = models.PositiveIntegerField(
        _("user_id"), unique=True, blank=True, null=True
    )
    full_name = models.CharField(_("full_name"), max_length=128, blank=True, null=True)
    login = models.CharField(_("login"), max_length=128, blank=True, null=True)
    paid = models.BooleanField(_("paid"), default=False)
    approve_notified = models.BooleanField(_("approve_notified"), default=False)
    invoice_image = models.ImageField(
        _("invoice_image"), blank=True, upload_to=f"documents/invoices/{user_id}"
    )
    joined = models.DateTimeField(_("joined"), auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        verbose_name = _("client")
        verbose_name_plural = _("clients")


class Batch(models.Model):
    batch_name = models.CharField(
        _("batch_name"), max_length=128, blank=True, null=True
    )
    start_date = models.DateTimeField(_("start_date"), blank=True, null=True)
    end_date = models.DateTimeField(_("end_date"), blank=True, null=True)
    is_finished = models.BooleanField(_("is_finished"), blank=True, null=True)
    user = models.ForeignKey(
        Client, verbose_name="users", on_delete=models.CASCADE, related_name="batch"
    )

    def __str__(self):
        return f"{self.batch_name}"

    class Meta:
        verbose_name = _("batch")
        verbose_name_plural = _("batches")


class Habit(models.Model):
    habit_title = models.CharField(
        _("habit_title"), max_length=512, blank=True, null=True
    )
    habit_score = models.IntegerField(_("habit_score"), blank=True, null=True)
    user = models.ForeignKey(
        Client, verbose_name="users", on_delete=models.CASCADE, related_name="habit"
    )

    def __str__(self):
        return f"{self.habit_title}"

    class Meta:
        verbose_name = _("habit")
        verbose_name_plural = _("habits")
