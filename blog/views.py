from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Blog
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q


class BlogView(APIView):
    allowed_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            #blogs = Blog.objects.all()

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

            serializer = BlogSerializer(blogs, many=True)

            return Response({
                'data': serializer.data,
                'message': 'blog fetched successfully',
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong',
            },status=status.HTTP_400_BAD_REQUEST)




    def post(self, request):
        try:
        # Create a mutable copy of request data
             data = request.data.copy()
             data['user'] = request.user.id
        
             serializer = BlogSerializer(data=data)
        
             if not serializer.is_valid():
                return Response({
                'data': serializer.errors,
                'message': 'Validation failed'
                }, status=status.HTTP_400_BAD_REQUEST)

             serializer.save()
             return Response({
             'data': serializer.data,
             'message': 'Blog created successfully'
             }, status=status.HTTP_201_CREATED)

        except Exception as e:
             return Response({
            'data': {},
            'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def patch(self, request):
        try:
            data = request.data
            
            # Validate uid exists in request
            if not data.get('uid'):
                return Response({
                    'data': {},
                    'message': 'blog uid is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            blog = Blog.objects.filter(uid=data.get('uid'))
            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'invalid blog uid'
                }, status=status.HTTP_400_BAD_REQUEST)

            blog_obj = blog.first()
            
            # Check if blog has user assigned
            if not hasattr(blog_obj, 'user'):
                return Response({
                    'data': {},
                    'message': 'blog has no user assigned'
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog_obj.user:
                return Response({
                    'data': {},
                    'message': 'you are not authorized to do this'
                }, status=status.HTTP_403_FORBIDDEN)
            
            serializer = BlogSerializer(blog_obj, data=data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'blog updated successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request):
            try:
                data = request.data
                blog = Blog.objects.filter(uid=data.get('uid'))
                if not blog.exists():
                    return Response({
                        'data': {},
                        'message': 'invalid blog uid'
                    }, status=status.HTTP_400_BAD_REQUEST)

                #blog = Blog.objects.all()
                if request.user != blog[0].user:
                    return Response({
                         'data': {},
                         'message': 'you are not authorized to do this'
                }, status=status.HTTP_400_BAD_REQUEST)  

                blog[0].delete()
                return Response({
                    'data': {},
                    'message': 'blog deleted successfully'
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(e)
                return Response({
                        'data': {},
                        'message': 'something went wrong'
                 }, status=status.HTTP_400_BAD_REQUEST)