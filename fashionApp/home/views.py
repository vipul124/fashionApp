from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from .models import User, Store, Product, Variant, Music, Video
from .serializers import UserSerializer, StoreSerializer, ProductSerializer, VariantSerializer, MusicSerializer, VideoSerializer, ViewVideoSerializer, ViewProductSerializer
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator


## A. API for retrieving all the videos in JSON format [ with Pagination + Caching + Database Optimization ]
# 1a. Pagination format 
class ImplementPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 100
    ordering = 'created_at'

    # Custom format for pagination as mentioned in the task
    def get_paginated_response(self, data):
        return Response({
            "videos": data,
            "pagination": {
                "page": self.page.number,
                "limit": self.get_page_size(self.request),
                "total_pages": self.page.paginator.num_pages,
                "total_videos": self.page.paginator.count,
                "previous_cursor": self.get_previous_link(),
                "next_cursor": self.get_next_link(),
            }
        })

# 1b. API for retrieving all the videos in JSON format - GET /api/getAllVideos/
class GetVideoList(generics.ListAPIView):
    # Database Optimization - I don't have much idea about this thing but googled and found out that this is one of the ways to optimize the database queries
    queryset = Video.objects.all().select_related('user', 'music').prefetch_related('products__variants', 'products__store')
    serializer_class = ViewVideoSerializer

    # Pagination
    pagination_class = ImplementPagination

    # Caching
    @method_decorator(cache_page(5 * 60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

## B. APIs for creating new entries in the database (just dummy ones for testing purposes for now, can implement authentication and better endpoints later)    
# 1. new user - POST /api/user/
class CreateUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. new store - POST /api/store/
class CreateStore(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3. new product - POST /api/product/
class CreateProduct(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 4. new song (was thinking to integrate with the video thing itself as done with varient but if you want to create something kindoff INSTAGRAM REELS for FASHION thing, a seperate API must be a better idea)
# - POST /api/music/
class CreateMusic(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 5. new video - POST /api/video/
class CreateVideo(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)