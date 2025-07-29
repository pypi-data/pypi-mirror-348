# openapi_client.VehicleLocationDataApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**vehicle_location_data_list**](VehicleLocationDataApi.md#vehicle_location_data_list) | **GET** /external-api/vehicle-location-data/ | Querying of vehicle location data


# **vehicle_location_data_list**
> PaginatedExternalAPIVehicleLocationDataList vehicle_location_data_list(cancelled_timestamp=cancelled_timestamp, cancelled_timestamp__gt=cancelled_timestamp__gt, cancelled_timestamp__gte=cancelled_timestamp__gte, cancelled_timestamp__isnull=cancelled_timestamp__isnull, cancelled_timestamp__lt=cancelled_timestamp__lt, cancelled_timestamp__lte=cancelled_timestamp__lte, confirmed_timestamp=confirmed_timestamp, confirmed_timestamp__gt=confirmed_timestamp__gt, confirmed_timestamp__gte=confirmed_timestamp__gte, confirmed_timestamp__isnull=confirmed_timestamp__isnull, confirmed_timestamp__lt=confirmed_timestamp__lt, confirmed_timestamp__lte=confirmed_timestamp__lte, destination_id=destination_id, dispatcher_timestamp=dispatcher_timestamp, dispatcher_timestamp__gt=dispatcher_timestamp__gt, dispatcher_timestamp__gte=dispatcher_timestamp__gte, dispatcher_timestamp__isnull=dispatcher_timestamp__isnull, dispatcher_timestamp__lt=dispatcher_timestamp__lt, dispatcher_timestamp__lte=dispatcher_timestamp__lte, driver_timestamp=driver_timestamp, driver_timestamp__gt=driver_timestamp__gt, driver_timestamp__gte=driver_timestamp__gte, driver_timestamp__isnull=driver_timestamp__isnull, driver_timestamp__lt=driver_timestamp__lt, driver_timestamp__lte=driver_timestamp__lte, limit=limit, offset=offset, truck_reg_number=truck_reg_number, waybill_number=waybill_number, waybill_status=waybill_status)

Querying of vehicle location data

Returns all vehicle location data for waybills associated with your company, according to the specified filters.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_vehicle_location_data_list import PaginatedExternalAPIVehicleLocationDataList
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.VehicleLocationDataApi(api_client)
    cancelled_timestamp = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data by specified cancellation timestamp (optional)
    cancelled_timestamp__gt = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where cancellation timestamp is greater than specified value (optional)
    cancelled_timestamp__gte = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where cancellation timestamp is greater than or equal to specified value (optional)
    cancelled_timestamp__isnull = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where cancellation timestamp is null or not null (optional)
    cancelled_timestamp__lt = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where cancellation timestamp is less than specified value (optional)
    cancelled_timestamp__lte = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where cancellation timestamp is less than or equal to specified value (optional)
    confirmed_timestamp = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data by specified confirmation timestamp (optional)
    confirmed_timestamp__gt = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where confirmation timestamp is greater than specified value (optional)
    confirmed_timestamp__gte = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where confirmation timestamp is greater than or equal to specified value (optional)
    confirmed_timestamp__isnull = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where confirmation timestamp is null or not null (optional)
    confirmed_timestamp__lt = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where confirmation timestamp is less than specified value (optional)
    confirmed_timestamp__lte = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where confirmation timestamp is less than or equal to specified value (optional)
    destination_id = 56 # int | Filters vehicle location data by specified destination ID (optional)
    dispatcher_timestamp = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data by specified dispatcher timestamp (optional)
    dispatcher_timestamp__gt = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where dispatcher timestamp is greater than specified value (optional)
    dispatcher_timestamp__gte = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where dispatcher timestamp is greater than or equal to specified value (optional)
    dispatcher_timestamp__isnull = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where dispatcher timestamp is null or not null (optional)
    dispatcher_timestamp__lt = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where dispatcher timestamp is less than specified value (optional)
    dispatcher_timestamp__lte = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where dispatcher timestamp is less than or equal to specified value (optional)
    driver_timestamp = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data by specified driver timestamp (optional)
    driver_timestamp__gt = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where driver timestamp is greater than specified value (optional)
    driver_timestamp__gte = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where driver timestamp is greater than or equal to specified value (optional)
    driver_timestamp__isnull = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where driver timestamp is null or not null (optional)
    driver_timestamp__lt = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where driver timestamp is less than specified value (optional)
    driver_timestamp__lte = '2013-10-20T19:20:30+01:00' # datetime | Filters vehicle location data where driver timestamp is less than or equal to specified value (optional)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)
    truck_reg_number = 'truck_reg_number_example' # str | Filters vehicle location data by specified truck registration number (optional)
    waybill_number = 'waybill_number_example' # str | Filters vehicle location data by specified waybill number (optional)
    waybill_status = 56 # int | Filters vehicle location data by specified waybill status (optional)

    try:
        # Querying of vehicle location data
        api_response = api_instance.vehicle_location_data_list(cancelled_timestamp=cancelled_timestamp, cancelled_timestamp__gt=cancelled_timestamp__gt, cancelled_timestamp__gte=cancelled_timestamp__gte, cancelled_timestamp__isnull=cancelled_timestamp__isnull, cancelled_timestamp__lt=cancelled_timestamp__lt, cancelled_timestamp__lte=cancelled_timestamp__lte, confirmed_timestamp=confirmed_timestamp, confirmed_timestamp__gt=confirmed_timestamp__gt, confirmed_timestamp__gte=confirmed_timestamp__gte, confirmed_timestamp__isnull=confirmed_timestamp__isnull, confirmed_timestamp__lt=confirmed_timestamp__lt, confirmed_timestamp__lte=confirmed_timestamp__lte, destination_id=destination_id, dispatcher_timestamp=dispatcher_timestamp, dispatcher_timestamp__gt=dispatcher_timestamp__gt, dispatcher_timestamp__gte=dispatcher_timestamp__gte, dispatcher_timestamp__isnull=dispatcher_timestamp__isnull, dispatcher_timestamp__lt=dispatcher_timestamp__lt, dispatcher_timestamp__lte=dispatcher_timestamp__lte, driver_timestamp=driver_timestamp, driver_timestamp__gt=driver_timestamp__gt, driver_timestamp__gte=driver_timestamp__gte, driver_timestamp__isnull=driver_timestamp__isnull, driver_timestamp__lt=driver_timestamp__lt, driver_timestamp__lte=driver_timestamp__lte, limit=limit, offset=offset, truck_reg_number=truck_reg_number, waybill_number=waybill_number, waybill_status=waybill_status)
        print("The response of VehicleLocationDataApi->vehicle_location_data_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VehicleLocationDataApi->vehicle_location_data_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cancelled_timestamp** | **datetime**| Filters vehicle location data by specified cancellation timestamp | [optional] 
 **cancelled_timestamp__gt** | **datetime**| Filters vehicle location data where cancellation timestamp is greater than specified value | [optional] 
 **cancelled_timestamp__gte** | **datetime**| Filters vehicle location data where cancellation timestamp is greater than or equal to specified value | [optional] 
 **cancelled_timestamp__isnull** | **datetime**| Filters vehicle location data where cancellation timestamp is null or not null | [optional] 
 **cancelled_timestamp__lt** | **datetime**| Filters vehicle location data where cancellation timestamp is less than specified value | [optional] 
 **cancelled_timestamp__lte** | **datetime**| Filters vehicle location data where cancellation timestamp is less than or equal to specified value | [optional] 
 **confirmed_timestamp** | **datetime**| Filters vehicle location data by specified confirmation timestamp | [optional] 
 **confirmed_timestamp__gt** | **datetime**| Filters vehicle location data where confirmation timestamp is greater than specified value | [optional] 
 **confirmed_timestamp__gte** | **datetime**| Filters vehicle location data where confirmation timestamp is greater than or equal to specified value | [optional] 
 **confirmed_timestamp__isnull** | **datetime**| Filters vehicle location data where confirmation timestamp is null or not null | [optional] 
 **confirmed_timestamp__lt** | **datetime**| Filters vehicle location data where confirmation timestamp is less than specified value | [optional] 
 **confirmed_timestamp__lte** | **datetime**| Filters vehicle location data where confirmation timestamp is less than or equal to specified value | [optional] 
 **destination_id** | **int**| Filters vehicle location data by specified destination ID | [optional] 
 **dispatcher_timestamp** | **datetime**| Filters vehicle location data by specified dispatcher timestamp | [optional] 
 **dispatcher_timestamp__gt** | **datetime**| Filters vehicle location data where dispatcher timestamp is greater than specified value | [optional] 
 **dispatcher_timestamp__gte** | **datetime**| Filters vehicle location data where dispatcher timestamp is greater than or equal to specified value | [optional] 
 **dispatcher_timestamp__isnull** | **datetime**| Filters vehicle location data where dispatcher timestamp is null or not null | [optional] 
 **dispatcher_timestamp__lt** | **datetime**| Filters vehicle location data where dispatcher timestamp is less than specified value | [optional] 
 **dispatcher_timestamp__lte** | **datetime**| Filters vehicle location data where dispatcher timestamp is less than or equal to specified value | [optional] 
 **driver_timestamp** | **datetime**| Filters vehicle location data by specified driver timestamp | [optional] 
 **driver_timestamp__gt** | **datetime**| Filters vehicle location data where driver timestamp is greater than specified value | [optional] 
 **driver_timestamp__gte** | **datetime**| Filters vehicle location data where driver timestamp is greater than or equal to specified value | [optional] 
 **driver_timestamp__isnull** | **datetime**| Filters vehicle location data where driver timestamp is null or not null | [optional] 
 **driver_timestamp__lt** | **datetime**| Filters vehicle location data where driver timestamp is less than specified value | [optional] 
 **driver_timestamp__lte** | **datetime**| Filters vehicle location data where driver timestamp is less than or equal to specified value | [optional] 
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]
 **truck_reg_number** | **str**| Filters vehicle location data by specified truck registration number | [optional] 
 **waybill_number** | **str**| Filters vehicle location data by specified waybill number | [optional] 
 **waybill_status** | **int**| Filters vehicle location data by specified waybill status | [optional] 

### Return type

[**PaginatedExternalAPIVehicleLocationDataList**](PaginatedExternalAPIVehicleLocationDataList.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

