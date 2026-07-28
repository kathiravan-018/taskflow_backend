from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import *
from .serializers import *

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
class BoardListCreateView(generics.ListCreateAPIView):

    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        board = serializer.save(user=self.request.user)

        Column.objects.bulk_create([
            Column(board=board, title="Todo", order=1),
            Column(board=board, title="Doing", order=2),
            Column(board=board, title="Review", order=3),
            Column(board=board, title="Done", order=4),
        ])

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user)

class ColumnListCreateView(generics.ListCreateAPIView):

    serializer_class = ColumnSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Column.objects.filter(
            board__user=self.request.user
        )
    def perform_create(self, serializer):
        board = serializer.validated_data["board"]

        if board.user != self.request.user:
            raise PermissionDenied("You cannot create a column on another user's board.")

        serializer.save()

class ColumnDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ColumnSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Column.objects.filter(
            board__user=self.request.user
        )


class TaskListCreateView(generics.ListCreateAPIView):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            column__board__user=self.request.user
        )
    def perform_create(self, serializer):

        column = serializer.validated_data["column"]

        if column.board.user != self.request.user:
            raise PermissionDenied(
                "You cannot add tasks to this column."
            )

        serializer.save()

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            column__board__user=self.request.user
        )
