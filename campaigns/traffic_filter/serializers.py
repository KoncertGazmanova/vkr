from rest_framework import serializers
from .models import TrafficFilter


class TrafficFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFilter
        fields = (
            "campaign",
            "allow_countries",
            "block_ip_list",
            "block_bots",
            "ip_rate_limit",
        )
        read_only_fields = ["campaign"]
