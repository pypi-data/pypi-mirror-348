# Naxai Python SDK

## Overview

The Naxai Python SDK provides a simple and intuitive way to interact with Naxai's APIs. This SDK offers both synchronous and asynchronous clients for accessing various Naxai services including Voice, SMS, Email, Calendars, and People APIs.

⚠️ This SDK is a work in progress. Features and APIs may change until the release of version 1.0.0.

## Table of Contents

- [Installation](#installation)
- [Client Initialization](#client-initialization)
  - [Example 1: Explicit Parameters](#example-1-initializing-with-explicit-parameters)
  - [Example 2: Environment Variables](#example-2-initializing-with-environment-variables)
- [Environment Variables](#environment-variables)
- [Authentication](#authentication)
- [Client Structure](#client-structure)
- [Available Resources](#available-resources)
  - [Voice API](#voice-api)
  - [SMS API](#sms-api)
  - [Email API](#email-api)
  - [Calendars API](#calendars-api)
  - [People API](#people-api)
  - [Webhooks API](#webhooks-api)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Resource Cleanup](#resource-cleanup)
- [Examples](#examples)
  - [Voice Call Example](#voice-call-example)
  - [Calendar Event Example](#calendar-event-example)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Installation

Install the Naxai SDK using pip:

```bash
pip install naxai
```

## Client Initialization

The Naxai SDK provides two client types:
- `NaxaiClient` - Synchronous client
- `NaxaiAsyncClient` - Asynchronous client

Both clients offer the same functionality but with different programming paradigms.

### Example 1: Initializing with Explicit Parameters

You can initialize the client by explicitly providing all required parameters:

```python
# For synchronous client
from naxai.client import NaxaiClient

client = NaxaiClient(
    api_client_id="your_client_id",
    api_client_secret="your_client_secret",
    api_version="2023-03-25",
    auth_url="https://auth.naxai.com/oauth2/token",
    api_base_url="https://api.naxai.com"
)

# Use the client
response = client.voice.call.create(language="en-GB",
                                    to=["XXXXXXXXXX"],
                                    from_="XXXXXXXX",
                                    welcome={"say": "Hello this is a test from the Naxai SDK."})
print(response)

# Always close the client when done
client.close()
```

```python
# For asynchronous client
import asyncio
from naxai.async_client import NaxaiAsyncClient

async def main():
    client = NaxaiAsyncClient(
        api_client_id="your_client_id",
        api_client_secret="your_client_secret",
        api_version="v1",
        auth_url="https://auth.naxai.com/oauth2/token",
        api_base_url="https://api.naxai.com"
    )

    # Use the client
    response = await client.voice.call.create(language="en-GB",
                                              to=["XXXXXXXXXX"],
                                              from_="XXXXXXXX",
                                              welcome={"say": "Hello this is a test from the Naxai SDK."})
    print(response)

    # Always close the async client when done
    await client.aclose()

asyncio.run(main())
```

### Example 2: Initializing with Environment Variables

You can also initialize the client using environment variables, which is useful for keeping sensitive information out of your code:

```bash
# Set these environment variables in your system or .env file
export NAXAI_CLIENT_ID="your_client_id"
export NAXAI_SECRET="your_client_secret"
export NAXAI_AUTH_URL="https://auth.naxai.com/oauth2/token"  # Optional, has default value
export NAXAI_API_URL="https://api.naxai.com"  # Optional, has default value
export NAXAI_API_VERSION="2023-03-25"  # Optional, has default value
```

Then in your code:

```python
# For synchronous client
from naxai.client import NaxaiClient

# The client will automatically use environment variables
client = NaxaiClient()

# Use the client
response = client.voice.call.create(language="en-GB",
                                    to=["XXXXXXXXXX"],
                                    from_="XXXXXXXX",
                                    welcome={"say": "Hello this is a test from the Naxai SDK."})
print(response)

# Always close the client when done
client.close()
```

```python
# For asynchronous client
import asyncio
from naxai.async_client import NaxaiAsyncClient

async def main():
    # The client will automatically use environment variables
    client = NaxaiAsyncClient()

    # Use the client
    response = await client.voice.call.create(language="en-GB",
                                              to=["XXXXXXXXXX"],
                                              from_="XXXXXXXX",
                                              welcome={"say": "Hello this is a test from the Naxai SDK."})
    print(response)

    # Always close the async client when done
    await client.aclose()

asyncio.run(main())
```

## Environment Variables

The SDK looks for the following environment variables:

| Environment Variable | Description | Default Value |
|---------------------|-------------|---------------|
| `NAXAI_CLIENT_ID` | Your Naxai API client ID | None (Required) |
| `NAXAI_SECRET` | Your Naxai API client secret | None (Required) |
| `NAXAI_AUTH_URL` | Authentication URL | https://auth.naxai.com/oauth2/token |
| `NAXAI_API_URL` | API base URL | https://api.naxai.com |
| `NAXAI_API_VERSION` | API version to use | 2023-03-25 |

## Authentication

Authentication is handled automatically by the SDK:

- When you first perform an API action, the SDK authenticates using the provided credentials
- The access token is stored and automatically refreshed when needed (valid for 24 hours)
- You don't need to manage tokens manually

The SDK uses the OAuth 2.0 client credentials flow for authentication.

## Client Structure

The main entry points to the SDK are:

```python
from naxai.client import NaxaiClient       # Synchronous client
from naxai.async_client import NaxaiAsyncClient  # Asynchronous client
```


## Available Resources

### Voice API

The Voice API allows you to create and manage voice calls:

```python
# Create a voice call
from naxai.models.voice.voice_flow import Welcome, End
import uuid
import datetime

welcome = Welcome(say="Welcome to the Naxai demo")
end = End(say="Thank you for using the Naxai demo")

# Synchronous
response = client.voice.call.create(to=["123456789"],
                                    from_="123456789",
                                    language="en-GB",
                                    welcome=welcome,
                                    end=end)

# Asynchronous
response = await client.voice.call.create(to=["123456789"],
                                          from_="123456789",
                                          language="en-GB",
                                          welcome=welcome,
                                          end=end)

```

### SMS API

The SMS API allows you to send text messages:

```python
# Send an SMS
sms_request = {
    "to": ["123456789"],
    "from": "1234",
    "body": "Hello from Naxai SDK!"
}

# Synchronous
response = client.sms.send(to=["123456789"],
                           from_="1234",
                           body="Hello from Naxai SDK!")

# Asynchronous
response = await client.sms.send(to=["123456789"],
                                 from_="1234",
                                 body="Hello from Naxai SDK!")
```

### Email API

The Email API allows you to send emails:

```python
# Send an email
email_request = {
    "to": ["recipient@example.com"],
    "from": "sender@example.com",
    "subject": "Hello from Naxai",
    "text": "This is a test email from Naxai SDK",
    "html": "<p>This is a test email from Naxai SDK</p>"
}

# Synchronous
response = client.email.send(data=email_request)

# Asynchronous
response = await client.email.send(data=email_request)
```

### Calendars API

The Calendars API allows you to manage calendar events:

```python
# Create a calendar event
schedules = [ScheduleObject(
        day = 1,
        open=True,
        start="10:00",
        stop="17:59",
        extended=False
    ),
    ScheduleObject(
        day = 2,
        open=True,
        start="10:00",
        stop="17:59",
        extended=False
    ),
    ScheduleObject(
        day = 3,
        open=True,
        start="10:00",
        stop="17:59",
        extended=False
    ),
    ScheduleObject(
        day = 4,
        open=True,
        start="10:00",
        stop="17:59",
        extended=False
    ),
    ScheduleObject(
        day = 5,
        open=True,
        start="10:00",
        stop="17:59",
        extended=False
    ),
    ScheduleObject(
        day = 6,
        open=False
    ),
    ScheduleObject(
        day = 7,
        open = False
    )]

    calendar = CreateCalendarRequest(
        name="Test Calendar from SDK",
        timezone="Europe/Brussels",
        schedule=schedules
    )

# Synchronous
response = client.calendars.create(data=calendar)

# Asynchronous
response = await client.calendars.create(data=calendar)
```

### People API ( Coming soon )

The People API allows you to manage contacts:

```python
# Create a contact
contact_request = {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890"
}

# Synchronous
response = client.people.create(data=contact_request)

# Asynchronous
response = await client.people.create(data=contact_request)
```

### Webhooks API

The Webhooks API allows you to manage webhooks:

```python
# List all webhooks
response = client.webhooks.list()
```

## Error Handling

All exceptions inherit from `NaxaiException`:

```python
from naxai.base.exceptions import NaxaiException, NaxaiAuthenticationError

try:
    response = client.voice.call.create(data=call_request)
except NaxaiAuthenticationError as e:
    print(f"Authentication failed: {e}")
except NaxaiException as e:
    print(f"API call failed: {e}")
```

Common exceptions include:

| Exception | When it Happens |
|-----------|-----------------|
| `NaxaiAuthenticationError` | Authentication failed (401) |
| `NaxaiAuthorizationError` | Access forbidden (403) |
| `NaxaiResourceNotFound` | Resource not found (404) |
| `NaxaiInvalidRequestError` | Invalid request parameters (422) |
| `NaxaiRateLimitExceeded` | Rate limit hit (429) |
| `NaxaiAPIRequestError` | Generic API error |
| `NaxaiValueError` | Incorrect parameter value |

## Logging

The SDK supports custom logging. Pass your own logger into the client to integrate with your application's logging system:

```python
import logging

# Configure your logger
logger = logging.getLogger("naxai")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Pass the logger to the client
client = NaxaiClient(
    api_client_id="your_client_id",
    api_client_secret="your_client_secret",
    logger=logger
)
```

## Resource Cleanup

Always close the HTTP session after usage to properly release network resources:

```python
# Synchronous client
client.close()

# Asynchronous client
await client.aclose()
```

For asynchronous clients, it's recommended to use them as context managers:

```python
async with NaxaiAsyncClient(
    api_client_id="your_client_id",
    api_client_secret="your_client_secret"
) as client:
    response = await client.voice.call.create(data=call_request)
    print(response)
    # No need to call aclose() when using as context manager
```

## Examples

### Voice Call Example

```python
import asyncio
import uuid
import datetime
from naxai import NaxaiAsyncClient
from naxai.models.voice.voice_flow import Welcome, End

async def make_voice_call():
    client = NaxaiAsyncClient(
        api_client_id="your_client_id",
        api_client_secret="your_client_secret"
    )
    
    try:
        # Create a simple voice flow
        welcome = Welcome(say="Welcome to the Naxai demo")
        end = End(say="Thank you for using the Naxai demo")
        
        # Make the API call
        response = await client.voice.call.create(welcome=welcome,
                                                  end=end,
                                                  to=["+1234567890"],
                                                  from_="+0987654321",
                                                  language="en-GB")
        print(f"Call created successfully: {response}")
        
    except Exception as e:
        print(f"Error creating call: {e}")
    finally:
        await client.aclose()

# Run the async function
asyncio.run(make_voice_call())
```

### Calendar Event Example

```python
from naxai import NaxaiClient
import datetime

# Initialize the client
client = NaxaiClient(
    api_client_id="your_client_id",
    api_client_secret="your_client_secret"
)

try:
    # Create a calendar event
    start_time = datetime.datetime.now() + datetime.timedelta(days=1)
    end_time = start_time + datetime.timedelta(hours=1)
    
    event_request = {
        "summary": "Project Review Meeting",
        "description": "Quarterly project review with the team",
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "UTC"
        },
        "attendees": [
            {"email": "team.member1@example.com"},
            {"email": "team.member2@example.com"}
        ],
        "location": "Conference Room A"
    }
    
    response = client.calendars.create(data=event_request)
    print(f"Calendar event created: {response}")
    
except Exception as e:
    print(f"Error creating calendar event: {e}")
finally:
    client.close()
```

## Roadmap

- ✅ Add Voice resource
- ✅ Add Calendars resource
- ✅ Add Email resource (partially implemented. Some methods are not working)
- ✅ Add SMS resource
- ✅ Add People resource
- ✅ Provide a client for synchronous code
- ✅ Publish SDK on PyPI
- ✅ Improve type hints for auto-completion and IDE support
- ✅ Webhooks
- ✅ Add comprehensive test suite
- 🚧 Add more examples and use cases

## Contributing

Contributions to the Naxai Python SDK are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.