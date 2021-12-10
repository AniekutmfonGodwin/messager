from rest_framework.response import Response
# from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework import generics
from chat import models
from users.models import CustomUser
from  django_filters import rest_framework
from rest_framework import filters



class MessageDetailSerialzer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Message
        fields = (
            "id",
            "body",
            "status",
            "updated_at",
            "created_at",
        ) 

        read_only_fields = (
            "id",
            "body",
            "updated_at",
            "created_at",
        )




class MessageListSerialzer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Message
        fields = (
            "id",
            "body",
            "sender",
            "receiver",
            "status",
            "updated_at",
            "created_at",
        ) 

    






class ChatDetailView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]


    def get_object(self):
        
        return get_object_or_404(
            models.Message,
            id = self.kwargs.get("id"),
            reveiver=self.request.user,
            active=True
            )
        
        

    def get_serializer_class(self):
        return MessageDetailSerialzer



    

    def put(self,request,*args, **kwargs):
        
        serializer = self.get_serializer_class()(data=request.data)

        message:models.Message = self.get_object()
        
        
        if serializer.is_valid():
            
            message.__dict__.update(**serializer.validated_data)
            message.save()
            return Response(self.get_serializer_class()(message).data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        
    def patch(self,request,*args,**kwargs):
        return self.put(request,*args,**kwargs)



class ChatListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]

    filterset_fields = {
        "sender":["exact"],
        "receiver":["exact"],
        "status":["exact","icontains","startswith"],
        "created_at":["exact","year__gt","year__lt","year__gte","month__lte","month__gt","month__lt","month__gte","month__lte","day__gt","day__lt","day__gte","day__lte"],
        "updated_at":["exact","year__gt","year__lt","year__gte","month__lte","month__gt","month__lt","month__gte","month__lte","day__gt","day__lt","day__gte","day__lte"]
    }

  
    ordering = ['created_at']

        

    def get_queryset(self):
        return models.Message.objects.filter(
                room__icontains=str(self.request.user.id),
                active=True
            )
        
    

    def get_serializer_class(self):
        return MessageListSerialzer




