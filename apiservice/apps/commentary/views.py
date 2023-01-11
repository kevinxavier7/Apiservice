from rest_framework.views import APIView
from apiservice.apps.news.models import News
from rest_framework.response import Response
from rest_framework import status
from .serializers import InsertCommentarySerializer

class  InsertCommentaryAPIView(APIView):

    def post(self, request, pk):
        
        nows_id = News.objects.filter(id = pk).first()
        if nows_id:
            serializer = InsertCommentarySerializer(data= request.data)
            if serializer.is_valid():
                News.objects.filter(id = pk).update(commentary = request.data['commentary'])
                return Response({
                    'message': 'comment inserted successfully'
                }, status= status.HTTP_200_OK)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        return Response({
            'error': 'this news does not exist'
        }, status= status.HTTP_404_NOT_FOUND)


        






