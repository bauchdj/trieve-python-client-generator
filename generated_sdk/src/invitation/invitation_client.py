from typing import Any, Dict, List, Optional, Union
from src.trieve_api_client import TrieveAPIClient
from models.models import *

class InvitationClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def post_invitation(
        self,
        tr_organization: str,
        app_url: str,
        email: str,
        redirect_uri: str,
        user_role: int,
    ) -> Any:
        """
        Invitations act as a way to invite users to join an organization. After a user is invited, they will automatically be added to the organization with the role specified in the invitation once they set their. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_organization: The organization id to use for the request
            app_url: The url of the app that the user will be directed to in order to set their password. Usually admin.trieve.ai, but may differ for local dev or self-hosted setups.
            email: The email of the user to invite. Must be a valid email as they will be sent an email to register.
            redirect_uri: The url that the user will be redirected to after setting their password.
            user_role: The role the user will have in the organization. 0 = User, 1 = Admin, 2 = Owner.

        Returns:
            Response data
        """
        path = f"/api/invitation"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = {
            "app_url": app_url if app_url is not None else None,
            "email": email if email is not None else None,
            "redirect_uri": redirect_uri if redirect_uri is not None else None,
            "user_role": user_role if user_role is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def delete_invitation(
        self,
        tr_organization: str,
        invitation_id: str,
    ) -> Any:
        """
        Delete an invitation by id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_organization: The organization id to use for the request
            invitation_id: The id of the invitation to delete

        Returns:
            Response data
        """
        path = f"/api/invitation/{invitation_id}"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = None

        response = self._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_invitations(
        self,
        tr_organization: str,
        organization_id: str,
    ) -> Any:
        """
        Get all invitations for the organization. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_organization: The organization id to use for the request
            organization_id: The organization id to get invitations for

        Returns:
            Response data
        """
        path = f"/api/invitations/{organization_id}"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
