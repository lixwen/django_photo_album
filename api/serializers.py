from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Photo

from django.conf import settings
from . import minioclient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class PhotoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'user', 'image', 'uploaded_at', 'url']
        read_only_fields = ['id', 'user', 'uploaded_at']

    def get_url(self, obj):
        return f"{obj.image}"

    def create(self, validated_data):
        tmpfile = validated_data['image'].file
        path = tmpfile.name
        objName = validated_data['image'].name
        obj = minioclient.upload_to_minio(path, objName, "photo")

        instance = Photo.objects.create(
            image=obj.location,
            file_data=obj.location,
            user=validated_data['user'],

        )  # 调用父类的 create 方法创建实例
        return instance
