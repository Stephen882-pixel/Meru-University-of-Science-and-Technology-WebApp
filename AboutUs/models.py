from django.db import models

# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=200)
    about_us = models.TextField()
    vision = models.CharField(max_length=500)
    mission = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class Community(models.Model):
    MEETING_TYPES = [
        ('VIRTUAL', 'Virtual'),
        ('PHYSICAL', 'Physical'),
        ('HYBRID', 'Hybrid')
    ]

    name = models.CharField(max_length=200)
    community_lead = models.CharField(max_length=200)
    co_lead = models.CharField(max_length=200, blank=True, null=True)
    #treasurer = models.CharField(max_length=200, blank=True, null=True)
    secretary = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    description = models.TextField()
    founding_date = models.DateField(blank=True, null=True)
    total_members = models.IntegerField(default=0)
    is_recruiting = models.BooleanField(default=False)
    tech_stack = models.JSONField(blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='communities')


    # def update_total_members(self):
    #     current_count = self.members.count()
    #     if self.total_members != current_count:
    #         CommunityProfile.objects.filter(id=self.id).update(total_members=current_count)

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # Only for new instances
    #         super().save(*args, **kwargs)
    #         self.update_total_members()
    #     else:
    #         super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.name
    
    # def get_sessions(self):
    #     return self.sessions.all()
    
    # @receiver([post_save, post_delete], sender='Innovation_WebApp.CommunityMember')
    # def update_community_member_count(sender, instance, **kwargs):
    #     if instance.community:
    #         instance.community.update_total_members()

    def __str__(self):
        return f"{self.name} ({self.club.name})"
    
class ExecutiveMember(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    #image = models.ImageField(upload_to='executives/',blank=True,null=True)
    community = models.ForeignKey(Community,on_delete=models.CASCADE,related_name='executives',blank=True,null=True)
    

    def __str__(self):
        return f"{self.name} - {self.position} ({self.community.name})"
    
class SocialMedia(models.Model):
    platform = models.CharField(max_length=100) # eg facebook,instagram,twitter
    url = models.URLField()
    club = models.ForeignKey(Club,on_delete=models.CASCADE,related_name='social_media',null=True,blank=True)
    community = models.ForeignKey(Community,on_delete=models.CASCADE,related_name='social_media',null=True,blank=True)
    executive = models.ForeignKey(ExecutiveMember,on_delete=models.CASCADE,related_name="social_media",null=True,blank=True)


    def __str__(self):
        return f'{self.platform}'


    
























# class Club(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     vision = models.CharField(max_length=500)
#     mission = models.CharField(max_length=500)
    
#     def __str__(self):
#         return self.name
    

# class ExecutiveMember(models.Model):
#     name = models.CharField(max_length=200)
#     position = models.CharField(max_length=200)
#     bio = models.TextField(blank=True)
#     email = models.EmailField(blank=True)
#     image = models.ImageField(upload_to='executives',blank=True,null=True)


#     def __str__(self):
#         return f"{self.name} - {self.position}"
    
# class SocialMedia(models.Model):
#     platform = models.CharField(max_length=100) # eg facebook,Instagram,Twitter
#     url = models.URLField()
    

#     def __str__(self):
#         return f"{self.platform}"
    