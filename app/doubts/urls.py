from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'doubts'

router = DefaultRouter()
router.register('doubts', views.DoubtViewSet)

urlpatterns = [
    path('', include(router.urls))
]
