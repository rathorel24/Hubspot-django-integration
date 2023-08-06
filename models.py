from django.db import models

HUBSPOT_ENUM_MAPPING = {
    HUBSPOT_IN_PROGRESS : 1,
    HUBSPOT_CLIENT_CONFIRMATION : 2,
    HUBSPOT_CLOSED : 3
}

class TicketStatus(models.IntegerChoices):
    IN_PROGRESS = HUBSPOT_ENUM_MAPPING[HUBSPOT_IN_PROGRESS] , "In Progress"
    CLIENT_CONFIRMATION = HUBSPOT_ENUM_MAPPING[HUBSPOT_CLIENT_CONFIRMATION] , "Client Confirmation"
    CLOSED = HUBSPOT_ENUM_MAPPING[HUBSPOT_CLOSED], "Closed"


class Ticket(models.Model):
    hubspot_id = models.CharField(_("HubSpot Ticket ID"), max_length=50,blank=True,null=True)
    # user from user app
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="tickets", verbose_name=_("User"))
    subject = models.IntegerField(_("Ticket Subject"), choices=Subject.choices)
    description = models.TextField(_("Description"))
    screenshot = models.FileField(_("Screenshot"),upload_to=upload_ticket_screenshot, blank=True, null=True)
    status = models.IntegerField(_("Ticket Status"), choices=TicketStatus.choices(), default=TicketStatus.IN_PROGRESS)
    status = models.IntegerField(_("Ticket Status"), choices=TicketStatus.choices, default=TicketStatus.IN_PROGRESS)
    closing_remark = models.TextField(
        _("Closing Remark"), null=True, blank=True, help_text="Please Enter remark on closing the ticket"
    )
  
    def __str__(self):
        return f"{self.id}-{self.user}"

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        db_table = "tickets"
