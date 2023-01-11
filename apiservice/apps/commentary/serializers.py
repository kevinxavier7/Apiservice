from rest_framework import serializers
from apiservice.apps.news.models import News

class InsertCommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('commentary',)