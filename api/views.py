from rest_framework.views import APIView
from rest_framework import generics, status
from django.contrib.auth.models import User
from .models import Photo
from .serializers import UserSerializer, PhotoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView
from django.core.files.base import ContentFile

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)



class PhotoCreateView(CreateAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        uploaded_image = self.request.data.get('image')
        file_data = uploaded_image.read()
        ins = serializer.save(user=self.request.user, file_data=file_data)
        print('ins: ' + str(ins))
        return Response({'code' : 200})

class PhotoListView(ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list = Photo.objects.filter(user=self.request.user)
        return list;

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        refresh = RefreshToken.for_user(token.user)

        return Response({'token': str(refresh.access_token), 'user_id': token.user_id, 'email': token.user.email})
