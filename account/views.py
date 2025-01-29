# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer,NormalUserSerializer
from .models import NormalUser
from rest_framework.generics import ListAPIView

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data': {},
                'message': 'Your account has been created'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'data': {},
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(serializer.validated_data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'data': {},
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserListView(ListAPIView):
    queryset = NormalUser.objects.all()
    serializer_class = NormalUserSerializer