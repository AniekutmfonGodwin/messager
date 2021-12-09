from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from utilities.helpers import BaseModelMixin
from utilities.types import MessageStatus
from django.contrib.auth import get_user_model


class Message(BaseModelMixin):
    sender = models.ForeignKey(get_user_model(), verbose_name=_("sender"),related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), verbose_name=_("receiver"),related_name="receiver", on_delete=models.CASCADE)
    body = models.TextField(_("body"))
    status = models.CharField(_("status"),choices=MessageStatus.choices(),default=MessageStatus.SEND.value, max_length=50)
    

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return f"from: {self.sender.email} to: {self.receiver.email}"

    # def get_absolute_url(self):
    #     return reverse("Message_detail", kwargs={"pk": self.pk})


