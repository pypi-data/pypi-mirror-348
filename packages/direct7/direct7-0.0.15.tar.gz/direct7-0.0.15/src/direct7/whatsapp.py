import logging
import uuid

log = logging.getLogger(__name__)


class WHATSAPP:

    def __init__(self, client):
        self._client = client

    def send_whatsapp_freeform_message(self, originator: str, recipient: str, message_type: str, first_name: str = None,
                                       last_name: str = None, formatted_name: str = None, middle_name: str = None,
                                       suffix: str = None, prefix: str = None, birthday: str = None,
                                       phones: list = None, emails: list = None, urls: list = None,
                                       latitude: str = None, longitude: str = None, name: str = None,
                                       address: str = None, type: str = None, url: str = None, caption: str = None,
                                       filename: str = None, body: str = None, message_id: uuid.UUID = None,
                                       emoji: str = None, contact_addresses: list = None, ):
        """
        Send a WhatsApp message to a single/multiple recipients.
        :param filename:
        :param prefix: Prefix for the contact's name, such as Mr., Ms., Dr., etc.
        :param suffix: Suffix for the contact's name, if applicable.
        :param middle_name: Contact's middle name.
        :param contact_addresses:
        :param emoji:
        :param message_id:
        :param birthday: Contact's birthday in YYYY-MM-DD format.
        :param originator: str - The message originator.
        :param recipient: str - The message recipient.
        :param message_type: str - The type of message ("CONTACTS", "LOCATION", "ATTACHMENT", "TEXT").
        :param first_name: str - First name for "CONTACTS" message type.
        :param last_name: str - Last name for "CONTACTS" message type.
        :param formatted_name: str - Display name for "CONTACTS" message type.
        :param phones: list - Phone number for "CONTACTS" message type.
        :param emails: list - Email address for "CONTACTS" message type.
        :param urls: list - URL for "CONTACTS" message type.
        :param latitude: str - Latitude for "LOCATION" message type.
        :param longitude: str - Longitude for "LOCATION" message type.
        :param name: str - Location name for "LOCATION" message type.
        :param address: str - Location address for "LOCATION" message type.
        :param type: str - Attachment type for "ATTACHMENT" message type.
        :param url: str - Attachment URL for "ATTACHMENT" message type.
        :param caption: str - Attachment caption for "ATTACHMENT" message type.
        :param body: str - Message text for "TEXT" message type.
        """
        message = {
            "originator": originator,
            "recipients": [{"recipient": recipient}],
            "content": {
                "message_type": message_type
            }
        }

        if message_type == "CONTACTS":
            message["content"]["contacts"] = [{
                "name": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "formatted_name": formatted_name,
                    "middle_name": middle_name,
                    "suffix": suffix,
                    "prefix": prefix,
                },
                "addresses": contact_addresses,
                "birthday": birthday,
                "phones": phones,
                "emails": emails,
                "urls": urls
            }]
        elif message_type == "LOCATION":
            message["content"]["location"] = {
                "latitude": latitude,
                "longitude": longitude,
                "name": name,
                "address": address
            }
        elif message_type == "ATTACHMENT":
            if type == "document":
                message["content"]["attachment"] = {
                    "type": type,
                    "url": url,
                    "caption": caption,
                    "filename": filename
                }
            else:
                message["content"]["attachment"] = {
                    "type": type,
                    "url": url,
                    "caption": caption
                }
        elif message_type == "TEXT":
            message["content"]["text"] = {
                "body": body
            }

        elif message_type == "REACTION":
            message["content"]["reaction"] = {
                "message_id": message_id,
                "emoji": emoji
            }

        response = self._client.post(
            self._client.host(), "/whatsapp/v2/send", params={"messages": [message]})
        log.info("Message sent successfully.")
        return response

    def send_whatsapp_templated_message(self, originator: str, recipient: str, template_id: str, language: str,
                                        body_parameter_values: dict = {}, media_type: str = None,
                                        text_header_title: str = None, media_url: str = None,
                                        latitude: str = None, longitude: str = None, name: str = None,
                                        address: str = None, lto_expiration_time_ms: str = None,
                                        coupon_code: str = None, quick_replies: dict = None, actions: dict = None,
                                        button_flow:dict = None,
                                        carousel_cards: list = []):
        """
        Send a WhatsApp message to a single/multiple recipients.
        :param originator: str - The message originator.
        :param recipient: str - The message recipient.
        :param template_id: str - The template ID for text messages.
        :param body_parameter_values: dict - The body parameter values for text templates.
        :param media_type: str - The type of media (e.g., "image", "video").
        :param media_url: str - The URL of the media content.
        """
        message = {
            "originator": originator,
            "recipients": [{"recipient": recipient}],
            "content": {
                "message_type": "TEMPLATE",
                "template": {"template_id": template_id, "language": language,
                             "body_parameter_values": body_parameter_values}
            }
        }

        if media_type:
            if media_type == "location":
                message["content"]["template"]["media"] = {
                    "media_type": "location",
                    "location": {
                        "latitude": latitude,
                        "longitude": longitude,
                        "name": name,
                        "address": address
                    }
                }
            elif media_type == "text":
                message["content"]["template"]["media"] = {
                    "media_type": media_type, "text_header_title": text_header_title}
            else:
                message["content"]["template"]["media"] = {
                    "media_type": media_type, "media_url": media_url}
        if lto_expiration_time_ms:
            message["content"]["template"]["limited_time_offer"] = {
                "expiration_time_ms": lto_expiration_time_ms
            }
        if button_flow:
            message["content"]["template"]["buttons"] = {
                'button_flow': button_flow
            }
        if coupon_code:
            message["content"]["template"]["buttons"] = {
                "coupon_code": [
                    {
                        "index": 0,
                        "type": "copy_code",
                        "coupon_code": coupon_code
                    }
                ]
            }
        if actions:
            message["content"]["template"]["buttons"] = {
                "actions": actions
            }

        if quick_replies:
            message["content"]["template"]["buttons"] = {
                "quick_replies": quick_replies
            }

        if carousel_cards:
            message["content"]["template"]["carousel"] = {
                "cards": carousel_cards
            }

        response = self._client.post(
            self._client.host(), "/whatsapp/v2/send", params={"messages": [message]})
        log.info("Message sent successfully.")
        return response

    def send_whatsapp_interactive_message(self, originator: str, recipient: str, interactive_type: str,
                                          header_type: str = None, header_text: str = None,
                                          header_link: str = None, header_file_name: str = None, body_text: str = None,
                                          footer_text: str = None, parameters: dict = None, sections: list = None,
                                          buttons: list = None, list_button_text: str = None, ):
        """
        Send a WhatsApp interactive message to a single/multiple recipients.
        :param originator: str - The message originator.
        :param recipient: str - The message recipient.
        :param interactive_type:

        """
        message = {
            "originator": originator,
            "recipients": [{"recipient": recipient}],
            "content": {
                "message_type": "INTERACTIVE",
                "interactive": {
                    "type": interactive_type,
                    "header": {
                        "type": header_type,
                    },
                    "body": {
                        "text": body_text,
                    },
                    "footer": {
                        "text": footer_text,
                    }
                }
            }
        }
        if header_type == "text":
            message["content"]["interactive"]["header"]["text"] = header_text

        elif header_type == "image" or header_type == "video" or header_type == "document":
            message["content"]["interactive"]["header"][header_type] = {
                "filename": header_file_name if header_type == "document" else None,
                "link": header_link
            }

        if interactive_type == "cta_url":
            message["content"]["interactive"]["action"] = {
                "parameters": parameters,
            }
        elif interactive_type == "button":
            message["content"]["interactive"]["action"] = {
                "buttons": buttons,
            }
        elif interactive_type == "list":
            message["content"]["interactive"]["action"] = {
                "sections": sections,
                "button": list_button_text
            }
        elif interactive_type == "location_request_message":
            message["content"]["interactive"]["action"] = {
                "name": "send_location"
            }
        
        elif interactive_type == "address_message":
            message["content"]["interactive"]["action"] = {
                "parameters": parameters
            }
        elif interactive_type == "flow":
            message["content"]["interactive"]["action"] = parameters
        

        response = self._client.post(
            self._client.host(), "/whatsapp/v2/send", params={"messages": [message]})
        log.info("Message sent successfully.")
        return response

    def get_status(self, request_id: str):
        """
        Get the status for a whatsapp message request.
        :param params:
        request_id : str - The request ID of the whatsapp message request.
        :return:
        """
        response = self._client.get(
            self._client.host(),
            f"/whatsapp/v1/report/{request_id}"
        )
        log.info("Message status retrieved successfully.")
        return response

    def read_receipt(self, message_id: str):
        """
        Mark an incoming messsage as read
        :param params:
        request_id : str - The message ID of the whatsapp message.
        :return:
        """
        response = self._client.post(
            self._client.host(),
            f"/whatsapp/v2/read-receipt/{message_id}"
        )
        log.info("Successfully marked incoming message as read.")
        return response

    def download_media(self, media_id: str):
         """
         Download user Initiated Media
         :param params:
         media_id : str - The media ID of the whatsapp user initiated message.
         :return:
         """
         response = self._client.get(
             self._client.host(),
             f"/whatsapp/v2/download/{media_id}"
         )
         log.info("Successfully downloaded media.")
         return response