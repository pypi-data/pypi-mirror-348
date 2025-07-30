# `stravawizard`

## Purpose

This package offers 2 clients to work with the Strava API:

* `stravauth_client`: Allows users to easily handle Strava OAuth authentication. Requires credentials of a declared Strava app (client ID, client secret, and redirect URI) to work properly.
* `strava_api_client`: Allows users to directly use the Strava API, given an access token.

## Installation

```bash
pip install stravawizard
```

## Usage

### Working with `stravauth_client`

The `stravauth_client` provides a complete OAuth flow implementation to authenticate with Strava's API. It consists of three main components:

* `StravauthClient`: The main client that orchestrates the authentication process
* `StravauthCredentialsManager`: Manages application credentials
* `StravauthTokenManager`: Handles OAuth tokens, including validation and refreshing

#### Basic Authentication Flow

```python
from stravawizard.clients.oauth_client.stravauth_client import StravauthClient

# Initialize the client
client = StravauthClient()

# Set app credentials using the credentials manager
client.credentials_manager.set_app_credentials(
    client_id="your_client_id", 
    client_secret="your_client_secret", 
    redirect_uri="your_redirect_uri"
)

# Check if client is ready before proceeding
client.check_if_ready()  # Raises exception if not ready

# Generate authorization URL for user to approve access
auth_url = client.get_authorization_url()
# Redirect your user to this URL in your application

# After user approval, exchange the authorization code received via the redirect URI
response = client.exchange_authorization_code("received_authorization_code")
# The response includes athlete data and OAuth tokens that are stored automatically

# Get athlete summary that was obtained during authentication
athlete = client.get_athlete_summary()
```

#### Working with Tokens

The token manager handles token lifecycle management:

```python
# Check if access token is still valid
if not client.token_manager.is_access_token_valid():
    # Automatically refresh the token using the stored refresh token
    client.token_manager.refresh_access_token()

# Get current user tokens (to use with strava_api_client or store in database)
credentials = client.token_manager.get_user_oauth_credentials()
access_token = credentials["access_token"]
refresh_token = credentials["refresh_token"]
expires_at = credentials["expires_at"]

# Set tokens from an existing user object (e.g., from database)
class User:
    def __init__(self):
        self.strava_access_token = "access_token"
        self.strava_refresh_token = "refresh_token"
        self.strava_expires_at = 1678901234  # Unix timestamp

user = User()
client.token_manager.set_user_oauth_credentials_from_user(user)
```

### Working with `strava_api_client`

```python
from stravawizard.clients.api_client.strava_api_client import StravaApiClient

# Initialize client with or without token
client = StravaApiClient()
# or
client = StravaApiClient(strava_access_token="your_access_token")

# You can also set the token after initialization
client.set_strava_access_token("your_access_token")

# Make sure your client is ready before making calls
is_ready = client.check_if_ready()
```

#### Athlete Data

Retrieve athlete information using the athlete namespace:

```python
# Get athlete stats
athlete_id = 1234567
stats = client.athlete.get_athlete_stats(athlete_id)
```

#### Activity Data

Access activities and related data using the activity namespace:

```python
# Get athlete activities (defaults to most recent 10)
activities = client.activity.get_athlete_activities()

# Get specific page with custom page size
activities = client.activity.get_athlete_activities(page="2", per_page="30")

# Get activities within a date range
from datetime import datetime, timedelta
end_date = datetime.now()
start_date = end_date - timedelta(days=30)  # Last 30 days
activities = client.activity.get_athlete_activities(
    start_date=start_date, 
    end_date=end_date
)

# Get photos for a specific activity
activity_id = 1234567890
photos = client.activity.get_activity_photos(activity_id, size=600)
```

## Architecture

StravaWizard is organized into specialized clients for different purposes:

### OAuth Authentication (`stravauth_client`)

* `StravauthClient`: Main client that orchestrates the OAuth authentication flow
* `StravauthCredentialsManager`: Manages application credentials (client ID, client secret, redirect URI)
* `StravauthTokenManager`: Handles OAuth tokens, their validation, and refreshing
* `StravauthBaseClient`: Base class with common OAuth functionality

### Strava API Access (`strava_api_client`)

* `StravaApiClient`: Main client that integrates all specialized API clients
* `StravaAthleteApiClient`: Handles athlete-related endpoints
* `StravaActivityApiClient`: Handles activity-related endpoints
* `StravaBaseApiClient`: Base class for API clients
* `StravaRequestHandler`: Manages HTTP requests to the Strava API

## Integration Flow

A typical workflow using both clients would be:

1. Use `stravauth_client` to authenticate the user and obtain tokens
2. Use those tokens with `strava_api_client` to make API calls

```python
from stravawizard.clients.oauth_client.stravauth_client import StravauthClient
from stravawizard.clients.api_client.strava_api_client import StravaApiClient

# First, authenticate with stravauth_client
auth_client = StravauthClient()
auth_client.credentials_manager.set_app_credentials(
    client_id="your_client_id", 
    client_secret="your_client_secret", 
    redirect_uri="your_redirect_uri"
)

# Generate an authorization URL and redirect the user
auth_url = auth_client.get_authorization_url()
# (User authorizes via the browser...)

# Exchange the authorization code received via redirect
auth_client.exchange_authorization_code("received_code")

# Retrieve tokens for API usage
tokens = auth_client.token_manager.get_user_oauth_credentials()

# Now use the strava_api_client with the obtained token
api_client = StravaApiClient(strava_access_token=tokens["access_token"])
api_client.check_if_ready()

# Make API calls
activities = api_client.activity.get_athlete_activities()
```

## Error Handling

### API Client Errors

API calls through `StravaApiClient` will return error information in the response:

```python
response = api_client.activity.get_athlete_activities()
if "error" in response:
    print(f"Error occurred: {response['error']}")
else:
    # Process successful response
    pass
```

### OAuth Client Errors

The `StravauthClient` uses exceptions for error handling:

```python
try:
    # Check if all required credentials are set
    auth_client.check_if_ready()
    
    # Attempt to refresh an expired token
    auth_client.token_manager.refresh_access_token()
except Exception as e:
    print(f"Authentication error: {str(e)}")
```

## Requirements

* Python 3.6+
* requests library

## Common Usage Patterns

### Storing and Reusing Tokens

In most applications, you'll want to store the OAuth tokens in a database:

```python
# After authentication
tokens = auth_client.token_manager.get_user_oauth_credentials()

# Store in your database
user.strava_access_token = tokens["access_token"]
user.strava_refresh_token = tokens["refresh_token"]
user.strava_expires_at = tokens["expires_at"]
user.save()

# Later, when loading from database
auth_client = StravauthClient()
auth_client.credentials_manager.set_app_credentials(...)
auth_client.token_manager.set_user_oauth_credentials_from_user(user)

# Check and refresh token if needed
if not auth_client.token_manager.is_access_token_valid():
    auth_client.token_manager.refresh_access_token()
    # Update tokens in database
    user.strava_access_token = auth_client.token_manager.get_user_oauth_credentials()["access_token"]
    user.strava_refresh_token = auth_client.token_manager.get_user_oauth_credentials()["refresh_token"]
    user.strava_expires_at = auth_client.token_manager.get_user_oauth_credentials()["expires_at"]
    user.save()
```

## Updating package on pypi.org

### For maintainers only

Update version to the update's date in `pyproject.toml` according to YYYY.MM.DD format (e.g., `2024.02.05` for a package made on February 5th, 2024. Versions under development should follow this standard, and add `.dev` at the end. For instance: `2024.02.05.dev`).

```bash
python -m build
python3 -m twine upload dist/*
```
