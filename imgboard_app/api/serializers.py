from rest_framework import serializers
from imgboard_app import models

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = models.Post
        fields = '__all__'
