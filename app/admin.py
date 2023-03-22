from asgiref.sync import async_to_sync
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .bot.inline_keyboards.user_buttons import send_message_to_client
from .inlines import BatchInline, HabitsInline
from .models import Batch, Client, Habit


@admin.register(Client)
class UserAdmin(admin.ModelAdmin):
    inlines = (HabitsInline, BatchInline)
    list_display = (
        "user_id",
        "login",
        "full_name",
        "paid",
        "approve_notified",
        "joined",
    )
    actions = ["send_approve_message"]

    def send_approve_message(self, request, queryset):
        for q in queryset:
            async_to_sync(send_message_to_client)(q.user_id)
            client = Client.objects.get(user_id=q.user_id)
            client.approve_notified = True
            client.save()

    send_approve_message.short_description = _("Send Approve Message to Bot")


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("batch_name", "start_date", "end_date", "is_finished")


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("habit_title", "habit_score")
