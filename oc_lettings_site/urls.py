from django.contrib import admin
from django.urls import path

import lettings.views
import oc_lettings_site.views

urlpatterns = [
    path('', oc_lettings_site.views.index, name='index'),
    path('lettings/', lettings.views.lettings_index, name='lettings_index'),
    path('lettings/<int:letting_id>/', lettings.views.letting, name='letting'),
    path('profiles/', oc_lettings_site.views.profiles_index, name='profiles_index'),
    path('profiles/<str:username>/', oc_lettings_site.views.profile, name='profile'),
    path('admin/', admin.site.urls),
]
