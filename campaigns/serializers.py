from rest_framework import serializers
from .models import Tag, Campaign, CampaignVariant

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    roi = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = '__all__'

    def get_roi(self, obj):
        return obj.roi()

class CampaignVariantSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer(read_only=True)

    class Meta:
        model = CampaignVariant
        fields = '__all__'
