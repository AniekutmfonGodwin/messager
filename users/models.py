from typing import Union
from django.db import models
# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from utilities.helpers import generate_id
from django.contrib.auth import get_user_model




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


    
    def generate_room(self,id:Union[int,str],*args, **kwargs):
        if type(id) == str:
            id = int(id)
        return "".join([str(n) for n in sorted([self.id,id])])


    def get_receiver(self,room:str,*args, **kwargs):
        receiver_id_str = room.replace(str(self.id),'')
        receiver_id = int(room.replace(str(self.id),'')) if receiver_id_str else self.id
        return get_user_model().objects.get(id=receiver_id)
        
        