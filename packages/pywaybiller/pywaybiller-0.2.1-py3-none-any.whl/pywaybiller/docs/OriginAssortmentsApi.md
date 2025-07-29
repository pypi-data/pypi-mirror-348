# openapi_client.OriginAssortmentsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**origin_assortments_list**](OriginAssortmentsApi.md#origin_assortments_list) | **GET** /external-api/origin-assortments/ | Querying origin assortments
[**origin_assortments_retrieve**](OriginAssortmentsApi.md#origin_assortments_retrieve) | **GET** /external-api/origin-assortments/{id}/ | Querying a single origin assortment


# **origin_assortments_list**
> PaginatedExternalAPIOriginAssortmentList origin_assortments_list(assortment__name=assortment__name, assortment__name__contains=assortment__name__contains, assortment__name__icontains=assortment__name__icontains, assortment__name__iexact=assortment__name__iexact, limit=limit, offset=offset, origin__id=origin__id, origin__id__gt=origin__id__gt, origin__id__gte=origin__id__gte, origin__id__in=origin__id__in, origin__id__lt=origin__id__lt, origin__id__lte=origin__id__lte, origin__name=origin__name, origin__name__contains=origin__name__contains, origin__name__icontains=origin__name__icontains, origin__name__iexact=origin__name__iexact, subset__subset_type__name=subset__subset_type__name, subset__subset_type__name__contains=subset__subset_type__name__contains, subset__subset_type__name__icontains=subset__subset_type__name__icontains, subset__subset_type__name__iexact=subset__subset_type__name__iexact, subset__value=subset__value, subset__value__contains=subset__value__contains, subset__value__icontains=subset__value__icontains, subset__value__iexact=subset__value__iexact)

Querying origin assortments

Returns all origin assortments associated with your company based on specified filters.

Available assortments include:
- Your company's origin assortments
- Your partner companies' origin assortments
- Public origin assortments


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_origin_assortment_list import PaginatedExternalAPIOriginAssortmentList
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
    api_instance = openapi_client.OriginAssortmentsApi(api_client)
    assortment__name = 'assortment__name_example' # str | Filters origin assortments by exact assortment name (case-sensitive) (optional)
    assortment__name__contains = 'assortment__name__contains_example' # str | Filters origin assortments where the assortment name contains the specified keyword (case-sensitive) (optional)
    assortment__name__icontains = 'assortment__name__icontains_example' # str | Filters origin assortments where the assortment name contains the specified keyword (case-insensitive) (optional)
    assortment__name__iexact = 'assortment__name__iexact_example' # str | Filters origin assortments by exact assortment name (case-insensitive) (optional)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)
    origin__id = 56 # int | Filters origin assortments by exact origin ID (optional)
    origin__id__gt = 56 # int | Filters origin assortments where origin ID is greater than the specified value (optional)
    origin__id__gte = 56 # int | Filters origin assortments where origin ID is greater than or equal to the specified value (optional)
    origin__id__in = 56 # int | Filters origin assortments by a comma-separated list of origin IDs (optional)
    origin__id__lt = 56 # int | Filters origin assortments where origin ID is less than the specified value (optional)
    origin__id__lte = 56 # int | Filters origin assortments where origin ID is less than or equal to the specified value (optional)
    origin__name = 'origin__name_example' # str | Filters origin assortments by exact origin name (case-sensitive) (optional)
    origin__name__contains = 'origin__name__contains_example' # str | Filters origin assortments where the origin name contains the specified keyword (case-sensitive) (optional)
    origin__name__icontains = 'origin__name__icontains_example' # str | Filters origin assortments where the origin name contains the specified keyword (case-insensitive) (optional)
    origin__name__iexact = 'origin__name__iexact_example' # str | Filters origin assortments by exact origin name (case-insensitive) (optional)
    subset__subset_type__name = 'subset__subset_type__name_example' # str | Filters origin assortments by exact subset type name (case-sensitive) (optional)
    subset__subset_type__name__contains = 'subset__subset_type__name__contains_example' # str | Filters origin assortments where the subset type name contains the specified keyword (case-sensitive) (optional)
    subset__subset_type__name__icontains = 'subset__subset_type__name__icontains_example' # str | Filters origin assortments where the subset type name contains the specified keyword (case-insensitive) (optional)
    subset__subset_type__name__iexact = 'subset__subset_type__name__iexact_example' # str | Filters origin assortments by exact subset type name (case-insensitive) (optional)
    subset__value = 'subset__value_example' # str | Filters origin assortments by exact subset value (case-sensitive) (optional)
    subset__value__contains = 'subset__value__contains_example' # str | Filters origin assortments where the subset value contains the specified keyword (case-sensitive) (optional)
    subset__value__icontains = 'subset__value__icontains_example' # str | Filters origin assortments where the subset value contains the specified keyword (case-insensitive) (optional)
    subset__value__iexact = 'subset__value__iexact_example' # str | Filters origin assortments by exact subset value (case-insensitive) (optional)

    try:
        # Querying origin assortments
        api_response = api_instance.origin_assortments_list(assortment__name=assortment__name, assortment__name__contains=assortment__name__contains, assortment__name__icontains=assortment__name__icontains, assortment__name__iexact=assortment__name__iexact, limit=limit, offset=offset, origin__id=origin__id, origin__id__gt=origin__id__gt, origin__id__gte=origin__id__gte, origin__id__in=origin__id__in, origin__id__lt=origin__id__lt, origin__id__lte=origin__id__lte, origin__name=origin__name, origin__name__contains=origin__name__contains, origin__name__icontains=origin__name__icontains, origin__name__iexact=origin__name__iexact, subset__subset_type__name=subset__subset_type__name, subset__subset_type__name__contains=subset__subset_type__name__contains, subset__subset_type__name__icontains=subset__subset_type__name__icontains, subset__subset_type__name__iexact=subset__subset_type__name__iexact, subset__value=subset__value, subset__value__contains=subset__value__contains, subset__value__icontains=subset__value__icontains, subset__value__iexact=subset__value__iexact)
        print("The response of OriginAssortmentsApi->origin_assortments_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OriginAssortmentsApi->origin_assortments_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **assortment__name** | **str**| Filters origin assortments by exact assortment name (case-sensitive) | [optional] 
 **assortment__name__contains** | **str**| Filters origin assortments where the assortment name contains the specified keyword (case-sensitive) | [optional] 
 **assortment__name__icontains** | **str**| Filters origin assortments where the assortment name contains the specified keyword (case-insensitive) | [optional] 
 **assortment__name__iexact** | **str**| Filters origin assortments by exact assortment name (case-insensitive) | [optional] 
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]
 **origin__id** | **int**| Filters origin assortments by exact origin ID | [optional] 
 **origin__id__gt** | **int**| Filters origin assortments where origin ID is greater than the specified value | [optional] 
 **origin__id__gte** | **int**| Filters origin assortments where origin ID is greater than or equal to the specified value | [optional] 
 **origin__id__in** | **int**| Filters origin assortments by a comma-separated list of origin IDs | [optional] 
 **origin__id__lt** | **int**| Filters origin assortments where origin ID is less than the specified value | [optional] 
 **origin__id__lte** | **int**| Filters origin assortments where origin ID is less than or equal to the specified value | [optional] 
 **origin__name** | **str**| Filters origin assortments by exact origin name (case-sensitive) | [optional] 
 **origin__name__contains** | **str**| Filters origin assortments where the origin name contains the specified keyword (case-sensitive) | [optional] 
 **origin__name__icontains** | **str**| Filters origin assortments where the origin name contains the specified keyword (case-insensitive) | [optional] 
 **origin__name__iexact** | **str**| Filters origin assortments by exact origin name (case-insensitive) | [optional] 
 **subset__subset_type__name** | **str**| Filters origin assortments by exact subset type name (case-sensitive) | [optional] 
 **subset__subset_type__name__contains** | **str**| Filters origin assortments where the subset type name contains the specified keyword (case-sensitive) | [optional] 
 **subset__subset_type__name__icontains** | **str**| Filters origin assortments where the subset type name contains the specified keyword (case-insensitive) | [optional] 
 **subset__subset_type__name__iexact** | **str**| Filters origin assortments by exact subset type name (case-insensitive) | [optional] 
 **subset__value** | **str**| Filters origin assortments by exact subset value (case-sensitive) | [optional] 
 **subset__value__contains** | **str**| Filters origin assortments where the subset value contains the specified keyword (case-sensitive) | [optional] 
 **subset__value__icontains** | **str**| Filters origin assortments where the subset value contains the specified keyword (case-insensitive) | [optional] 
 **subset__value__iexact** | **str**| Filters origin assortments by exact subset value (case-insensitive) | [optional] 

### Return type

[**PaginatedExternalAPIOriginAssortmentList**](PaginatedExternalAPIOriginAssortmentList.md)

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

# **origin_assortments_retrieve**
> ExternalAPIOriginAssortment origin_assortments_retrieve(id)

Querying a single origin assortment

Returns a specific origin assortment by ID.
Access is limited to origin assortments that your company has permission to view:
- Your company's origin assortments
- Your partner companies' origin assortments
- Public origin assortments

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_origin_assortment import ExternalAPIOriginAssortment
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
    api_instance = openapi_client.OriginAssortmentsApi(api_client)
    id = 56 # int | A unique integer value identifying this origin assortment.

    try:
        # Querying a single origin assortment
        api_response = api_instance.origin_assortments_retrieve(id)
        print("The response of OriginAssortmentsApi->origin_assortments_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OriginAssortmentsApi->origin_assortments_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this origin assortment. | 

### Return type

[**ExternalAPIOriginAssortment**](ExternalAPIOriginAssortment.md)

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

