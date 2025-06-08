from rest_framework import serializers
from .models import Tag, Campaign, CampaignVariant, TrafficPath

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
        extra_kwargs = {
            "country":  {"required": False, "allow_blank": True},
            "category": {"required": False, "allow_blank": True},
        }

    def get_roi(self, obj):
        return obj.roi()

class CampaignVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignVariant
        fields = "__all__"

class TrafficPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficPath
        fields = "__all__"
