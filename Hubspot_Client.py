import logging
import json
from urllib.parse import quote_plus, urlencode
from django.conf import settings
from apps.request.utils.connections import requests_retry_session
from . import TicketStatus

logger = logging.getLogger(__name__)


class HubSpotClient():

    def __init__(self):
        self.base_url = "https://api.hubapi.com/crm/v3/objects/"
        self.access_token = "Token"
        self.headers = {"authorization" : f"Bearer {self.access_token}"}
        

    def get_tickets(self,limit=10):
        self.tickets_url = f"{self.base_url}tickets"
        query_params = {"limit": limit,"properties": "hs_pipeline,hs_pipeline_stage,source_type,subject,content"}
        urlencoded_string = urlencode(query_params, quote_via=quote_plus)
        response = requests_retry_session().get(url=self.tickets_url, headers=self.headers,params=urlencoded_string)
        if response.status_code == 200:
            data = response.json()
            return data["results"]
        logger.error(f"Somthing went wrong with gettting tickets from Hubspot {response.status_code}-  {response.json()}")
        return None


    def retrieve_ticket(self,ticket_id):
        self.tickets_url = f"{self.base_url}tickets/{ticket_id}"
        query_params = {"properties": "hs_pipeline,hs_pipeline_stage,source_type,subject,content"}
        urlencoded_string = urlencode(query_params, quote_via=quote_plus)
        response = requests_retry_session().get(url=self.tickets_url, headers=self.headers,params=urlencoded_string)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Somthing went wrong with gettting the ticket id - {ticket_id} from Hubspot {response.status_code} - {response.json()}")
        return None
    

    def create_ticket(self,content,subject):
        self.tickets_url = f"{self.base_url}tickets"
        self.headers["content-type"] = "application/json"
        payload = {
            "properties" : {
            "hs_pipeline": settings.HUBSPOT_PIPELINE_ID,
            "hs_pipeline_stage": TicketStatus.IN_PROGRESS,
            "subject": subject,
            "content" : content,
            "source_type" : "FALCON"
            }
        }
        payload_json = json.dumps(payload)

        response = requests_retry_session().post(url=self.tickets_url, data=payload_json,headers=self.headers)
        if response.status_code == 201:
            return response.json()
        logger.error(f"Somthing went wrong while creating ticket on Hubspot {response.status_code} - {response.json()}")
        return None
