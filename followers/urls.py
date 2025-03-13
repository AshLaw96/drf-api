from django.urls import path
from followers import views


urlpatterns = [
    path('followers/', views.FollowList.as_view(), name='followers'),
    path(
        'followers/<int:pk>/',
        views.FollowDetail.as_view(),
        name='follower_detail'
    ),
]
