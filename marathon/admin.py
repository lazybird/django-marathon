from django.contrib import admin

from marathon.models import Lock


@admin.register(Lock)
class LockAdmin(admin.ModelAdmin):
    list_display = ("name", "locked_at")
