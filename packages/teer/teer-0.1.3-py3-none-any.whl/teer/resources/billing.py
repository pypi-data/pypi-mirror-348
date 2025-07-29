# SPDX-FileCopyrightText: 2025-present Shane Rogers <shane@teer.ai>
#
# SPDX-License-Identifier: MIT

from typing import (
    Dict,
    Any,
    Optional,
    Union,
    TypedDict,
    Literal,
    TYPE_CHECKING,
    NotRequired,
)
from .base import BaseResource

if TYPE_CHECKING:
    from .. import TeerClient


# Billing provider type
BillingProvider = Literal["stripe"]


# Common billing fields without the meter/meters
class BillingFieldsBase(TypedDict):
    """Base interface for billing fields"""

    customer: str
    email: NotRequired[str]


# Single meter option
class SingleMeterFields(BillingFieldsBase):
    """Billing fields with a single meter"""

    meter: str


# Multiple meters option
class MultiMeterFields(BillingFieldsBase):
    """Billing fields with multiple meters"""

    meters: Dict[str, str]


# Union type that allows either single meter or multiple meters
BillingFields = Union[SingleMeterFields, MultiMeterFields]


class TeerBillingConfig(TypedDict):
    """Configuration for Teer billing"""

    provider: BillingProvider
    fields: BillingFields


# Meter Events


class MeterEventFieldsBase(TypedDict):
    """Base interface for meter event fields"""

    event_name: str
    identifier: Optional[str]
    timestamp: Optional[str]


class StripePayload(TypedDict):
    """Payload data for the Stripe event"""

    stripe_customer_id: str
    value: str


class StripeMeterEventFields(MeterEventFieldsBase):
    """Stripe-specific meter event fields"""

    payload: StripePayload


class StripeMeterEventCreateParams(TypedDict):
    """Parameters for creating a meter event with Stripe provider"""

    provider: Literal["stripe"]
    fields: StripeMeterEventFields


# Union type for all supported provider meter event params
MeterEventCreateParams = StripeMeterEventCreateParams
# Add more provider types here in the future


class MeterEvent(TypedDict):
    """Response type for meter events"""

    id: str
    event_name: str
    timestamp: str
    payload: Dict[str, Any]
    identifier: Optional[str]
    created_at: str
    updated_at: str


class MeterEventsResource(BaseResource):
    """Resource for meter events operations"""

    def __init__(self, client: "TeerClient"):
        """
        Initialize the MeterEvents resource.

        Args:
            client: The Teer client instance.
        """
        super().__init__(client, "billing/meter-events")

    def create(
        self,
        params: MeterEventCreateParams,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 10,
    ) -> MeterEvent:
        """
        Create a meter event to record usage.

        Args:
            params: Parameters for creating a meter event
            headers: Additional headers to include in the request.
            timeout: Request timeout in seconds. Defaults to 10 seconds.

        Returns:
            The created meter event.

        Raises:
            Exception: If the request fails.
        """
        return self._request("POST", data=params, headers=headers, timeout=timeout)


class BillingResource(BaseResource):
    """Billing Resource for handling billing operations"""

    def __init__(self, client: "TeerClient"):
        """
        Initialize the Billing resource.

        Args:
            client: The Teer client instance.
        """
        super().__init__(client, "billing")
        self.meter_events = MeterEventsResource(client)
