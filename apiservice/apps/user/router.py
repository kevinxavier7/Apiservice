from rest_framework import routers
from .api import UserApiViewSet


router = routers.SimpleRouter()
router.register('user', UserApiViewSet, basename= 'user')