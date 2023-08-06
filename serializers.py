from rest_framework import serializers
from models.py import Ticket, HUBSPOT_ENUM_MAPPING

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = __all__

class TicketHubspotUpdateSerializer(serializers.Serializer):
    hubspot_ticket_id = serializers.CharField()
    hubspot_status = serializers.IntegerField()

    def validate_hubspot_status(self, value):
        if value not in HUBSPOT_ENUM_MAPPING.keys():
            raise serializers.ValidationError("Invalid status")
        return value
