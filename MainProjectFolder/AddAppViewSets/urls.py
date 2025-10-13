
from django.urls import path
from . import views

# # MWANZO IN ORDER TO USE MODEL VIEW SET
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('AllMyUser', views.AllMyUserViewSet)
router.register('AllVituoVyote', views.AllVituoVyoteViewSet)
router.register('AllAinaZaMarejesho', views.AllAinaZaMarejeshoViewSet)



urlpatterns = router.urls