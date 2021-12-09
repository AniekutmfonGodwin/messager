from django.urls import path
from chat import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('message/<int:id>/', csrf_exempt(views.ChatDetailView.as_view())),
    path('message/', csrf_exempt(views.ChatListView.as_view())),
]
