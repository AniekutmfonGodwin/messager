from django.db import models
# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from utilities.helpers import generate_id





class CustomUser(AbstractUser):
    USERNAME_FIELD = "email"   # e.g: "username", "email"
    EMAIL_FIELD = "email"         # e.g: "email", "primary_email"
    REQUIRED_FIELDS = ["username"]

    
    id = models.IntegerField(primary_key = True,unique=True,editable=False,default=generate_id) 
    email = models.EmailField(_("email"),blank=False, max_length=80,unique=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    


    def __str__(self):
        return self.email or "__none__"


    
    def generate_room(self,id:int,*args, **kwargs):
        return "".join([str(n) for n in sorted([self.id,id])])
        