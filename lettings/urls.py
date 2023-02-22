from django.urls import path
import lettings.views


urlpatterns = [
    path('', lettings.views.index, name='index'),
    path('<int:letting_id>/', lettings.views.letting, name='letting'),
]
