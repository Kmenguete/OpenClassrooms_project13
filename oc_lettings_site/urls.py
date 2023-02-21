from django.contrib import admin
from django.urls import path

import lettings.views
import profiles.views
import oc_lettings_site.views

urlpatterns = [
    path('', oc_lettings_site.views.index, name='index'),
    path('lettings/', lettings.views.index, name='lettings_index'),
    path('lettings/<int:letting_id>/', lettings.views.letting, name='letting'),
    path('profiles/', profiles.views.index, name='profiles_index'),
    path('profiles/<str:username>/', profiles.views.profile, name='profile'),
    path('admin/', admin.site.urls),
]
