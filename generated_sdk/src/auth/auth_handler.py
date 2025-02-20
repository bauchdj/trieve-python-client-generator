from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ...models.models import *

if TYPE_CHECKING:
    from ..trieve_api import TrieveApi


class Auth:
    def __init__(self, parent: "TrieveApi"):
        """
        Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API.

        Args:
            parent: The parent client to use for the requests
        """
        self.parent = parent

    def login(
        self,
        organization_id: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        inv_code: Optional[str] = None,
    ) -> Any:
        """
        This will redirect you to the OAuth provider for authentication with email/pass, SSO, Google, Github, etc.

        Args:
            organization_id: ID of organization to authenticate into
            redirect_uri: URL to redirect to after successful login
            inv_code: Code sent via email as a result of successful call to send_invitation

        Returns:
            Response data
        """
        path = f"/api/auth"
        params = {}
        headers = {}
        if organization_id is not None:
            params["organization_id"] = organization_id
        if redirect_uri is not None:
            params["redirect_uri"] = redirect_uri
        if inv_code is not None:
            params["inv_code"] = inv_code
        json_data = None

        response = self.parent._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def logout(
        self,
    ) -> Any:
        """
        Invalidate your current auth credential stored typically stored in a cookie. This does not invalidate your API key.

        Returns:
            Response data
        """
        path = f"/api/auth"
        params = None
        headers = None
        json_data = None

        response = self.parent._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def callback(
        self,
    ) -> Any:
        """
        This is the callback route for the OAuth provider, it should not be called directly. Redirects to browser with set-cookie header.

        Returns:
            Response data
        """
        path = f"/api/auth/callback"
        params = None
        headers = None
        json_data = None

        response = self.parent._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_me(
        self,
    ) -> Any:
        """
        Get the user corresponding to your current auth credentials.

        Returns:
            Response data
        """
        path = f"/api/auth/me"
        params = None
        headers = None
        json_data = None

        response = self.parent._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
