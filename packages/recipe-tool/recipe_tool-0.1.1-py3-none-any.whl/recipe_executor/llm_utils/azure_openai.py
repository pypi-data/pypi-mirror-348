import logging
import os
from typing import Optional

from azure.identity import DefaultAzureCredential, ManagedIdentityCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


def _mask_secret(secret: Optional[str]) -> str:
    """
    Mask a secret, showing only the first and last character.
    """
    if not secret:
        return "<None>"
    if len(secret) <= 2:
        return "**"
    return f"{secret[0]}***{secret[-1]}"


def get_azure_openai_model(
    logger: logging.Logger,
    model_name: str,
    deployment_name: Optional[str] = None,
) -> OpenAIModel:
    """
    Create a PydanticAI OpenAIModel instance, configured from environment variables for Azure OpenAI.

    Args:
        logger (logging.Logger): Logger for logging messages.
        model_name (str): Model name, such as "gpt-4o" or "o4-mini".
        deployment_name (Optional[str]): Azure deployment name; defaults to model_name or env var.

    Returns:
        OpenAIModel: A PydanticAI OpenAIModel instance created from AsyncAzureOpenAI client.

    Raises:
        Exception: If required environment variables are missing or client/model creation fails.
    """
    # Load configuration
    use_managed_identity = os.getenv("AZURE_USE_MANAGED_IDENTITY", "false").lower() in ("1", "true", "yes")
    azure_endpoint = os.getenv("AZURE_OPENAI_BASE_URL")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-03-01-preview")
    env_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_client_id = os.getenv("AZURE_CLIENT_ID")

    if not azure_endpoint:
        logger.error("Environment variable AZURE_OPENAI_BASE_URL is required")
        raise Exception("Missing AZURE_OPENAI_BASE_URL")

    # Determine deployment
    deployment = deployment_name or env_deployment or model_name

    # Log loaded config
    masked_key = _mask_secret(os.getenv("AZURE_OPENAI_API_KEY"))
    logger.debug(
        f"Azure OpenAI config: endpoint={azure_endpoint}, api_version={azure_api_version}, "
        f"deployment={deployment}, use_managed_identity={use_managed_identity}, "
        f"client_id={azure_client_id or '<None>'}, api_key={masked_key}"
    )

    # Create Azure OpenAI client
    try:
        if use_managed_identity:
            logger.info("Using Azure Managed Identity for authentication")
            if azure_client_id:
                credential = ManagedIdentityCredential(client_id=azure_client_id)
            else:
                credential = DefaultAzureCredential()

            token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
            azure_client = AsyncAzureOpenAI(
                azure_ad_token_provider=token_provider,
                azure_endpoint=azure_endpoint,
                api_version=azure_api_version,
                azure_deployment=deployment,
            )
            auth_method = "Azure Managed Identity"
        else:
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            if not api_key:
                logger.error("Environment variable AZURE_OPENAI_API_KEY is required for API key authentication")
                raise Exception("Missing AZURE_OPENAI_API_KEY")
            logger.info("Using API key authentication for Azure OpenAI")
            azure_client = AsyncAzureOpenAI(
                api_key=api_key,
                azure_endpoint=azure_endpoint,
                api_version=azure_api_version,
                azure_deployment=deployment,
            )
            auth_method = "API Key"
    except Exception as err:
        logger.error(f"Failed to create AsyncAzureOpenAI client: {err}")
        raise

    # Wrap in PydanticAI provider and model
    logger.info(f"Creating Azure OpenAI model '{model_name}' with {auth_method}")
    provider = OpenAIProvider(openai_client=azure_client)
    try:
        model = OpenAIModel(model_name=model_name, provider=provider)
    except Exception as err:
        logger.error(f"Failed to create OpenAIModel: {err}")
        raise

    return model
