from rest_framework import routers
from .api import NewsViewSet

routerNows = routers.SimpleRouter()
routerNows.register('news', NewsViewSet, basename= 'news')


