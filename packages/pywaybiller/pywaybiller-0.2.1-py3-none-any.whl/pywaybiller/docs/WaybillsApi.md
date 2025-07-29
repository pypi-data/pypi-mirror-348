# openapi_client.WaybillsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**waybills_accept_update**](WaybillsApi.md#waybills_accept_update) | **PUT** /external-api/waybills/{id}/accept/ | Accepting waybill
[**waybills_cancel_update**](WaybillsApi.md#waybills_cancel_update) | **PUT** /external-api/waybills/{id}/cancel/ | Cancelling waybill
[**waybills_comment_create**](WaybillsApi.md#waybills_comment_create) | **POST** /external-api/waybills/{id}/comment/ | Commenting waybill
[**waybills_create**](WaybillsApi.md#waybills_create) | **POST** /external-api/waybills/ | Creation of a waybill
[**waybills_finish_drive_create**](WaybillsApi.md#waybills_finish_drive_create) | **POST** /external-api/waybills/{id}/finish_drive/ | Completing driving
[**waybills_list**](WaybillsApi.md#waybills_list) | **GET** /external-api/waybills/ | Querying of waybills
[**waybills_refuse_update**](WaybillsApi.md#waybills_refuse_update) | **PUT** /external-api/waybills/{id}/refuse/ | Refusing waybill
[**waybills_retrieve**](WaybillsApi.md#waybills_retrieve) | **GET** /external-api/waybills/{id}/ | Querying of a single waybill
[**waybills_start_drive_create**](WaybillsApi.md#waybills_start_drive_create) | **POST** /external-api/waybills/{id}/start_drive/ | Starting driving
[**waybills_update_accepted_amounts_update**](WaybillsApi.md#waybills_update_accepted_amounts_update) | **PUT** /external-api/waybills/{id}/update_accepted_amounts/ | Updating of accepted amounts
[**waybills_update_custom_fields_update**](WaybillsApi.md#waybills_update_custom_fields_update) | **PUT** /external-api/waybills/{id}/update_custom_fields/ | Updating custom fields
[**waybills_update_dispatched_amounts_update**](WaybillsApi.md#waybills_update_dispatched_amounts_update) | **PUT** /external-api/waybills/{id}/update_dispatched_amounts/ | Updating of dispatched amounts
[**waybills_vehicle_location_data_retrieve**](WaybillsApi.md#waybills_vehicle_location_data_retrieve) | **GET** /external-api/waybills/{id}/vehicle_location_data/ | Querying of vehicle location data


# **waybills_accept_update**
> ExternalAPIWaybillAccept waybills_accept_update(id, external_api_waybill_accept_request)

Accepting waybill

Sets the status of a waybill to `accepted`.
        Only the receiving company of the waybill is authorized to accept the waybill.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_accept import ExternalAPIWaybillAccept
from openapi_client.models.external_api_waybill_accept_request import ExternalAPIWaybillAcceptRequest
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.
    external_api_waybill_accept_request = openapi_client.ExternalAPIWaybillAcceptRequest() # ExternalAPIWaybillAcceptRequest | 

    try:
        # Accepting waybill
        api_response = api_instance.waybills_accept_update(id, external_api_waybill_accept_request)
        print("The response of WaybillsApi->waybills_accept_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_accept_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 
 **external_api_waybill_accept_request** | [**ExternalAPIWaybillAcceptRequest**](ExternalAPIWaybillAcceptRequest.md)|  | 

### Return type

[**ExternalAPIWaybillAccept**](ExternalAPIWaybillAccept.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_cancel_update**
> ExternalAPIWaybillCancel waybills_cancel_update(id, external_api_waybill_cancel_request)

Cancelling waybill

Marks waybill as `cancelled`.
        Any waybill can be cancelled except waybills with status `accepted`.
        Waybill can be cancelled by origin owner, transportation company or receiver company or its representative."
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_cancel import ExternalAPIWaybillCancel
from openapi_client.models.external_api_waybill_cancel_request import ExternalAPIWaybillCancelRequest
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.
    external_api_waybill_cancel_request = openapi_client.ExternalAPIWaybillCancelRequest() # ExternalAPIWaybillCancelRequest | 

    try:
        # Cancelling waybill
        api_response = api_instance.waybills_cancel_update(id, external_api_waybill_cancel_request)
        print("The response of WaybillsApi->waybills_cancel_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_cancel_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 
 **external_api_waybill_cancel_request** | [**ExternalAPIWaybillCancelRequest**](ExternalAPIWaybillCancelRequest.md)|  | 

### Return type

[**ExternalAPIWaybillCancel**](ExternalAPIWaybillCancel.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_comment_create**
> waybills_comment_create(id, external_api_waybill_comment_request)

Commenting waybill

Adds a comment to the waybill.
        Only companies associated with the waybill can add comments to it.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_comment_request import ExternalAPIWaybillCommentRequest
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.
    external_api_waybill_comment_request = openapi_client.ExternalAPIWaybillCommentRequest() # ExternalAPIWaybillCommentRequest | 

    try:
        # Commenting waybill
        api_instance.waybills_comment_create(id, external_api_waybill_comment_request)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_comment_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 
 **external_api_waybill_comment_request** | [**ExternalAPIWaybillCommentRequest**](ExternalAPIWaybillCommentRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_create**
> ExternalAPIWaybillCreate waybills_create(external_api_waybill_create_request)

Creation of a waybill

Creates a new waybill.<br><br>
        **NB!** IDs posted this way are IDs in your system and these are used to match objects in
        your system with objects in Waybiller.
        It is also possible to use the origin or destination ID in Waybiller
        (if you have received those via GET Origins or GET Destinations endpoints).
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_create import ExternalAPIWaybillCreate
from openapi_client.models.external_api_waybill_create_request import ExternalAPIWaybillCreateRequest
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
    api_instance = openapi_client.WaybillsApi(api_client)
    external_api_waybill_create_request = openapi_client.ExternalAPIWaybillCreateRequest() # ExternalAPIWaybillCreateRequest | 

    try:
        # Creation of a waybill
        api_response = api_instance.waybills_create(external_api_waybill_create_request)
        print("The response of WaybillsApi->waybills_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_api_waybill_create_request** | [**ExternalAPIWaybillCreateRequest**](ExternalAPIWaybillCreateRequest.md)|  | 

### Return type

[**ExternalAPIWaybillCreate**](ExternalAPIWaybillCreate.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_finish_drive_create**
> waybills_finish_drive_create(id, external_api_waybill_finish_drive_request)

Completing driving

Sets the status of a waybill to `in destination`. Waybill status has to be `in progress` to use this endpoint.
        Only the transportation company or receiving company of the waybill are authorized to move waybill to `in destination`.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_finish_drive_request import ExternalAPIWaybillFinishDriveRequest
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.
    external_api_waybill_finish_drive_request = openapi_client.ExternalAPIWaybillFinishDriveRequest() # ExternalAPIWaybillFinishDriveRequest | 

    try:
        # Completing driving
        api_instance.waybills_finish_drive_create(id, external_api_waybill_finish_drive_request)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_finish_drive_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 
 **external_api_waybill_finish_drive_request** | [**ExternalAPIWaybillFinishDriveRequest**](ExternalAPIWaybillFinishDriveRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_list**
> PaginatedExternalAPIWaybillListList waybills_list(destination_ids=destination_ids, limit=limit, offset=offset, origin_ids=origin_ids, raw_destination_ids=raw_destination_ids, raw_origin_ids=raw_origin_ids, transportation_cost_confirmed_at_timestamp__gt=transportation_cost_confirmed_at_timestamp__gt, transportation_cost_confirmed_at_timestamp__lt=transportation_cost_confirmed_at_timestamp__lt)

Querying of waybills

Returns all waybills associated with your company, according to the specified filters.<br><br>
        **NB!** By default, past 30 days according to the `dispatcher_timestamp` field waybills are returned. Use
        `dispatcher_timestamp__lt` and `dispatcher_timestamp__gt` for filtering. Note that the maximum range is 30 days.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_waybill_list_list import PaginatedExternalAPIWaybillListList
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
    api_instance = openapi_client.WaybillsApi(api_client)
    destination_ids = 'destination_ids_example' # str | Filters waybills with a specified list of destination IDs from your system. Multiple values may be separated by commas. (optional)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)
    origin_ids = 'origin_ids_example' # str | Filters waybills with a specified list of origin IDs from your systemMultiple values may be separated by commas. (optional)
    raw_destination_ids = 'raw_destination_ids_example' # str | Filters waybills with a specified list of raw destination IDs. Multiple values may be separated by commas. (optional)
    raw_origin_ids = 'raw_origin_ids_example' # str | Filters waybills with a specified list of raw origin IDs. Multiple values may be separated by commas. (optional)
    transportation_cost_confirmed_at_timestamp__gt = '2013-10-20T19:20:30+01:00' # datetime | Filters waybills with a transportation cost confirmed timestamp greater than the specified value. The value must be in ISO 8601 format. (optional)
    transportation_cost_confirmed_at_timestamp__lt = '2013-10-20T19:20:30+01:00' # datetime | Filters waybills with a transportation cost confirmed timestamp less than the specified value. The value must be in ISO 8601 format. (optional)

    try:
        # Querying of waybills
        api_response = api_instance.waybills_list(destination_ids=destination_ids, limit=limit, offset=offset, origin_ids=origin_ids, raw_destination_ids=raw_destination_ids, raw_origin_ids=raw_origin_ids, transportation_cost_confirmed_at_timestamp__gt=transportation_cost_confirmed_at_timestamp__gt, transportation_cost_confirmed_at_timestamp__lt=transportation_cost_confirmed_at_timestamp__lt)
        print("The response of WaybillsApi->waybills_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **destination_ids** | **str**| Filters waybills with a specified list of destination IDs from your system. Multiple values may be separated by commas. | [optional] 
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]
 **origin_ids** | **str**| Filters waybills with a specified list of origin IDs from your systemMultiple values may be separated by commas. | [optional] 
 **raw_destination_ids** | **str**| Filters waybills with a specified list of raw destination IDs. Multiple values may be separated by commas. | [optional] 
 **raw_origin_ids** | **str**| Filters waybills with a specified list of raw origin IDs. Multiple values may be separated by commas. | [optional] 
 **transportation_cost_confirmed_at_timestamp__gt** | **datetime**| Filters waybills with a transportation cost confirmed timestamp greater than the specified value. The value must be in ISO 8601 format. | [optional] 
 **transportation_cost_confirmed_at_timestamp__lt** | **datetime**| Filters waybills with a transportation cost confirmed timestamp less than the specified value. The value must be in ISO 8601 format. | [optional] 

### Return type

[**PaginatedExternalAPIWaybillListList**](PaginatedExternalAPIWaybillListList.md)

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

# **waybills_refuse_update**
> ExternalAPIWaybillRefuse waybills_refuse_update(id, external_api_waybill_refuse_request)

Refusing waybill

Marks waybill as `refused` in destination and sets the status of waybill to in progress again.
        If new destination is provided, then new destination is set for the waybill.
        Only the transportation company or receiving company of the waybill are authorized to refuse the waybill.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_refuse import ExternalAPIWaybillRefuse
from openapi_client.models.external_api_waybill_refuse_request import ExternalAPIWaybillRefuseRequest
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.
    external_api_waybill_refuse_request = openapi_client.ExternalAPIWaybillRefuseRequest() # ExternalAPIWaybillRefuseRequest | 

    try:
        # Refusing waybill
        api_response = api_instance.waybills_refuse_update(id, external_api_waybill_refuse_request)
        print("The response of WaybillsApi->waybills_refuse_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_refuse_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 
 **external_api_waybill_refuse_request** | [**ExternalAPIWaybillRefuseRequest**](ExternalAPIWaybillRefuseRequest.md)|  | 

### Return type

[**ExternalAPIWaybillRefuse**](ExternalAPIWaybillRefuse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_retrieve**
> ExternalAPIWaybillRetrieve waybills_retrieve(id)

Querying of a single waybill

Returns a waybill with the specified ID. Only companies associated with the waybill can query it.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_retrieve import ExternalAPIWaybillRetrieve
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 'id_example' # str | The ID of the waybill queried.

    try:
        # Querying of a single waybill
        api_response = api_instance.waybills_retrieve(id)
        print("The response of WaybillsApi->waybills_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the waybill queried. | 

### Return type

[**ExternalAPIWaybillRetrieve**](ExternalAPIWaybillRetrieve.md)

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

# **waybills_start_drive_create**
> ExternalAPIWaybillStartDrive waybills_start_drive_create(id, external_api_waybill_start_drive_request)

Starting driving

Sets the status of a waybill to `in progress`. Waybill status has to be `created` to use this endpoint. Only
        the transportation company or receiving company of the waybill are authorized to move waybill to `in
        progress`.<br><br>
        **NB!** Destination needs to belong to the receiving company in case the origin’s
        `feature_waybill_destination_changing_disabled_for_drivers` flag is set to `True`.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_start_drive import ExternalAPIWaybillStartDrive
from openapi_client.models.external_api_waybill_start_drive_request import ExternalAPIWaybillStartDriveRequest
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.
    external_api_waybill_start_drive_request = openapi_client.ExternalAPIWaybillStartDriveRequest() # ExternalAPIWaybillStartDriveRequest | 

    try:
        # Starting driving
        api_response = api_instance.waybills_start_drive_create(id, external_api_waybill_start_drive_request)
        print("The response of WaybillsApi->waybills_start_drive_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_start_drive_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 
 **external_api_waybill_start_drive_request** | [**ExternalAPIWaybillStartDriveRequest**](ExternalAPIWaybillStartDriveRequest.md)|  | 

### Return type

[**ExternalAPIWaybillStartDrive**](ExternalAPIWaybillStartDrive.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_update_accepted_amounts_update**
> ExternalAPIWaybillAcceptedAmounts waybills_update_accepted_amounts_update(id, external_api_waybill_accepted_amounts_request)

Updating of accepted amounts

Sets the accepted amounts for the waybill.
        Optional `accepted_assortment_id` can be used when the accepted assortment differs from the dispatched one.
        In this case, you must still provide `assortment_id` matching the dispatched assortment.
        Authorized only for the receiving company of the waybill.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_accepted_amounts import ExternalAPIWaybillAcceptedAmounts
from openapi_client.models.external_api_waybill_accepted_amounts_request import ExternalAPIWaybillAcceptedAmountsRequest
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.
    external_api_waybill_accepted_amounts_request = openapi_client.ExternalAPIWaybillAcceptedAmountsRequest() # ExternalAPIWaybillAcceptedAmountsRequest | 

    try:
        # Updating of accepted amounts
        api_response = api_instance.waybills_update_accepted_amounts_update(id, external_api_waybill_accepted_amounts_request)
        print("The response of WaybillsApi->waybills_update_accepted_amounts_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_update_accepted_amounts_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 
 **external_api_waybill_accepted_amounts_request** | [**ExternalAPIWaybillAcceptedAmountsRequest**](ExternalAPIWaybillAcceptedAmountsRequest.md)|  | 

### Return type

[**ExternalAPIWaybillAcceptedAmounts**](ExternalAPIWaybillAcceptedAmounts.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_update_custom_fields_update**
> ExternalAPIWaybillRetrieve waybills_update_custom_fields_update(id, request_body=request_body)

Updating custom fields

Updates custom fields defined by the customer support.<br>
        The values of the fields must match the type assigned to the field. If the field is of type `timestamp`,
        the value must be an integer representing the timestamp in milliseconds.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_retrieve import ExternalAPIWaybillRetrieve
from openapi_client.models.waybills_update_custom_fields_update_request_value import WaybillsUpdateCustomFieldsUpdateRequestValue
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.
    request_body = {"moisture":5.7,"comment":"Good quality","temperature":20} # Dict[str, WaybillsUpdateCustomFieldsUpdateRequestValue] |  (optional)

    try:
        # Updating custom fields
        api_response = api_instance.waybills_update_custom_fields_update(id, request_body=request_body)
        print("The response of WaybillsApi->waybills_update_custom_fields_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_update_custom_fields_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 
 **request_body** | [**Dict[str, WaybillsUpdateCustomFieldsUpdateRequestValue]**](WaybillsUpdateCustomFieldsUpdateRequestValue.md)|  | [optional] 

### Return type

[**ExternalAPIWaybillRetrieve**](ExternalAPIWaybillRetrieve.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**303** |  |  * Location - Querying of the updated waybill. <br>  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_update_dispatched_amounts_update**
> ExternalAPIWaybillDispatchedAmounts waybills_update_dispatched_amounts_update(id, external_api_waybill_dispatched_amounts_request)

Updating of dispatched amounts

Updates dispatched amounts for the waybill.<br>
        Generally only authorized for the origin company of the waybill,
        unless the Waybiller team has given the key a permission to update the dispatched weights as a receiver as well.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_dispatched_amounts import ExternalAPIWaybillDispatchedAmounts
from openapi_client.models.external_api_waybill_dispatched_amounts_request import ExternalAPIWaybillDispatchedAmountsRequest
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.
    external_api_waybill_dispatched_amounts_request = openapi_client.ExternalAPIWaybillDispatchedAmountsRequest() # ExternalAPIWaybillDispatchedAmountsRequest | 

    try:
        # Updating of dispatched amounts
        api_response = api_instance.waybills_update_dispatched_amounts_update(id, external_api_waybill_dispatched_amounts_request)
        print("The response of WaybillsApi->waybills_update_dispatched_amounts_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_update_dispatched_amounts_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 
 **external_api_waybill_dispatched_amounts_request** | [**ExternalAPIWaybillDispatchedAmountsRequest**](ExternalAPIWaybillDispatchedAmountsRequest.md)|  | 

### Return type

[**ExternalAPIWaybillDispatchedAmounts**](ExternalAPIWaybillDispatchedAmounts.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waybills_vehicle_location_data_retrieve**
> ExternalAPIWaybillVehicleLocation waybills_vehicle_location_data_retrieve(id)

Querying of vehicle location data

Returns vehicle location data.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_waybill_vehicle_location import ExternalAPIWaybillVehicleLocation
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
    api_instance = openapi_client.WaybillsApi(api_client)
    id = 56 # int | A unique integer value identifying this waybill.

    try:
        # Querying of vehicle location data
        api_response = api_instance.waybills_vehicle_location_data_retrieve(id)
        print("The response of WaybillsApi->waybills_vehicle_location_data_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaybillsApi->waybills_vehicle_location_data_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this waybill. | 

### Return type

[**ExternalAPIWaybillVehicleLocation**](ExternalAPIWaybillVehicleLocation.md)

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

