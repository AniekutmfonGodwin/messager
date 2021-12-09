from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _

def generate_id(length:int=10):
    return int(str(uuid4().int)[:length])




class BaseModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=generate_id, editable=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(_("active"),default=True)