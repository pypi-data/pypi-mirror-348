from fastmcp import FastMCP
import requests
from typing import Optional, Any
import os

mcp = FastMCP(name="Terra Dashboard MCP Server",
              instructions="Use this MCP server to configure your Terra Application", dependencies=["requests"])

BASE_API_URL = "https://api.tryterra.co/v2"

# Set the API key from environment variable
API_KEY = os.getenv("TERRA_API_KEY")
DEV_ID = os.getenv("TERRA_DEV_ID")


def get_default_headers():
    headers = {"X-API-Key": API_KEY, "dev-id": DEV_ID, "User-Agent": "Terra-MCP/1.0.0"}
    return headers


# Get list of available integrations
@mcp.tool()
def terra_get_integrations() -> str:
    """
    Get list of available integrations.

    Returns:
        str: list of available integrations in json format
    """
    data = requests.get(f"{BASE_API_URL}/integrations", headers=get_default_headers())
    return data.json()


# Get detailed list of integrations
@mcp.tool()
def terra_get_detailed_integrations(sdk: Optional[bool] = None) -> str:
    """
    Retrieve a detailed list of supported integrations, filtered by the developer's enabled integrations and the requirement for SDK usage.

    Args:
        sdk (Optional[bool]): If true, allows SDK integrations to be included in the response.
    Returns:
        str: Detailed list of integrations in json format
    """
    params = {}
    if sdk is not None:
        params["sdk"] = sdk

    data = requests.get(
        f"{BASE_API_URL}/integrations/detailed",
        params=params,
        headers=get_default_headers(),
    )
    return data.json()


@mcp.tool()
def get_destinations() -> dict[str, Any]:
    """
    Get destinations.

    Returns:
        dict[str, Any]: list of destinations or destination details for a specific developer
    """
    params = {"dev_id": DEV_ID}

    response = requests.get(
        f"{BASE_API_URL}/dashboard/destinations",
        params=params,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def get_developer_destination_credentials(
    destination: str
) -> dict[str, Any]:
    """
    Get developer destination credentials.

    Args:
        destination (str): The destination to get credentials for

    Returns:
        dict[str, Any]: Destination credentials details
    """
    params = {"destination": destination}

    response = requests.get(
        f"{BASE_API_URL}/dashboard/destinations/credentials",
        params=params,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def delete_destination(
    destination: str, dev_id: Optional[str] = None
) -> dict[str, Any]:
    """
    Delete a destination.

    Args:
        destination (str): The destination to delete
        dev_id (Optional[str]): Developer ID. If not provided, uses the environment variable.

    Returns:
        dict[str, Any]: Response indicating success or failure
    """
    payload = {"dev_id": dev_id or DEV_ID, "destination": destination}

    response = requests.delete(
        f"{BASE_API_URL}/dashboard/destinations",
        json=payload,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def set_destination_state(
    destination: str, active: bool
) -> dict[str, Any]:
    """
    Set destination state (active or inactive).

    Args:
        destination (str): The destination to update
        active (bool): Whether the destination should be active or not

    Returns:
        dict[str, Any]: Response indicating success or failure
    """
    payload = {"dev_id": DEV_ID, "destination": destination, "active": active}

    response = requests.patch(
        f"{BASE_API_URL}/dashboard/destinations",
        json=payload,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def add_developer_destination(
    destination: str,
    scheme: str,
    host: str,
    path: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    port: Optional[int] = None,
    query: Optional[str] = None,
    certificate: Optional[str] = None,
    complete_destination: bool = True,
) -> dict[str, Any]:
    """
    Add developer destination.

    Args:
        destination (str): The destination type to add (e.g. 's3', 'sql', 'webhook')
        scheme (str): The scheme (e.g 's3/postgres/https/mysql')
        host (str): The host (e.g 'webhook.site', 'eu-west-2', 'localhost')
        path (Optional[str]): The path (e.g bucket name, database name, webhook path without leading '/')
        user (Optional[str]): Username for credentials
        password (Optional[str]): Password for credentials
        port (Optional[int]): Port for the service if needed
        query (Optional[str]): Query string if needed
        certificate (Optional[str]): Certificate for certain destinations like GCS
        complete_destination (bool): If true, ping the destination before adding

    Returns:
        dict[str, Any]: Response indicating success or failure
    """
    payload = {
        "destination": destination,
        "dev_id": DEV_ID,
        "scheme": scheme,
        "host": host,
        "complete_destination": complete_destination,
    }

    if path is not None:
        payload["path"] = path
    if user is not None:
        payload["user"] = user
    if password is not None:
        payload["password"] = password
    if port is not None:
        payload["port"] = port
    if query is not None:
        payload["query"] = query
    if certificate is not None:
        payload["certificate"] = certificate

    response = requests.post(
        f"{BASE_API_URL}/dashboard/destinations",
        json=payload,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def ping_developer_destination(
    destination: str,
    scheme: str,
    host: str,
    path: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    port: Optional[int] = None,
    query: Optional[str] = None,
    certificate: Optional[str] = None,
) -> dict[str, Any]:
    """
    Ping a developer destination to check if it's reachable.

    Args:
        destination (str): The destination type to ping
        scheme (str): The scheme (e.g 's3/postgres/https/mysql')
        host (str): The host (e.g 'webhook.site', 'eu-west-2', 'localhost')
        path (Optional[str]): The path (e.g bucket name, database name, webhook path)
        user (Optional[str]): Username for credentials
        password (Optional[str]): Password for credentials
        port (Optional[int]): Port for the service if needed
        query (Optional[str]): Query string if needed
        certificate (Optional[str]): Certificate for certain destinations like GCS

    Returns:
        dict[str, Any]: Response indicating ping success or failure
    """
    payload = {
        "destination": destination,
        "dev_id": DEV_ID,
        "scheme": scheme,
        "host": host,
    }

    if path is not None:
        payload["path"] = path
    if user is not None:
        payload["user"] = user
    if password is not None:
        payload["password"] = password
    if port is not None:
        payload["port"] = port
    if query is not None:
        payload["query"] = query
    if certificate is not None:
        payload["certificate"] = certificate

    response = requests.post(
        f"{BASE_API_URL}/dashboard/destinations/ping",
        json=payload,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def set_provider_keys(
    resource: str,
    client_id: str,
    client_secret: str,
    redirect_url: Optional[str] = None,
) -> dict[str, Any]:
    """
    Set provider keys.

    Args:
        resource (str): The provider resource
        client_id (str): The client ID for the provider
        client_secret (str): The client secret for the provider
        redirect_url (Optional[str]): The redirect URL for the provider

    Returns:
        dict[str, Any]: Response indicating success or failure
    """
    params = {
        "resource": resource,
        "client_id": client_id,
        "client_secret": client_secret,
        "dev_id": DEV_ID,
    }

    if redirect_url:
        params["redirect_url"] = redirect_url

    response = requests.patch(
        f"{BASE_API_URL}/dashboard/providerKeys",
        params=params,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def get_provider_keys(resource: str) -> dict[str, Any]:
    """
    Get provider keys.

    Args:
        resource (str): The provider resource

    Returns:
        dict[str, Any]: Provider key details
    """
    params = {"resource": resource, "dev_id": DEV_ID}

    response = requests.get(
        f"{BASE_API_URL}/dashboard/providerKeys",
        params=params,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def get_developer_providers() -> dict[str, Any]:
    """
    Get developer providers.

    Args:
        None

    Returns:
        dict[str, Any]: list of provider details
    """
    params = {"dev_id": DEV_ID}

    response = requests.get(
        f"{BASE_API_URL}/dashboard/providers",
        params=params,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def add_providers(providers: list[str]) -> dict[str, Any]:
    """
    Add providers.

    Args:
        providers (list[str]): list of providers to add

    Returns:
        dict[str, Any]: Response indicating success or failure
    """
    payload = {"dev_id": DEV_ID, "providers": providers}

    response = requests.post(
        f"{BASE_API_URL}/dashboard/providers",
        json=payload,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def deactivate_provider(provider: str) -> dict[str, Any]:
    """
    Delete provider.

    Args:
        provider (str): The provider to deactivate

    Returns:
        dict[str, Any]: Response indicating success or failure
    """
    payload = {"dev_id": DEV_ID, "provider": provider}

    response = requests.delete(
        f"{BASE_API_URL}/dashboard/providers",
        json=payload,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def set_provider_state(
    provider: str, active: bool
) -> dict[str, Any]:
    """
    Set provider state (active or inactive).

    Args:
        provider (str): The provider to update
        active (bool): Whether the provider should be active or not

    Returns:
        dict[str, Any]: Response indicating success or failure
    """
    payload = {"dev_id": DEV_ID, "provider": provider, "active": active}

    response = requests.patch(
        f"{BASE_API_URL}/dashboard/providers",
        json=payload,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def get_providers_by_popularity() -> dict[str, Any]:
    """
    Get providers ranked by popularity.

    Returns:
        dict[str, Any]: list of providers ranked by popularity
    """
    response = requests.get(
        f"{BASE_API_URL}/dashboard/providers/ranked", headers=get_default_headers()
    )
    return response.json()


@mcp.tool()
def add_custom_credentials(
    provider: str,
    client_id: str,
    client_secret: str,
    redirect_url: Optional[str] = None,
) -> dict[str, Any]:
    """
    Add custom credentials for a provider.

    Args:
        provider (str): The provider to add credentials for
        client_id (str): The client ID
        client_secret (str): The client secret
        redirect_url (Optional[str]): The redirect URL

    Returns:
        dict[str, Any]: Response indicating success or failure
    """
    payload = {
        "provider": provider,
        "client_id": client_id,
        "client_secret": client_secret,
        "dev_id": DEV_ID,
    }

    if redirect_url:
        payload["redirect_url"] = redirect_url

    response = requests.post(
        f"{BASE_API_URL}/dashboard/providers/credentials",
        json=payload,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def get_custom_credentials(
    provider: str
) -> dict[str, Any]:
    """
    Get custom credentials for a provider.

    Args:
        provider (str): The provider to get credentials for

    Returns:
        dict[str, Any]: Provider credential details
    """
    params = {"provider": provider}

    response = requests.get(
        f"{BASE_API_URL}/dashboard/providers/credentials",
        params=params,
        headers=get_default_headers(),
    )
    return response.json()


@mcp.tool()
def search_documentation(
    query: str
) -> dict[str, Any]:
    """
    Search documentation using AI.
    Use this whenever you are unsure about the API or how to use it.
    Ask questions like "How do I build a application that integrates with Terra?" or "What is the best way to integrate with the API?"

    Args:
        query (str): The search query. Written in natural language.
        This will be used to search the documentation.

    Returns:
        str: Response from the AI model.
    """
    params = {"query": query}

    response = requests.post(
        "https://ubd7f3f36wgejf3kvci5647fby0ueuvi.lambda-url.eu-west-1.on.aws",
        json=params,
        headers=get_default_headers(),
    )
    return response.json().get("content", "No response was received.")


@mcp.resource("docs://v5_api")
def get_docs() -> str:
    """Get minifed v5 TerraAPI OpenAPI documentation"""
    URL = "https://raw.githubusercontent.com/tryterra/llms.txt/refs/heads/master/chunked/v5.txt"
    response = requests.get(URL)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError(
            "Failed to fetch documentation. Please check the URL or your network connection."
        )


@mcp.resource("docs://rt_api")
def get_rt_docs() -> str:
    """Get minifed real-time TerraAPI OpenAPI documentation"""
    URL = "https://raw.githubusercontent.com/tryterra/llms.txt/refs/heads/master/chunked/rt.txt"
    response = requests.get(URL)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError(
            "Failed to fetch documentation. Please check the URL or your network connection."
        )

# Check if API key is set


@mcp.resource("config://api_key")
def get_api_key() -> str:
    """Get the API key"""
    if API_KEY:
        return f"API key is set: {API_KEY}"
    else:
        raise ValueError(
            "API key is not set. Please set the TERRA_API_KEY environment variable."
        )


# Check if developer ID is set
@mcp.resource("config://dev_id")
def get_dev_id() -> str:
    """Get the developer ID"""
    if DEV_ID:
        return f"Developer key is set: {DEV_ID}"
    else:
        raise ValueError(
            "Developer ID is not set. Please set the TERRA_DEV_ID environment variable."
        )

# About Terra


@mcp.resource("config://about")
def get_about() -> str:
    """Get about information"""
    return (
        "The Terra API standardizes health and fitness data, allowing you to use it structured and efficient manner, no matter the source."
        "It allows developers to integrate and manage their data sources easily."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
