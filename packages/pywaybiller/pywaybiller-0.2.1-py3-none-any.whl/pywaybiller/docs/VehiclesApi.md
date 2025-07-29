# openapi_client.VehiclesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**vehicles_list**](VehiclesApi.md#vehicles_list) | **GET** /external-api/vehicles/ | Querying of vehicles
[**vehicles_retrieve**](VehiclesApi.md#vehicles_retrieve) | **GET** /external-api/vehicles/{id}/ | Querying of a single vehicle


# **vehicles_list**
> PaginatedExternalAPIVehicleList vehicles_list(limit=limit, offset=offset, dispatcher_timestamp__gt=dispatcher_timestamp__gt, dispatcher_timestamp__lt=dispatcher_timestamp__lt)

Querying of vehicles

Returns all vehicles associated with your company and with your subcontractors.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_vehicle_list import PaginatedExternalAPIVehicleList
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
    api_instance = openapi_client.VehiclesApi(api_client)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)
    dispatcher_timestamp__gt = 'dispatcher_timestamp__gt_example' # str |  (optional)
    dispatcher_timestamp__lt = 'dispatcher_timestamp__lt_example' # str |  (optional)

    try:
        # Querying of vehicles
        api_response = api_instance.vehicles_list(limit=limit, offset=offset, dispatcher_timestamp__gt=dispatcher_timestamp__gt, dispatcher_timestamp__lt=dispatcher_timestamp__lt)
        print("The response of VehiclesApi->vehicles_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VehiclesApi->vehicles_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]
 **dispatcher_timestamp__gt** | **str**|  | [optional] 
 **dispatcher_timestamp__lt** | **str**|  | [optional] 

### Return type

[**PaginatedExternalAPIVehicleList**](PaginatedExternalAPIVehicleList.md)

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

# **vehicles_retrieve**
> ExternalAPIVehicle vehicles_retrieve(id)

Querying of a single vehicle

Returns a vehicle instance.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_vehicle import ExternalAPIVehicle
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
    api_instance = openapi_client.VehiclesApi(api_client)
    id = 56 # int | A unique integer value identifying this vehicle.

    try:
        # Querying of a single vehicle
        api_response = api_instance.vehicles_retrieve(id)
        print("The response of VehiclesApi->vehicles_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VehiclesApi->vehicles_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this vehicle. | 

### Return type

[**ExternalAPIVehicle**](ExternalAPIVehicle.md)

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
**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

