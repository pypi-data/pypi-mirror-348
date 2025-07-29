# -*- coding: utf-8 -*-

"""Main module."""

import contextvars

from pydantic import BaseModel

from . import apis
from .openapi_client.api_client import ApiClient
from .openapi_client.configuration import Configuration

full_serialization = contextvars.ContextVar("full_serialization", default=False)


class ExtendedApiClient(ApiClient):
    @classmethod
    def deserialize_data(cls, response_data, response_type):
        """Deserializes parsed json into an object.

        :param response_data: parsed json to be deserialized.
        :param response_type: class literal for
            deserialized object, or string of class name.

        :return: deserialized object.
        """
        return response_type.from_dict(response_data)

    def sanitize_for_serialization(self, obj):
        if hasattr(obj, "actual_instance"):
            return self.sanitize_for_serialization(obj.actual_instance)

        # For some reason, set sanitization is not handled correctly
        if isinstance(obj, set):
            obj = [*obj]

        if full_serialization.get() and isinstance(obj, BaseModel):
            return super().sanitize_for_serialization(obj.__dict__)

        return super().sanitize_for_serialization(obj)

    def serialize_fully(self, obj):
        token = full_serialization.set(True)
        try:
            result = self.sanitize_for_serialization(obj)
        finally:
            full_serialization.reset(token)
        return result


class WaybillerClient:
    """API client class for Waybiller.

    :param api_key: Company API key in Waybiller
    :param host: Waybiller host. Defaults to test host (optional)
    """

    openapi_client_class = ExtendedApiClient

    def __init__(self, api_key: str, host: str = None):
        configuration = Configuration(api_key={"ApiKeyAuth": api_key})
        if host is not None:
            configuration.host = host
        self.openapi_client = self.openapi_client_class(configuration)

        self.destinations = apis.DestinationsApi(self.openapi_client)
        self.employments = apis.EmploymentsApi(self.openapi_client)
        self.loader_action_logs = apis.LoaderActionLogsApi(self.openapi_client)
        self.orders = apis.OrdersApi(self.openapi_client)
        self.origin_assortments = apis.OriginAssortmentsApi(self.openapi_client)
        self.origins = apis.OriginsApi(self.openapi_client)
        self.transport_orders = apis.TransportOrdersApi(self.openapi_client)
        self.vehicle_location_datas = apis.VehicleLocationDataApi(self.openapi_client)
        self.vehicles = apis.VehiclesApi(self.openapi_client)
        self.waybills = apis.WaybillsApi(self.openapi_client)

    @classmethod
    def deserialize_data(cls, response_data, response_type):
        return cls.openapi_client_class.deserialize_data(response_data, response_type)

    @classmethod
    def sanitize_for_serialization(cls, api_model):
        return cls.openapi_client_class().serialize_fully(api_model)
