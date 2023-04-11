from django.contrib import admin
from django.urls import path, include
import oc_lettings_site.views


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('', oc_lettings_site.views.index, name='index'),
    path('profiles/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    path('profiles/', include(('profiles.urls', 'profiles'), namespace='profile')),
    path('lettings/', include(('lettings.urls', 'lettings'), namespace='lettings')),
    path('lettings/', include(('lettings.urls', 'lettings'), namespace='letting')),
    path('admin/', admin.site.urls),
]
