from django.urls import path
from .views import GetVideoList, CreateUser, CreateStore, CreateProduct, CreateMusic, CreateVideo

urlpatterns = [
    path('api/getAllVideos/', GetVideoList.as_view(), name='videos-list'),
    path('api/user/', CreateUser.as_view(), name='create_user'),
    path('api/store/', CreateStore.as_view(), name='create_store'),
    path('api/product/', CreateProduct.as_view(), name='create_product'),
    path('api/music/', CreateMusic.as_view(), name='create_music'),
    path('api/video/', CreateVideo.as_view(), name='create_video'),
]