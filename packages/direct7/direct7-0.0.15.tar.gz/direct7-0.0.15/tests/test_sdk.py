from src.direct7 import Client

client = Client(
    api_token='Your API Token')


def test_send_messages():
    # Contacts

    contact_addresses = [
        {
            "street": "1 Lucky Shrub Way",
            "city": "Menlo Park",
            "state": "CA",
            "zip": "94025",
            "country": "United States",
            "country_code": "US",
            "type": "WORK"
        },
        {
            "street": "1 Hacker Way",
            "city": "Menlo Park",
            "state": "CA",
            "zip": "94025",
            "country": "United States",
            "country_code": "US",
            "type": "WORK"
        }
    ]

    phones = [
        {
            "phone": "+16505559999",
            "type": "HOME"
        },
        {
            "phone": "+19175559999",
            "type": "WORK",
            "wa_id": "19175559999"
        }
    ]

    emails = [
        {
            "email": "bjohnson@luckyshrub.com",
            "type": "WORK"
        },
        {
            "email": "bjohnson@luckyshrubplants.com",
            "type": "HOME"
        }
    ]
    urls = [
        {
            "url": "https://www.luckyshrub.com",
            "type": "WORK"
        },
        {
            "url": "https://www.facebook.com/luckyshrubplants",
            "type": "WORK"
        }
    ]

    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="XXXXXXXXXXXX",
                                                                            recipient="XXXXXXXXXXXX",
                                                                            message_type="CONTACTS",
                                                                            first_name="Barbara",
                                                                            last_name="Johnson",
                                                                            formatted_name="Barbara J. Johnson",
                                                                            middle_name="Joana", suffix="Esq.",
                                                                            prefix="Dr.",
                                                                            phones=phones, emails=emails,
                                                                            contact_addresses=contact_addresses,
                                                                            urls=urls)

    # Text

    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="XXXXXXXXXXXX",
                                                                            recipient="XXXXXXXXXXXX",
                                                                            message_type="TEXT", body="Hi")

    # attachment
    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="XXXXXXXXXXXXX",
                                                                            recipient="XXXXXXXXXXXXX",
                                                                            message_type="ATTACHMENT", type="image",
                                                                            url="https://t4.ftcdn.net/jpg/01/43/23/83/360_F_143238306_lh0ap42wgot36y44WybfQpvsJB5A1CHc.jpg",
                                                                            caption="Tet")

    # attachment: Sticker
    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="+XXXXXXXXXXXX",
                                                                            recipient="XXXXXXXXXXXX",
                                                                            message_type="ATTACHMENT", type="sticker",
                                                                            url="https://raw.githubusercontent.com/sagarbhavsar4328/dummys3bucket/master/sample3.webp")
    # location
    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="+XXXXXXXXXXXX",
                                                                            recipient="XXXXXXXXXXXX",
                                                                            message_type="LOCATION",
                                                                            latitude="12.93803129081362",
                                                                            longitude="77.61088653615994",
                                                                            name="Mobile Pvt Ltd",
                                                                            address="30, Hosur Rd, 7th Block, Koramangala, Bengaluru, Karnataka 560095")

    # templated: location
    response_send_messages = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXXX",
                                                                             recipient="+XXXXXXXXXXXX",
                                                                             template_id="location", language="en",
                                                                             media_type="location",
                                                                             latitude="12.93803129081362",
                                                                             longitude="77.61088653615994",
                                                                             name="Mobile Pvt Ltd",
                                                                             address="30, Hosur Rd, 7th Block, Koramangala, Bengaluru, Karnataka 560095")

    # templated: text
    response_send_messages = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXXX",
                                                                             recipient="+XXXXXXXXXXXX",
                                                                             template_id="header_param", language="en",
                                                                             media_type="text",
                                                                             text_header_title="Ds")

    # lto
    response_send_messages = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXX",
                                                                             recipient="XXXXXXXXXXXXX",
                                                                             template_id="limited_time_offer",
                                                                             media_type="image",
                                                                             media_url="https://upload.wikimedia.org",
                                                                             lto_expiration_time_ms="1708804800000",
                                                                             coupon_code="DWS44")
    # Action
    actions = [
        {
            "action_type": "url",
            "action_index": "0",
            "action_payload": "dashboard"
        }
    ]

    response_send_messages = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXX",
                                                                             recipient="XXXXXXXXXXXXX",
                                                                             template_id="click_me",
                                                                             actions=actions)
    # Flow
    button_flow=[{"flow_token":"unused",
                "action_type":"flow",
                "index":"0",
                "flow_action_data":{}
                }]

    response_send_messages = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXX",
                                                                             recipient="+XXXXXXXXXXX",
                                                                             template_id="sample_testing_campaign",
                                                                             language='en_GB',
                                                                             button_flow=button_flow)
    # Carousel
    cards = [
        {
            "card_index": "0",
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "link": "https://miro.medium.com/max/780/1*9Wdo1PuiJTZo0Du2A9JLQQ.jpeg"
                            }
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "quick_reply",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "payload",
                            "payload": "2259NqSd"
                        }
                    ]
                }
            ]
        },
        {
            "card_index": "1",
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "link": "https://www.selfdrive.ae/banner_image/desktop/21112023164328_409449002729.jpg"
                            }
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "quick_reply",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "payload",
                            "payload": "59NqSdd"
                        }
                    ]
                }
            ]
        }
    ]

    response_send_messages = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXX",
                                                                             recipient="XXXXXXXXXXXXX",
                                                                             template_id="carousel_card",
                                                                             carousel_cards=cards)

    # Reaction
    emoji = "\U0001F600"
    response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="+XXXXXXXXXXXX",
                                                                            recipient="XXXXXXXXXXXX",
                                                                            message_type="REACTION",
                                                                            message_id="f1a99798-11aa-11ef-9821-0242ac1b0030",
                                                                            emoji="\U0001F600")

    # interactive cta_url: text

    parameters = {
        "display_text": "Visit Alpha",
        "url": "https://www.luckyshrub.com?clickID=kqDGWd24Q5TRwoEQTICY7W1JKoXvaZOXWAS7h1P76s0R7Paec4"
    }
    response_send_messages = client.whatsapp.send_whatsapp_interactive_message(originator="+XXXXXXXXXXXX",
                                                                               recipient="XXXXXXXXXXXX",
                                                                               interactive_type="cta_url",
                                                                               header_type="text",
                                                                               header_text="Payment$ for D7 Whatsapp Service",
                                                                               body_text="Direct7 Networks is a messaging service provider that specializes in helping organizations efficiently communicate with their customers.",
                                                                               footer_text="Thank You",
                                                                               parameters=parameters)

    ## interactive cta_url: image

    parameters = {
        "display_text": "Visit Alpha",
        "url": "https://www.luckyshrub.com?clickID=kqDGWd24Q5TRwoEQTICY7W1JKoXvaZOXWAS7h1P76s0R7Paec4"
    }
    response_send_messages = client.whatsapp.send_whatsapp_interactive_message(originator="+XXXXXXXXXXXX",
                                                                               recipient="XXXXXXXXXXXX",
                                                                               interactive_type="cta_url",
                                                                               header_type="image",
                                                                               header_link="https://karix.s3.ap-south-1.amazonaws.com/English-4.jpg",
                                                                               body_text="Direct7 Networks is a messaging service provider that specializes in helping organizations efficiently communicate with their customers.",
                                                                               footer_text="Thank You",
                                                                               parameters=parameters)

    # interactive Location Request Message

    response_send_messages = client.whatsapp.send_whatsapp_interactive_message(originator="+XXXXXXXXXXXX",
                                                                               recipient="XXXXXXXXXXXX",
                                                                               interactive_type="location_request_message",
                                                                               body_text="Let's Start with your pickup")
    # interactive Address Message
    parameters_address = {
            "country": "IN",
            "values": {
               "name": "Steni Mariya",
               "phone_number": "+971549758543",
               "in_pin_code": 687826,
               "house_number": "45",
               "floor_number": "3",
              "tower_number": 34,
              "building_name": "Excel",
              "address": "House nammmme",
              "landmark_area": "Near Mobile Tower",
              "city": "Thrissur",
              "state": "Kerala"
            },
          "saved_addresses": [
              {
              "id": "address1",
               "value": {
               "name": "Lifiya Mariya",
               "phone_number": "+971569698543",
               "in_pin_code": 6843426,
               "house_number": "45",
               "floor_number": "3",
              "tower_number": 34,
              "building_name": "Excel",
              "address": "House nammmme",
              "landmark_area": "Near Mobile Tower",
              "city": "Thrissur",
              "state": "Kerala"
            }
              },
              {
              "id": "address1",
               "value": {
               "name": "Mariya",
               "phone_number": "+971589652543",
               "in_pin_code": 680012,
               "house_number": "45",
               "floor_number": "3",
              "tower_number": 34,
              "building_name": "Excel",
              "address": "House nammmme",
              "landmark_area": "Near Mobile Tower",
              "city": "Thrissur",
              "state": "Kerala"
            }
              }
          ]
         }

    response_send_messages = client.whatsapp.send_whatsapp_interactive_message(originator="+XXXXXXXXXXXX",
                                                                               recipient="XXXXXXXXXXXX",
                                                                               interactive_type="address_message",
                                                                                header_type="image",
                                                                               header_link="https://karix.s3.ap-south-1.amazonaws.com/English-4.jpg",
                                                                               body_text="Direct7 Networks is a messaging service provider that specializes in helping organizations efficiently communicate with their customers.",
                                                                               footer_text="Thank You",
                                                                               parameters=parameters_address)

    # interactive button: image

    buttons = [
        {
            "type": "reply",
            "reply": {
                "id": "1",
                "title": "Debit Card"
            }
        },
        {
            "type": "reply",
            "reply": {
                "id": "2",
                "title": "Credit Card"
            }
        },
        {
            "type": "reply",
            "reply": {
                "id": "3",
                "title": "Cash"
            }
        }
    ]
    response_send_messages = client.whatsapp.send_whatsapp_interactive_message(originator="+XXXXXXXXXXXX",
                                                                               recipient="XXXXXXXXXXXX",
                                                                               interactive_type="button",
                                                                               header_type="image",
                                                                               header_link="https://karix.s3.ap-south-1.amazonaws.com/English-4.jpg",
                                                                               body_text="Direct7 Networks is a messaging service provider that specializes in helping organizations efficiently communicate with their customers.",
                                                                               footer_text="Thank You",
                                                                               buttons=buttons)

    # interactive list: image

    sections = [
        {
            "title": "SMS Messaging",
            "rows": [
                {
                    "id": "1",
                    "title": "Normal SMS",
                    "description": "Signup for free at the D7 platform to use our Messaging APIs."
                },
                {
                    "id": "2",
                    "title": "Verify",
                    "description": "D7 Verify API is to applications requires SMS based OTP authentications."
                }
            ]
        },
        {
            "title": "Whatsapp",
            "rows": [
                {
                    "id": "3",
                    "title": "WhatsApp Messages",
                    "description": "D7 Whatsapp API is to applications requires pre-registration."
                }
            ]
        }
    ]
    response_send_messages = client.whatsapp.send_whatsapp_interactive_message(originator="+XXXXXXXXXXXX",
                                                                               recipient="XXXXXXXXXXXX",
                                                                               interactive_type="list",
                                                                               header_type="text",
                                                                               header_text="Payment$ for D7 Whatsapp Service",
                                                                               body_text="Direct7 Networks is a messaging service provider that specializes in helping organizations efficiently communicate with their customers.",
                                                                               footer_text="Thank You",
                                                                               list_button_text="Choose Service",
                                                                               sections=sections)

    # Interactive flow

    flowparameter= {
      "name": "flow",
      "parameters": {
        "flow_message_version": "3",
        "flow_token": "unused",
        "flow_id": "530404409952136",
        "flow_cta": "Book Demo",
        "flow_action": "navigate",
        "flow_action_payload": {
          "screen": "screen_"
        }
      }
      }

    response_send_messages = client.whatsapp.send_whatsapp_interactive_message(originator="+XXXXXXXXXXX",
                                                                               recipient="+XXXXXXXXXXX",
                                                                               interactive_type="flow",
                                                                               header_type="text",
                                                                               header_text="Payment$ for D7 Whatsapp Service",
                                                                               body_text="Direct7 Networks is a messaging service provider that specializes in helping organizations efficiently communicate with their customers.",
                                                                               footer_text="Thank You",
                                                                               parameters=flowparameter
                                                                               )

    print(response_send_messages)
    assert response_send_messages is not None
    assert response_send_messages


def test_get_status():
    response_get_status = client.whatsapp.get_status(request_id="00152e17-1717-4568-b793-bd6c729c1ff3")
    print(response_get_status)
    assert response_get_status is not None
    assert response_get_status


def test_read_receipt():
    response_read_receipt = client.whatsapp.read_receipt(message_id="d4056f64-9cdd-11ef-84b3-0242ac1b0027")
    print(response_read_receipt)
    assert response_read_receipt is not None
    assert response_read_receipt


def test_download_media():
    response_download_media = client.whatsapp.download_media(media_id="1645986862789581")
    print(response_download_media)
    assert response_download_media is not None
    assert response_download_media

def test_send_flow_template_message():
    button_flow=[{"flow_token":"unused",
                "action_type":"flow",
                "index":"0",
                "flow_action_data":{}
                }
            ]
    response_data = client.whatsapp.send_whatsapp_templated_message(originator="+XXXXXXXXXXX",
                                                                             recipient="+XXXXXXXXXXX",
                                                                             template_id="benq_owew",
                                                                             language='en_GB',
                                                                             button_flow=button_flow)

if __name__ == "__main__":
    test_send_messages()
    test_send_flow_template_message()
    test_get_status()
    test_read_receipt()
    test_download_media()
