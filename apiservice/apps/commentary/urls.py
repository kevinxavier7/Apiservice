from django.urls import path
from .views import InsertCommentaryAPIView

urlpatterns = [ 
    path('insert-commentary/<int:pk>/', InsertCommentaryAPIView.as_view(), name= 'insert-commentary')
]