from typing import List, Optional

from google import auth
from google.auth import impersonated_credentials
from google.oauth2 import service_account
from loguru import logger

from .config import settings


def get_credentials(
    project_id: Optional[str] = None,
    impersonate_service_account: Optional[str] = None,
    scopes: Optional[List[str]] = None,
    lifetime: Optional[int] = None,
) -> auth.credentials.Credentials:
    """Get the credentials based on settings."""
    logger.debug(
        f"Getting credentials. Project: {settings.GOOGLE_CLOUD_PROJECT_ID}, "
        f"Impersonate SA: {settings.IMPERSONATE_SERVICE_ACCOUNT}, "
        f"SA Key Path: {settings.SOURCE_SA_KEY_PATH}"
    )

    current_project_id = project_id if project_id else settings.GOOGLE_CLOUD_PROJECT_ID
    current_impersonate_sa = (
        impersonate_service_account
        if impersonate_service_account
        else settings.IMPERSONATE_SERVICE_ACCOUNT
    )
    current_sa_key_path = settings.SOURCE_SA_KEY_PATH

    if current_impersonate_sa:
        logger.info(f"Impersonation is configured for SA: {current_impersonate_sa}")
        return get_impersonate_credentials(
            target_sa_email=current_impersonate_sa,
            source_sa_key_path=current_sa_key_path,
            quota_project_id=current_project_id,
            scopes=scopes,
            lifetime=lifetime,
        )

    logger.info("No impersonation. Using direct credentials.")
    if current_sa_key_path:
        logger.info(f"Using service account key from: {current_sa_key_path}")
        try:
            credentials = service_account.Credentials.from_service_account_file(
                current_sa_key_path,
                scopes=scopes
                if scopes
                else ["https://www.googleapis.com/auth/cloud-platform"],
            )
            # quota_project_id を設定できる場合は設定する
            if current_project_id and hasattr(credentials, "with_quota_project"):
                credentials = credentials.with_quota_project(current_project_id)
            logger.debug("Successfully loaded credentials from SA key file.")
            return credentials
        except FileNotFoundError:
            logger.error(f"Service account key file not found: {current_sa_key_path}")
            raise
        except Exception as e:
            logger.error(
                f"Failed to load credentials from SA key file {current_sa_key_path}: {e}"
            )
            raise

    logger.info("No SA key path provided. Falling back to default ADC.")
    return get_default_credentials(current_project_id)


def get_default_credentials(
    project_id: Optional[str] = None,
) -> auth.credentials.Credentials:
    """Get the default credentials (ADC)."""
    logger.debug(f"Getting default ADC. Quota project: {project_id}")
    try:
        if project_id is not None:
            credentials, _ = auth.default(quota_project_id=project_id)
        else:
            credentials, _ = auth.default()
        logger.debug("Successfully obtained default ADC.")
        return credentials
    except Exception as e:
        logger.error(f"Failed to get default ADC: {e}")
        raise Exception(f"Failed to obtain default ADC: {e}") from e


def get_impersonate_credentials(
    target_sa_email: str,
    source_sa_key_path: Optional[str] = None,
    quota_project_id: Optional[str] = None,
    scopes: Optional[List[str]] = None,
    lifetime: Optional[int] = None,
) -> impersonated_credentials.Credentials:
    """Get impersonated credentials."""
    logger.debug(
        f"Getting impersonated credentials for target SA: {target_sa_email}. "
        f"Source SA key path: {source_sa_key_path}, Quota project: {quota_project_id}"
    )

    if scopes is None:
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    if lifetime is None:
        lifetime = 3600

    source_credentials: auth.credentials.Credentials

    if source_sa_key_path:
        logger.info(f"Using source SA key from {source_sa_key_path} for impersonation.")
        try:
            source_credentials = service_account.Credentials.from_service_account_file(
                source_sa_key_path,
            )
            if quota_project_id and hasattr(source_credentials, "with_quota_project"):
                source_credentials = source_credentials.with_quota_project(
                    quota_project_id
                )
            logger.debug(
                "Successfully loaded source credentials from SA key file for impersonation."
            )
        except FileNotFoundError:
            logger.error(
                f"Source SA key file not found for impersonation: {source_sa_key_path}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Failed to load source SA key {source_sa_key_path} for impersonation: {e}"
            )
            raise
    else:
        logger.info(
            "No source SA key path provided for impersonation. Falling back to default ADC."
        )
        try:
            if quota_project_id is not None:
                source_credentials, _ = auth.default(quota_project_id=quota_project_id)
            else:
                source_credentials, _ = auth.default()
            logger.debug(
                "Successfully obtained default ADC as source for impersonation."
            )
        except Exception as e:
            logger.error(f"Failed to get default ADC as source for impersonation: {e}")
            raise

    logger.debug(f"Creating impersonated credentials for target: {target_sa_email}")
    try:
        target_credentials = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=target_sa_email,
            target_scopes=scopes,
            lifetime=lifetime,
        )
        logger.info("Successfully created impersonated credentials.")
        return target_credentials
    except Exception as e:
        logger.error(
            f"Failed to create impersonated credentials for {target_sa_email}: {e}"
        )
        raise
