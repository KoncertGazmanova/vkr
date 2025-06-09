from rest_framework import serializers
from .models import CampaignStat, Tag, Campaign, CampaignVariant, TrafficPath, CampaignHeadline, CampaignNote, TeaserMetric

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    roi = serializers.SerializerMethodField()
    variants_count = serializers.IntegerField(read_only=True)

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
    payout = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False
    )
    class Meta:
        model  = CampaignVariant
        fields = "__all__"

class TrafficPathSerializer(serializers.ModelSerializer):
    leads = serializers.IntegerField()
    approvals = serializers.IntegerField()
    payout = serializers.DecimalField(max_digits=8, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = TrafficPath
        fields = "__all__"
        
class CampaignStatSerializer(serializers.ModelSerializer):
    cost    = serializers.DecimalField(max_digits=10, decimal_places=2,
                                       coerce_to_string=False)
    revenue = serializers.DecimalField(max_digits=10, decimal_places=2,
                                       coerce_to_string=False)
    hour = serializers.IntegerField()

    class Meta:
        model  = CampaignStat
        fields = "__all__"

class CampaignHeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignHeadline
        fields = "__all__"

class CampaignNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignNote
        fields = "__all__"

class TeaserMetricCurrentSerializer(serializers.ModelSerializer):
    roi = serializers.SerializerMethodField()

    class Meta:
        model  = TeaserMetric
        fields = ("teaser_id","clicks","conversions","cost","revenue","roi")

    def get_roi(self,obj):
        return obj.roi()

class TeaserMetricDeltaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TeaserMetric
        fields = (
            "teaser_id",
            "clicks", "clicks_prev", "diff_clicks",
            "roi_now", "roi_prev", "diff_roi"
        )
