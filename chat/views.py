from rest_framework.response import Response
# from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework import generics
from chat import models



class MessageWriteSerialzer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Message
        fields = (
            "status",
        ) 





class ChatDetailView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]


    def get_object(self):
        
        return get_object_or_404(
            models.Message,
            id = self.kwargs.get("id"),
            receiver=self.request.user
            )
        
        

    def get_serializer_class(self):
        return MessageWriteSerialzer





    def put(self,request,*args, **kwargs):
        
        serializer = self.get_serializer_class(data=request.data)

        message:models.Message = self.get_object()
        
        
        if serializer.is_valid():
            
            message.__dict__.update(**serializer.validated_data)
            message.save()
            return Response(self.get_serializer_class(message).data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        
    def patch(self,request,*args,**kwargs):
        return self.put(request,*args,**kwargs)
        
    


