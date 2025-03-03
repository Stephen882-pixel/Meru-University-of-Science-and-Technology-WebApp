from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Club,Community,ExecutiveMember,SocialMedia
from .serializers import ClubSerializers,CommunitySerializer,ExecutiveMemberSerializer,SocialMediaSerializer
from django.shortcuts import get_object_or_404
# Create your views here.

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializers
    permission_classes = [IsAuthenticated]

    def list(self,request):
        clubs = self.get_queryset()
        serializer = self.get_serializer(clubs,many=True)
        return Response({
            'message':'Clubs retrieved successfully',
            'message':'success',
            'data':serializer.data
        },status=status.HTTP_200_OK)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Club created successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
    
    def retrieve(self,request,pk=None):
        try:
            #club = self.get_object()
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            print("Serializer data:",serializer.data)
            print("Instance Data:", instance.__dict__)  
            return Response({
                'message':'Club retrieved successfully',
                'status':'succeess',
                'data':serializer.data
            },status =status.HTTP_200_OK)
        except Club.DoesNotExist:
            return Response({
                'message':'Club not found',
                'status':'error'
            },status=status.HTTP_404_NOT_FOUND)
    def update(self,request,pk=None):
        club = self.get_object()
        serializer = self.get_serializer(club, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Club update successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            'message':'failed to update club',
            'status':'failed',
            'data':serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    def destroy(self,request,pk=None):
        club = self.get_object()
        club.delete()
        return Response({
            'message':'Club deleted successfully',
            'status':'success',
            'data':[]
        },status=status.HTTP_200_OK)

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def list(self,request):
        communities = self.get_queryset()
        club_id = request.query_params.get('club_id',None)
        if club_id:
            communities = communities.filter(club_id=club_id)
        serializer = self.get_serializer(communities,many=True)
        return Response({
            'message':'Communities retrieved successfuly',
            'status':'success',
            'data':serializer.data
        },status=status.HTTP_200_OK)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Community created successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            'message':'failed to create the community',
            'status':'error',
            'data':serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        try:
            community = self.get_object()
            serializer = self.get_serializer(community)
            return Response({
                'message':'Community retrieved successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        except Community.DoesNotExist:
            return Response({
                'message':'Community not found',
                'status':'failed',
                'data':None
            },status=status.HTTP_400_BAD_REQUEST)
        
    def update(self,request,pk=None):
        community = self.get_object()
        serializer = self.get_serializer(community,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Community updated succesfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            'message':'failed to update community',
            'status':'failed',
            'data':serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        community = self.get_object()
        community.delete()
        return Response({
            'message':'Community deleted successfully',
            'status':'success',
            'data':[]
        }, status=status.HTTP_204_NO_CONTENT)
    
class ExecutiveMemberViewSet(viewsets.ModelViewSet):
    queryset = ExecutiveMember.objects.all()
    serializer_class = ExecutiveMemberSerializer
    permission_classes = [IsAuthenticated]

    def list(self,request):
        executives = self.get_queryset()
        community_id = request.query_params.get('community_id',None)
        if community_id:
            executives = executives.filter(community_id=community_id)
        serializer = self.get_serializer(executives,many=True)
        return Response({
            'message':'Exective members retrieved successfully',
            'status':'success',
            'data':serializer.data
        },status=status.HTTP_200_OK)
    
    def create(self,request):
        club_id=request.data.get('club') # extract club id from request
        club = get_object_or_404(Club, id=club_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Executive Member created successully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            'message':'failed to create executive member',
            'status':'failed',
            'data':serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        try:
            executive = self.get_object()
            serializer = self.get_serializer(executive)
            return Response({
                'message':'Executive member retrieved successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        except ExecutiveMember.DoesNotExist:
            return Response({
                'message':'Executive member not found',
                'status':'failed',
                'data':None
            },status=status.HTTP_404_NOT_FOUND)
    
    def update(self,request,pk=None):
        executive = self.get_object()
        serializer = self.get_serializer(executive,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Executive member updated successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            'message':'failed to update the executive member',
            'status':'failed',
            'data':serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def destory(self,request,pk=None):
        executive = self.get_object()
        executive.delete()
        return Response({
            'message':'Executive memeber deleted successfully',
            'status':'success',
            'data':[]
        },status=status.HTTP_204_NO_CONTENT)

class SocialMediaViewSet(viewsets.ModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [IsAuthenticated]

    def list(self,request):
        social_media = self.get_queryset()
        club_id = request.query_params.get('club_id',None)
        community_id = request.query_params.get('community_id', None)
        executive_id = request.query_params.get('executive_id', None)

        if club_id:
            social_media = social_media.filter(club_id=club_id)
        if community_id:
            social_media = social_media.filter(community_id=community_id)
        if executive_id:
            social_media = social_media.filter(executive_id=executive_id)

        serializer = self.get_serializer(social_media,many=True)
        return Response({
            'message':'social media platforms retrieved successfully',
            'status':'success',
            'data':serializer.data
        },status=status.HTTP_200_OK)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Social platform created successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            'meeage':'failed to create social media platform',
            'status':'failed',
            'data':serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        try:
            social_media = self.get_object()
            serializer = self.get_serializer(social_media)
            return Response({
                'message':'social media platform retrieved successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        except SocialMedia.DoesNotExist:
            return Response({
                'messge':'Social Media Platform was not found',
                'status':'failed',
                'data':None
            },status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        social_media = self.get_object()
        serializer = self.get_serializer(social_media, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Social media platform updated successfully',
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Failed to update social media platform',
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        social_media = self.get_object()
        social_media.delete()
        return Response({
            'message': 'Social media platform deleted successfully',
            'status': 'success',
            'data':[]
        }, status=status.HTTP_204_NO_CONTENT)
    


   


