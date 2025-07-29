# openapi_client.LoaderActionLogsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**loader_action_logs_list**](LoaderActionLogsApi.md#loader_action_logs_list) | **GET** /external-api/loader-action-logs/ | Querying loader action logs


# **loader_action_logs_list**
> PaginatedExternalAPILoaderActionLogList loader_action_logs_list(limit=limit, loader_unit_id=loader_unit_id, offset=offset, timestamp=timestamp, timestamp__gt=timestamp__gt, timestamp__gte=timestamp__gte, timestamp__isnull=timestamp__isnull, timestamp__lt=timestamp__lt, timestamp__lte=timestamp__lte)

Querying loader action logs

Returns all loader action logs created by your company according to the specified filters.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_loader_action_log_list import PaginatedExternalAPILoaderActionLogList
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
    api_instance = openapi_client.LoaderActionLogsApi(api_client)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    loader_unit_id = 56 # int | Filters loader action logs for your company with the specified loader unit ID (optional)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)
    timestamp = 'timestamp_example' # str | Filters loader action logs for your company within the specified time period (exact) (optional)
    timestamp__gt = 'timestamp__gt_example' # str | Filters loader action logs for your company within the specified time period (greater than) (optional)
    timestamp__gte = 'timestamp__gte_example' # str | Filters loader action logs for your company within the specified time period (greater than or equal) (optional)
    timestamp__isnull = 'timestamp__isnull_example' # str | Filters loader action logs for your company that do not have a timestamp (optional)
    timestamp__lt = 'timestamp__lt_example' # str | Filters loader action logs for your company within the specified time period (less than) (optional)
    timestamp__lte = 'timestamp__lte_example' # str | Filters loader action logs for your company within the specified time period (less than or equal) (optional)

    try:
        # Querying loader action logs
        api_response = api_instance.loader_action_logs_list(limit=limit, loader_unit_id=loader_unit_id, offset=offset, timestamp=timestamp, timestamp__gt=timestamp__gt, timestamp__gte=timestamp__gte, timestamp__isnull=timestamp__isnull, timestamp__lt=timestamp__lt, timestamp__lte=timestamp__lte)
        print("The response of LoaderActionLogsApi->loader_action_logs_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LoaderActionLogsApi->loader_action_logs_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **loader_unit_id** | **int**| Filters loader action logs for your company with the specified loader unit ID | [optional] 
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]
 **timestamp** | **str**| Filters loader action logs for your company within the specified time period (exact) | [optional] 
 **timestamp__gt** | **str**| Filters loader action logs for your company within the specified time period (greater than) | [optional] 
 **timestamp__gte** | **str**| Filters loader action logs for your company within the specified time period (greater than or equal) | [optional] 
 **timestamp__isnull** | **str**| Filters loader action logs for your company that do not have a timestamp | [optional] 
 **timestamp__lt** | **str**| Filters loader action logs for your company within the specified time period (less than) | [optional] 
 **timestamp__lte** | **str**| Filters loader action logs for your company within the specified time period (less than or equal) | [optional] 

### Return type

[**PaginatedExternalAPILoaderActionLogList**](PaginatedExternalAPILoaderActionLogList.md)

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

