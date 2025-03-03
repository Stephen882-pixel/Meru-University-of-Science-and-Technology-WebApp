from rest_framework import serializers
from .models import Club,Community,ExecutiveMember,SocialMedia


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id','platform','url']

class ExecutiveMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveMember
        fields = ['id','name','position','bio','email',]

class CommunitySerializer(serializers.ModelSerializer):
    executives = serializers.SerializerMethodField()
    class Meta:
        model = Community
        fields = [
            'id', 'name', 'community_lead', 'co_lead', 'secretary', 
            'email', 'phone_number', 'github_link', 'linkedin_link',
            'description', 'founding_date', 'total_members', 
            'is_recruiting', 'tech_stack', 'executives'
        ]
        
    def get_executive(self,obj):
        executives = ExecutiveMember.objects.filter(Community=obj)
        return ExecutiveMemberSerializer(executives,many=True).data
        
class ClubSerializers(serializers.ModelSerializer):
    communities = serializers.SerializerMethodField()
    social_media = SocialMediaSerializer(many=True,read_only=True)

    class Meta:
        model = Club
        fields = ['id', 'name', 'about_us', 'vision', 'mission', 'communities', 'social_media']
        

    def get_communities(self,obj):
        communities = Community.objects.filter(club=obj)
        return CommunitySerializer(communities,many=True).data
    