from rest_framework import viewsets
from .serializers import NewsSerializer
from rest_framework.response import Response
from rest_framework import status


class NewsViewSet(viewsets.ModelViewSet):

    serializer_class = NewsSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    
    def list(self, request, pk = None):
        nows_serializer = self.serializer_class(self.get_queryset(pk), many = True)
        return Response(nows_serializer.data, status= status.HTTP_200_OK)

    def create(self, request):
        nows_serializer = self.serializer_class(data= request.data)
        if nows_serializer.is_valid():
            nows_serializer.save()
            return Response({
                'message': 'Nows created successfully'
            }, status= status.HTTP_200_OK)
        return Response(nows_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        nows = self.get_queryset(pk)
        if nows:
            nows_serializer = self.serializer_class(nows, data= request.data)
            if nows_serializer.is_valid():
                return Response({
                    'message':'Nows updated successfully'
                }, status= status.HTTP_200_OK)
            return Response(nows_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        return Response({
            'error':'Nows not found'
        }, status= status.HTTP_404_NOT_FOUND)


    def detroy(self, request, pk):
        nows = self.get_queryset(pk)
        if nows:
            nows.delete()
            return Response('Nows deleted successfully', status= status.HTTP_200_OK)
        return Response({
            'error': 'Nows not found'
        }, status = status.HTTP_404_NOT_FOUND)



    