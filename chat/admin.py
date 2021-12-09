from django.contrib import admin
from chat import models

# Register your models here.
from chat import models
@admin.register(models.Message)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "receiver",
        "status",
        "created_at",
        "updated_at",
        "active"
    )

    ordering = (
        "-created_at",
        "-updated_at",
    )

    search_fields = (
        "sender__email",
        "receiver__email",
        "status"
    )
