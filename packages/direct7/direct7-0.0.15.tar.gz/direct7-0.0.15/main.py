from direct7 import Client

if __name__ == "__main__":
    client = Client(api_token="Your API Token")

response_send_messages = client.whatsapp.send_whatsapp_freeform_message(originator="XXXXXXXXXXXX",
                                                                            recipient="XXXXXXXXXXXX",
                                                                            message_type="TEXT", body="Hi")
print(response_send_messages)
