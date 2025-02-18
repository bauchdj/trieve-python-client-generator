from typing import Any, Dict, List, Optional, Union
from src.trieve_api_client import TrieveAPIClient
from models.models import *

class StripeClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def create_setup_checkout_session(
        self,
        organization_id: str,
    ) -> Any:
        """Create a checkout session (setup)

        Args:
            organization_id: The id of the organization to create setup checkout session for.

        Returns:
            Response data
        """
        path = f"/api/stripe/checkout/setup/{organization_id}"
        params = {}
        headers = {}
        json_data = None

        response = self._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_all_invoices(
        self,
        organization_id: str,
    ) -> Any:
        """Get a list of all invoices

        Args:
            organization_id: The id of the organization to get invoices for.

        Returns:
            Response data
        """
        path = f"/api/stripe/invoices/{organization_id}"
        params = {}
        headers = {}
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def direct_to_payment_link(
        self,
        plan_id: str,
        organization_id: str,
    ) -> Any:
        """Get a 303 SeeOther redirect link to the stripe checkout page for the plan and organization

        Args:
            plan_id: id of the plan you want to subscribe to
            organization_id: id of the organization you want to subscribe to the plan

        Returns:
            Response data
        """
        path = f"/api/stripe/payment_link/{plan_id}/{organization_id}"
        params = {}
        headers = {}
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_all_plans(
        self,
    ) -> Any:
        """Get a list of all plans

        Returns:
            Response data
        """
        path = f"/api/stripe/plans"
        params = None
        headers = None
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def cancel_subscription(
        self,
        tr_organization: str,
        subscription_id: str,
    ) -> Any:
        """Cancel a subscription by its id

        Args:
            tr_organization: The organization id to use for the request
            subscription_id: id of the subscription you want to cancel

        Returns:
            Response data
        """
        path = f"/api/stripe/subscription/{subscription_id}"
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

    def update_subscription_plan(
        self,
        tr_organization: str,
        subscription_id: str,
        plan_id: str,
    ) -> Any:
        """Update a subscription to a new plan

        Args:
            tr_organization: The organization id to use for the request
            subscription_id: id of the subscription you want to update
            plan_id: id of the plan you want to subscribe to

        Returns:
            Response data
        """
        path = f"/api/stripe/subscription_plan/{subscription_id}/{plan_id}"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = None

        response = self._make_request(
            method="PATCH",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
