from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from utilities.helpers import generate_id
from utilities.types import MessageStatus
from django.contrib.auth import get_user_model



class BaseModelMixin(models.Model):
    id = models.IntegerField(primary_key=True, default=generate_id, editable=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(_("active"),default=True)


    class Meta:
        abstract = True




class Message(BaseModelMixin):
    sender = models.ForeignKey(get_user_model(), verbose_name=_("sender"),related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), verbose_name=_("receiver"),related_name="receiver", on_delete=models.CASCADE)
    body = models.TextField(_("body"))
    room = models.CharField(_("room"), max_length=50,blank=True,null=True)
    status = models.CharField(_("status"),choices=MessageStatus.choices(),default=MessageStatus.SEND.value, max_length=50)
    

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return f"from: {self.sender.email} to: {self.receiver.email}"
    
    def read(self):
        self.__dict__.update(status=MessageStatus.READ.value)
        self.save()
        return self

    # def get_absolute_url(self):
    #     return reverse("Message_detail", kwargs={"pk": self.pk})


