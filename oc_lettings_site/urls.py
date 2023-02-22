from django.contrib import admin
from django.urls import path, include
import oc_lettings_site.views


urlpatterns = [
    path('', oc_lettings_site.views.index, name='index'),
    path('profiles/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    path('profiles/', include(('profiles.urls', 'profiles'), namespace='profile')),
    path('lettings/', include(('lettings.urls', 'lettings'), namespace='lettings')),
    path('lettings/', include(('lettings.urls', 'lettings'), namespace='letting')),
    path('admin/', admin.site.urls),
]
