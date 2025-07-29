from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from abs_integration_core.schema import TokenData, Integration
from abs_integration_core.repository import IntegrationRepository
from abs_exception_core.exceptions import NotFoundError
from abs_repository_core.services.base_service import BaseService
from abs_integration_core.utils.encryption import Encryption
from datetime import datetime, timedelta, UTC


class IntegrationBaseService(ABC, BaseService):
    """
    Base abstract class for all integration services.
    Any integration service should inherit from this class and implement its methods.
    """
    def __init__(
        self, 
        provider_name: str, 
        integration_repository: IntegrationRepository,
        encryption: Encryption
    ):
        self.provider_name = provider_name
        self.encryption = encryption
        super().__init__(integration_repository)

    @abstractmethod
    def get_auth_url(self, state: Optional[Dict] = None) -> Dict[str, str]:
        """
        Generate an authentication URL for OAuth flow.
        
        Args:
            state: Optional state dictionary to include in the OAuth flow
        
        Returns:
            A dictionary containing the auth URL and other necessary information
        """
        pass

    @abstractmethod
    async def get_token_data(self, code: str) -> TokenData:
        """
        Exchange authorization code for token data.
        
        Args:
            code: The authorization code from OAuth callback
            
        Returns:
            TokenData object with access_token, refresh_token and expires_in
        """
        pass

    @abstractmethod
    async def handle_oauth_callback(self, code: str) -> TokenData:
        """
        Handle the OAuth callback and store tokens.
        
        Args:
            code: The authorization code from OAuth callback
            
        Returns:
            TokenData object
        """
        pass

    @abstractmethod
    async def refresh_token(self) -> Optional[TokenData]:
        """
        Refresh the access token using the refresh token.
        
        Returns:
            Updated TokenData if successful, None otherwise
        """
        pass

    async def _verify_access_token(self, token_data: TokenData) -> TokenData:
        """
        Verify the access token and refresh it if it's close to expiration.
        
        Args:
            token_data: The token data to verify
        
        Returns:
            TokenData object - either the original if valid or a refreshed one
        """
        current_time = datetime.now(UTC)
        buffer_minutes = 5
        expiration_buffer = current_time + timedelta(minutes=buffer_minutes)
        
        # Ensure token_data.expires_at is also timezone-aware
        if token_data.expires_at.tzinfo is None:
            token_data.expires_at = token_data.expires_at.replace(tzinfo=UTC)

        if token_data.expires_at <= expiration_buffer:
            return await self.refresh_token()
        
        return token_data

    async def get_integration_tokens(self) -> TokenData:
        """
        Get the integration tokens.
        """
        result = self.get_query_by_provider()

        tokens = TokenData(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            expires_at=result.expires_at
        )

        return await self._verify_access_token(tokens)

    def get_query_by_provider(self):
        return super().get_by_attr(
            attr="provider_name",
            value=self.provider_name
        )

    def get_integration(self) -> Optional[TokenData]:
        """
        Get integration data.
        
        Returns:
            TokenData if integration exists, None otherwise
        """
        try:
            integration = self.get_query_by_provider()
            return integration
        except Exception:
            return None

    def get_all_integrations(self) -> List[Integration]:
        """
        Get all integrations.
        
        Returns:
            List of TokenData objects
        """
        try:
            integrations = super().get_list()
            return integrations
        except Exception:
            return []

    def delete_integration(self) -> bool:
        """
        Delete an integration.
        
        Returns:
            True if deleted, False otherwise
        """
        try:
            integration = self.get_query_by_provider()
            super().remove_by_id(integration.id)

            return True

        except NotFoundError:
            # If the integration doesn't exist, consider it "deleted"
            return True

        except Exception as e:
            print(f"Error deleting integration: {str(e)}")
            return False
