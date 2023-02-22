from django.urls import path
import profiles.views


urlpatterns = [
    path('', profiles.views.index, name='index'),
    path('<str:username>/', profiles.views.profile, name='profile'),
]
