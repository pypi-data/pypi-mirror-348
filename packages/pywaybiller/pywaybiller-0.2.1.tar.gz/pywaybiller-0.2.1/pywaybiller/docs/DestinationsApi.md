# openapi_client.DestinationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**destinations_list**](DestinationsApi.md#destinations_list) | **GET** /external-api/destinations/ | Querying destinations


# **destinations_list**
> PaginatedExternalAPIDestinationList destinations_list(company__reg_code=company__reg_code, company__reg_code__contains=company__reg_code__contains, company__reg_code__icontains=company__reg_code__icontains, company__reg_code__iexact=company__reg_code__iexact, explicitly_viewable=explicitly_viewable, limit=limit, location__address=location__address, location__address__contains=location__address__contains, location__address__icontains=location__address__icontains, location__address__iexact=location__address__iexact, name=name, name__contains=name__contains, name__icontains=name__icontains, name__iexact=name__iexact, offset=offset)

Querying destinations

Returns all destinations associated with your company according to the specified filters

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_destination_list import PaginatedExternalAPIDestinationList
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
    api_instance = openapi_client.DestinationsApi(api_client)
    company__reg_code = 'company__reg_code_example' # str | Filters destinations that belong to the company with the specified registration code (case-sensitive) (optional)
    company__reg_code__contains = 'company__reg_code__contains_example' # str | Filters destinations that belong to companies whose registration codes contain this keyword (case-sensitive) (optional)
    company__reg_code__icontains = 'company__reg_code__icontains_example' # str | Filters destinations that belong to companies whose registration codes contain this keyword (case-insensitive) (optional)
    company__reg_code__iexact = 'company__reg_code__iexact_example' # str | Filters destinations that belong to the company with the specified registration code (case-insensitive) (optional)
    explicitly_viewable = True # bool | Filters destinations that belong to your company or where your company was added as a partner (optional)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    location__address = 'location__address_example' # str | Filters destinations with the specified address (case-sensitive) (optional)
    location__address__contains = 'location__address__contains_example' # str | Filters destinations whose addresses contain this keyword (case-sensitive) (optional)
    location__address__icontains = 'location__address__icontains_example' # str | Filters destinations whose addresses contain this keyword (case-insensitive) (optional)
    location__address__iexact = 'location__address__iexact_example' # str | Filters destinations with the specified address (case-insensitive) (optional)
    name = 'name_example' # str | Filters destinations with the specified name (case-sensitive) (optional)
    name__contains = 'name__contains_example' # str | Filters destinations whose names contain this keyword (case-sensitive) (optional)
    name__icontains = 'name__icontains_example' # str | Filters destinations whose names contain this keyword (case-insensitive) (optional)
    name__iexact = 'name__iexact_example' # str | Filters destinations with the specified name (case-insensitive) (optional)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)

    try:
        # Querying destinations
        api_response = api_instance.destinations_list(company__reg_code=company__reg_code, company__reg_code__contains=company__reg_code__contains, company__reg_code__icontains=company__reg_code__icontains, company__reg_code__iexact=company__reg_code__iexact, explicitly_viewable=explicitly_viewable, limit=limit, location__address=location__address, location__address__contains=location__address__contains, location__address__icontains=location__address__icontains, location__address__iexact=location__address__iexact, name=name, name__contains=name__contains, name__icontains=name__icontains, name__iexact=name__iexact, offset=offset)
        print("The response of DestinationsApi->destinations_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DestinationsApi->destinations_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **company__reg_code** | **str**| Filters destinations that belong to the company with the specified registration code (case-sensitive) | [optional] 
 **company__reg_code__contains** | **str**| Filters destinations that belong to companies whose registration codes contain this keyword (case-sensitive) | [optional] 
 **company__reg_code__icontains** | **str**| Filters destinations that belong to companies whose registration codes contain this keyword (case-insensitive) | [optional] 
 **company__reg_code__iexact** | **str**| Filters destinations that belong to the company with the specified registration code (case-insensitive) | [optional] 
 **explicitly_viewable** | **bool**| Filters destinations that belong to your company or where your company was added as a partner | [optional] 
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **location__address** | **str**| Filters destinations with the specified address (case-sensitive) | [optional] 
 **location__address__contains** | **str**| Filters destinations whose addresses contain this keyword (case-sensitive) | [optional] 
 **location__address__icontains** | **str**| Filters destinations whose addresses contain this keyword (case-insensitive) | [optional] 
 **location__address__iexact** | **str**| Filters destinations with the specified address (case-insensitive) | [optional] 
 **name** | **str**| Filters destinations with the specified name (case-sensitive) | [optional] 
 **name__contains** | **str**| Filters destinations whose names contain this keyword (case-sensitive) | [optional] 
 **name__icontains** | **str**| Filters destinations whose names contain this keyword (case-insensitive) | [optional] 
 **name__iexact** | **str**| Filters destinations with the specified name (case-insensitive) | [optional] 
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]

### Return type

[**PaginatedExternalAPIDestinationList**](PaginatedExternalAPIDestinationList.md)

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

