from django.contrib import admin

from .models import Campaign, CampaignCategory, CommunicationLog

admin.site.register(Campaign)
admin.site.register(CommunicationLog)
admin.site.register(CampaignCategory)
