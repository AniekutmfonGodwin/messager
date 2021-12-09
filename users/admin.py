from django.contrib import admin
from users import models

@admin.register(models.CustomUser)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
    )



    search_fields = (
        "email",
    )