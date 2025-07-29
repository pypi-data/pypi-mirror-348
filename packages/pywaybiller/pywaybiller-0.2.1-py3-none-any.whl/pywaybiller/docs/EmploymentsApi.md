# openapi_client.EmploymentsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**employments_list**](EmploymentsApi.md#employments_list) | **GET** /external-api/employments/ | Querying employments
[**employments_retrieve**](EmploymentsApi.md#employments_retrieve) | **GET** /external-api/employments/{id}/ | Querying a single employment


# **employments_list**
> PaginatedExternalAPIEmploymentList employments_list(limit=limit, offset=offset)

Querying employments

Returns all employments associated with your company

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_employment_list import PaginatedExternalAPIEmploymentList
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
    api_instance = openapi_client.EmploymentsApi(api_client)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)

    try:
        # Querying employments
        api_response = api_instance.employments_list(limit=limit, offset=offset)
        print("The response of EmploymentsApi->employments_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EmploymentsApi->employments_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]

### Return type

[**PaginatedExternalAPIEmploymentList**](PaginatedExternalAPIEmploymentList.md)

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

# **employments_retrieve**
> ExternalAPIEmployment employments_retrieve(id)

Querying a single employment

Returns an employment instance

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_employment import ExternalAPIEmployment
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
    api_instance = openapi_client.EmploymentsApi(api_client)
    id = 56 # int | A unique integer value identifying this employment.

    try:
        # Querying a single employment
        api_response = api_instance.employments_retrieve(id)
        print("The response of EmploymentsApi->employments_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EmploymentsApi->employments_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this employment. | 

### Return type

[**ExternalAPIEmployment**](ExternalAPIEmployment.md)

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

