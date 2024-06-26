from django.contrib.auth import logout, authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user_management.models import User
from user_management.serializers import UserSerializer, AdminUserSerializer, LoginSerializer


# Create your views here.
class AdminUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = User.objects.filter(is_staff=True).order_by('username')
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = AdminUserSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            serializer = AdminUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        if request.user.is_superuser:
            username = request.query_params.get('username')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'Không có giá trị thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)

            serializer = AdminUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.user.is_staff:
                serializer = AdminUserSerializer(request.user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Không có quyền thực hiện hành động này'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser:
            username = request.query_params.get('username')
            user = User.objects.get(username=username)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Không có quyền thực hiện hành động này'}, status=status.HTTP_401_UNAUTHORIZED)


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        username = request.query_params.get('username', None)

        if username:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user, many=False)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            limit = request.query_params.get('limit', 10)
            page = request.query_params.get('page', 1)
            limit = int(limit)
            page = int(page)

            objects = User.objects.filter(is_staff=False).order_by('username')
            total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
            current_page_objects = objects[(page - 1) * limit:page * limit]

            serializer = UserSerializer(current_page_objects, many=True)
            return Response({
                'data': serializer.data,
                'meta': {
                    'total_pages': total_pages,
                    'current_page': page,
                    'limit': limit,
                    'total': objects.count()
                }
            }, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        if request.user.is_superuser:
            username = request.query_params.get('username')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'Không có giá trị thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializers = UserSerializer(request.user, data=request.data, partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response({'data': serializers.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser:
            username = request.query_params.get('username')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error':'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            request.user.delete()
            return Response( status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            print(user)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response('Đã đăng xuất', status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class InfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request,  *args, **kwargs):
        serializer = UserSerializer(instance=request.user)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        

