from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [

    path("register/", RegisterView.as_view()),

    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("profile/", ProfileView.as_view()),

    path("boards/", BoardListCreateView.as_view()),
    path("boards/<int:pk>/", BoardDetailView.as_view()),

    path("columns/", ColumnListCreateView.as_view()),
    path("columns/<int:pk>/", ColumnDetailView.as_view()),

    path("tasks/", TaskListCreateView.as_view()),
    path("tasks/<int:pk>/", TaskDetailView.as_view()),
]

 