# Hubspot-django-integration
# Ticketing System - Hubspot Integration with Django App

This project aims to integrate HubSpot, a popular CRM platform, with a Django web application to streamline ticket management and provide a seamless experience for users. The integration will allow users to create, update, and manage tickets in HubSpot directly from the Django app. To achieve this, we'll be using the HubSpot API and creating a private app to authenticate our API requests.

## Obtaining a Private App Token from HubSpot

To access the HubSpot API, we need a private app token. Follow the steps below to obtain the private app token:

1. Log in to HubSpot with a super admin account.
2. Navigate to the App Marketplace and create a new private app.
3. The private app token will be generated, and we will use this token for authentication in API requests to HubSpot.

For more details on obtaining the private app token, refer to the [HubSpot documentation](https://developers.hubspot.com/docs/api/private-apps).


### Pipeline Setup

1. Create a dedicated pipeline specifically for integrating with our App.
2. Customize the pipeline by adding new statuses that reflect the various stages of ticket resolution.

For instructions on creating a new pipeline in HubSpot, follow this [link](https://knowledge.hubspot.com/tickets/customize-ticket-pipelines-and-statuses).

## Creating HubSpot Tickets from our Platform and Synchronization

### HubSpot API Integration

We will utilize the HubSpot API to establish a connection between our Django platform and HubSpot. By leveraging the capabilities of the HubSpot API, we can seamlessly transfer ticket data between the two systems.

### Ticket Creation

1. When a user creates a ticket on our Django platform, we will initiate a POST request to the HubSpot API endpoint for ticket creation.
2. The HubSpot API will process this request and create a corresponding ticket in the designated New pipeline.
3. Upon successful ticket creation in HubSpot, we will save the HubSpot ticket ID in our database. This unique identifier allows us to maintain a reference to the ticket in HubSpot, enabling future updates and synchronizations between our platform and HubSpot.

### Webhook Integration for Ticket Status Updates

To keep our database updated with the latest ticket status, we will utilize the HubSpot webhook feature. Follow the steps below to set up the webhook integration:

1. Configure a webhook in HubSpot that triggers a notification to our Django platform whenever there is a change in the ticket status.
2. Include the HubSpot ticket ID in the webhook payload, enabling us to identify the corresponding ticket in our database and update its status accordingly.

### Creating Authorization Token for Hubspot Webhook

To authenticate incoming requests from HubSpot webhooks, we will create an entry in API Auth Tokens. This will ensure that only authenticated users can interact with our webhook.

## Setting up Workflow in HubSpot for Status Updates

1. Set up a workflow in HubSpot to handle status updates for tickets.
2. Utilize the HubSpot webhook functionality to trigger an HTTP request to our "hubspot_update" API endpoint whenever a ticket status changes in HubSpot.

For more details on setting up workflows in HubSpot, refer to the [HubSpot documentation](https://knowledge.hubspot.com/tickets/customize-ticket-pipelines-and-statuses).

With this integration in place, our Django platform and HubSpot will work harmoniously, enabling efficient ticket management and seamless synchronization of ticket statuses.
