from django.urls import path
from .views import RegisterView, PhotoListView, CustomAuthToken, PhotoCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('photos/create/', PhotoCreateView.as_view(), name='photo-create'),
    path('photos/', PhotoListView.as_view(), name='photo-list-create'),
]
