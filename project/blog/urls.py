from django.urls import path,include
from blog import views
from .views import (
   PostListView, 
   PostDetailView, 
   PostCreateView,
   PostUpdateView,
   PostDeleteView,
   UserPostListView,
)




urlpatterns = [
   path('blog',PostListView.as_view(),name="handleblog"),
   path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
   path('blog/post/<int:pk>/',PostDetailView.as_view(),name="post-detail"),
   path('blog/post/new/',PostCreateView.as_view(),name="post-create"),
   path('blog/post/<int:pk>/update/',PostUpdateView.as_view(),name="post-update"),
   path('blog/post/<int:pk>/delete/',PostDeleteView.as_view(),name="post-delete"),  
]

