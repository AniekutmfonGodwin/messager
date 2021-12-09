from django.urls import path
from chat import views



urlpatterns = [
    path('<int:id>/', views.ChatDetailView.as_view),
]
