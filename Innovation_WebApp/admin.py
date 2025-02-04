from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Events)
admin.site.register(SubscribedUsers)
admin.site.register(EventRegistration)
#admin.site.register(CommunityCategory)
admin.site.register(CommunityProfile)
admin.site.register(CommunitySession)
admin.site.register(Testimonial)




