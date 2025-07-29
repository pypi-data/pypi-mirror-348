# Direct7 Python SDK

Python SDK to seamlessly incorporate communication features into your Python applications via the Direct7 REST API. This SDK empowers you to effortlessly initiate SMS,Whatsapp, Slack, Viber  messages and 2 factor authentication features.

## Documentation
The documentation for the Direct7 REST API can be found here [Direct7 API Reference](https://d7networks.com/docs/).


## Installation

The SDK is available on PyPI and can be installed using `pip`:

```bash
pip install direct7
```


## Usage

To get started you need to have an active Direct7 account, If you haven't yet registered, please proceed to [Sign up](https://app.d7networks.com/signup?tag="direct7-python-sdk")

### Authentication

In order to initiate API requests, create a client object using your Direct7 API token. To obtain an API token, kindly visit the following link: https://app.d7networks.com/api-tokens.

## Examples

  - [SMS](#sms)
  - [Verify](#verify)
  - [Whatsapp](#whatsapp)
  - [Number Lookup](#number-lookup)
  - [Viber](#viber)
  - [Slack](#slack)

### SMS


### Send SMS

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.sms.send_messages(
        {"recipients": ["+9199XXXXXXXX"], "content": "Greetings from D7 API", "unicode": False},
        originator="Sender",
        report_url="https://the_url_to_receive_delivery_report.com",
        schedule_time='2024-02-05T09:48:42+0000',
        )
```

### Send an Unicode SMS

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.sms.send_messages(
        {"recipients": ["+9199XXXXXXXX"],"content": "مرحبا بالعالم!", "unicode": True},
        originator="Sender",
        report_url="https://the_url_to_receive_delivery_report.com",
        )
```

### Check SMS Request Status

```python
from direct7 import Client

client = Client(api_token="Your API token")

# request_id is the id returned in the response of send_message
client.sms.get_status(request_id="0012c7f5-2ba5-49db-8901-4ee9be6dc8d1")
```

### Verify

### Send OTP

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.verify.send_otp(originator="SignOTP", recipient="+97150900XXXX", content = "Greetings from D7 API, your mobile verification code is: {}", expiry = 600, data_coding = "text")
```

### Re-Send OTP

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.verify.resend_otp(otp_id="0012c7f5-2ba5-49db-8901-4ee9be6dc8d1")
```

### Verify OTP

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.verify.verify_otp(otp_id="0012c7f5-2ba5-49db-8901-4ee9be6dc8d1", otp_code="1425")
```

### Check Verify Request Status

```python
from direct7 import Client

client = Client(api_token="Your API token")

# otp_id is the id returned in the response of send_otp
client.verify.get_status(otp_id="0012c7f5-2ba5-49db-8901-4ee9be6dc8d1")
```


### Whatsapp

### Send Whatsapp Free-form Message (Location Details)

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.whatsapp.send_whatsapp_freeform_message(originator="91906152XXXX",
                                               recipient="91906112XXXX",
                                                message_type="LOCATION", latitude="12.93803129081362",
                                                longitude="77.61088653615994",
                                                name="Mobile Pvt Ltd", address="30, Hosur Rd, 7th Block, Koramangala, Bengaluru, Karnataka 560095")
```

### Send Whatsapp Templated Message.

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.whatsapp.send_whatsapp_templated_message(originator="91906152XXXX", recipient="91906112XXXX", template_id="monthly_promotion", language= "en", body_parameter_values={"0": "promotion"})
```

### Send Whatsapp Interactive Message.

```python
from direct7 import Client

client = Client(api_token="Your API token")

parameters = {
    "display_text": "Visit Alpha",
    "url": "https://www.luckyshrub.com?clickID=kqDGWd24Q5TRwoEQTICY7W1JKoXvaZOXWAS7h1P76s0R7Paec4"
}
    
response_send_messages = client.whatsapp.send_whatsapp_interactive_message(originator="+91906152XXXX",
                                                                           recipient="91906112XXXX",
                                                                           interactive_type="cta_url",
                                                                           header_type="text",
                                                                           header_text="Payment$ for D7 Whatsapp Service",
                                                                           body_text="Direct7 Networks is a messaging service provider that specializes in helping organizations efficiently communicate with their customers.",
                                                                           footer_text="Thank You",
                                                                           parameters=parameters)
```

### Check Whatsapp Request Status

```python
from direct7 import Client

client = Client(api_token="Your API token")

# request_id is the id returned in the response of send_message
client.whatsapp.get_status(request_id="0012c7f5-2ba5-49db-8901-4ee9be6dc8d1")
```

### Whatsapp Read Receipt

```python
from direct7 import Client

client = Client(api_token="Your API token")

# request_id is the id returned in the response of send_message
client.whatsapp.read_receipt(message_id="0012c7f5-2ba5-49db-8901-4ee9be6dc8d1")
```

### Whatsapp User Initiated Media Download

```python
from direct7 import Client

client = Client(api_token="Your API token")

# request_id is the id returned in the response of send_message
client.whatsapp.download_media(media_id="16554534343")
```

### Number Lookup

### Search Phone Number Details

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.number_lookup.search_number_details(recipient="+914257845XXXX")
```

### Viber

### Send Viber Message

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.viber.send_viber_message(recipients=["+97150900XXXX","+97845900XXX"], content="Greetings from D7 API", label="PROMOTION", originator="INFO2WAY", call_back_url="https://the_url_to_recieve_delivery_report.com")
```


### Check Viber Request Status

```python
from direct7 import Client

client = Client(api_token="Your API token")

# request_id is the id returned in the response of send_viber_message
client.viber.get_status(request_id="0012c7f5-2ba5-49db-8901-4ee9be6dc8d1")
```

### Slack

### Send Slack Message

```python
from direct7 import Client

client = Client(api_token="Your API token")

client.slack.send_slack_message(content="Greetings from D7 API", work_space_name="WorkspaceName", channel_name="ChannelName", report_url="https://the_url_to_recieve_delivery_report.com")
```


### Check Slack Request Status

```python
from direct7 import Client

client = Client(api_token="Your API token")

# request_id is the id returned in the response of send_slack_message
client.slack.get_status(request_id="0012c7f5-2ba5-49db-8901-4ee9be6dc8d1")
```


## FAQ

### How do I get my API token?

You can get your API token from the Direct7 dashboard. If you don't have an account yet, you can create one for free.

### Supported Python versions

The SDK supports Python 3.6 and higher.

### Supported APIs

As of now, the SDK supports the following APIs:

| API                    |        Supported?        |
|------------------------|:------------------------:|
| SMS API                |            ✅             |
| Verify API             |            ✅             |
| Whatsapp API           |            ✅             |
| Number Lookup API      |            ✅             |
| Viber API              |            ✅             |
| Slack API              |            ✅             |

### How do I get started?

You can find the platform documentation @ [Direct7 Docs](https://d7networks.com/docs/).

### How do I get help?

If you need help using the SDK, you can create an issue on GitHub or email to support@d7networks.com

## Contributing

We welcome contributions to the Direct7 Python SDK. If you have any ideas for improvements or bug fixes, please feel
free to create an issue on GitHub.
