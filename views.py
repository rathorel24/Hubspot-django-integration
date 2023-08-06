from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from Hubspot_Client import HubspotClient
from .serializers import TicketSerializer, TicketHubspotUpdateSerializer


def create_ticket_on_hubspot(ticket_id):

    ticket = Ticket.objects.get(id=ticket_id)
    request_id, user_takeoff_id, address_or_name, source = get_ticket_content_data(ticket)
    content , subject = get_hubspot_ticket_content(ticket,request_id, user_takeoff_id, address_or_name, source)

    hubspot_client = HubSpotClient()
    response = hubspot_client.create_ticket(content=content,subject=subject)
    if response:
        ticket.hubspot_id = response["id"]
        ticket.save(update_fields=["hubspot_id"])
    else:
        logger.error(f"Hubspot ticket creation failed")
      
class TicketViewSet(ViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = Ticket.objects.create(user=user, **serializer.validated_data)
        create_ticket_on_hubspot(ticket.id)
        return response.Created(self.serializer_class(ticket).data)
    
    @action(methods=["POST"], detail=False,)
    def hubspot_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hubspot_ticket_id = serializer.validated_data.get("hubspot_ticket_id")
        hubspot_status = HUBSPOT_ENUM_MAPPING[serializer.validated_data.get("hubspot_status")]

        ticket = Ticket.objects.filter(hubspot_id=hubspot_ticket_id).first()
        if not ticket:
            raise BadRequest("Ticket Does not exist")
        ticket.status = hubspot_status
        ticket.resolved_at = timezone.now()
        ticket.save(update_fields=["status","resolved_at"])
        return response.Ok()
    
    def get_serializer_class(self):
        if self.action == "hubspot_update":
            return TicketHubspotUpdateSerializer
        return self.serializer_class
