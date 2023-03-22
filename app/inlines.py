from django.contrib import admin

from .models import Batch, Habit


class BatchInline(admin.StackedInline):
    extra = 0
    model = Batch

    fields = ("batch_name", "start_date", "end_date", "is_finished")


class HabitsInline(admin.StackedInline):
    extra = 0
    model = Habit

    fields = (
        "habit_title",
        "habit_score",
    )
