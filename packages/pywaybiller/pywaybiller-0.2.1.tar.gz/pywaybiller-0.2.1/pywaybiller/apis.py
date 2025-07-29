from typing import Callable

from .openapi_client import api


class AllMixin:
    """Mixin for API endpoint classes to have an all() method for returning objects from all pages.

    :attr list_endpoint_attr: API endpoint's method for returning paged results
    """

    list_endpoint_attr = None
    limit_parameter_name = "limit"
    offset_parameter_name = "offset"
    default_limit = 30

    def get_list_endpoint(self) -> Callable:
        """Method for getting the callable API's endpoint that is responsible for returning paged results

        :return: Callable API's list endpoint method.
        """
        if self.list_endpoint_attr is None:
            raise ValueError("AllMixin requires `list_endpoint_attr` to be set")
        if not hasattr(self, self.list_endpoint_attr):
            raise ValueError(
                f"{self.__class__} does not have the required list attribute `{self.list_endpoint_attr}`"
            )
        return getattr(self, self.list_endpoint_attr)

    def all(self, **kwargs):
        """Method for going through all the pages of a list view that is responsible for returning paged results"""
        if self.offset_parameter_name in kwargs:
            del kwargs[self.offset_parameter_name]
        limit: int = kwargs.pop(self.limit_parameter_name, self.default_limit)
        endpoint = self.get_list_endpoint()

        current_offset = 0
        total_count = None

        while total_count is None or current_offset < total_count:
            kwargs[self.limit_parameter_name] = limit
            kwargs[self.offset_parameter_name] = current_offset
            page_response = endpoint(**kwargs)
            if total_count is None:
                total_count = page_response.count

            if page_response.results:
                yield from page_response.results
            else:
                # Possibly number of items changed while iterating, in this case assume no more items are coming
                return

            current_offset += limit


class DestinationsApi(AllMixin, api.DestinationsApi):
    list_endpoint_attr = "destinations_list"


class EmploymentsApi(AllMixin, api.EmploymentsApi):
    list_endpoint_attr = "employments_list"


class LoaderActionLogsApi(AllMixin, api.LoaderActionLogsApi):
    list_endpoint_attr = "loader_action_logs_list"


class OrdersApi(AllMixin, api.OrdersApi):
    list_endpoint_attr = "orders_list"


class OriginAssortmentsApi(AllMixin, api.OriginAssortmentsApi):
    list_endpoint_attr = "origin_assortments_list"


class OriginsApi(AllMixin, api.OriginsApi):
    list_endpoint_attr = "origins_list"


class TransportOrdersApi(AllMixin, api.TransportOrdersApi):
    list_endpoint_attr = "transport_orders_list"


class VehicleLocationDataApi(AllMixin, api.VehicleLocationDataApi):
    list_endpoint_attr = "vehicle_location_data_list"


class VehiclesApi(AllMixin, api.VehiclesApi):
    list_endpoint_attr = "vehicles_list"


class WaybillsApi(AllMixin, api.WaybillsApi):
    list_endpoint_attr = "waybills_list"
