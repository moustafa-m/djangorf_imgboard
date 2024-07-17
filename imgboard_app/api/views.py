from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from imgboard_app import models
from . import serializers, permissions

# ----> Posts
class PostList(generics.ListAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]

class PostCreate(generics.CreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated, permissions.ObjUserOrReadOnly | permissions.AdminOrReadOnly]
    
    def update(self, request, pk):
        post = get_object_or_404(models.Post, pk=pk)
        post.image = request.FILES['image']
        self.check_object_permissions(request, post)
        serializer = serializers.PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status.HTTP_200_OK)
# <---- Posts