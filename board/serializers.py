from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Profile, Board, Column, Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"

class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ["user"]


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "name",
            "college",
            "city",
            "email",
        ]


class RegisterSerializer(serializers.ModelSerializer):

    name = serializers.CharField(write_only=True)
    college = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "name",
            "college",
            "city",
        ]

    extra_kwargs = {
    "password": {
        "write_only": True,
        "validators": [validate_password],
    }
}
    def create(self, validated_data):

        name = validated_data.pop("name")
        college = validated_data.pop("college")
        city = validated_data.pop("city")

        user = User.objects.create_user(**validated_data)

        Profile.objects.create(
            user=user,
            name=name,
            college=college,
            city=city,
        )
        

        return user
