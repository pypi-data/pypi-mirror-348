# openapi_client.OrdersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**orders_create**](OrdersApi.md#orders_create) | **POST** /external-api/orders/ | Creation of an order
[**orders_list**](OrdersApi.md#orders_list) | **GET** /external-api/orders/ | Querying of orders
[**orders_retrieve**](OrdersApi.md#orders_retrieve) | **GET** /external-api/orders/{id}/ | Querying of a single order
[**orders_transportation_update**](OrdersApi.md#orders_transportation_update) | **PUT** /external-api/orders/{id}/transportation/ | Editing of an order transportation companies and vehicles
[**orders_update**](OrdersApi.md#orders_update) | **PUT** /external-api/orders/{id}/ | Editing of an order


# **orders_create**
> ExternalAPIOrderCreate orders_create(external_api_order_create_request)

Creation of an order

Creates a new order.<br><br>
        **NB!** All posted IDs are IDs in your system and these are used to match objects in your system with objects in Waybiller.
        It is also possible to use the Waybiller IDs (`_raw_id`)
        (if you have received it via GET endpoints (e.g. Destinations, Origin assortments).
        Exception is `client`, where the `reg_code` is used as raw id.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_order_create import ExternalAPIOrderCreate
from openapi_client.models.external_api_order_create_request import ExternalAPIOrderCreateRequest
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
    api_instance = openapi_client.OrdersApi(api_client)
    external_api_order_create_request = openapi_client.ExternalAPIOrderCreateRequest() # ExternalAPIOrderCreateRequest | 

    try:
        # Creation of an order
        api_response = api_instance.orders_create(external_api_order_create_request)
        print("The response of OrdersApi->orders_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->orders_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_api_order_create_request** | [**ExternalAPIOrderCreateRequest**](ExternalAPIOrderCreateRequest.md)|  | 

### Return type

[**ExternalAPIOrderCreate**](ExternalAPIOrderCreate.md)

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

# **orders_list**
> PaginatedExternalAPIOrderListList orders_list(limit=limit, offset=offset)

Querying of orders

Returns all orders associated with your company.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_order_list_list import PaginatedExternalAPIOrderListList
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
    api_instance = openapi_client.OrdersApi(api_client)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)

    try:
        # Querying of orders
        api_response = api_instance.orders_list(limit=limit, offset=offset)
        print("The response of OrdersApi->orders_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->orders_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]

### Return type

[**PaginatedExternalAPIOrderListList**](PaginatedExternalAPIOrderListList.md)

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

# **orders_retrieve**
> ExternalAPIOrder orders_retrieve(id)

Querying of a single order

Returns an order with the specified ID. Only companies associated with the order can query it.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_order import ExternalAPIOrder
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
    api_instance = openapi_client.OrdersApi(api_client)
    id = 'id_example' # str | The ID of the order queried.

    try:
        # Querying of a single order
        api_response = api_instance.orders_retrieve(id)
        print("The response of OrdersApi->orders_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->orders_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the order queried. | 

### Return type

[**ExternalAPIOrder**](ExternalAPIOrder.md)

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

# **orders_transportation_update**
> ExternalAPIPartialOrderUpdate orders_transportation_update(id, external_api_partial_order_update_request=external_api_partial_order_update_request)

Editing of an order transportation companies and vehicles

Edits order transportation companies and vehicles data. It is allowed to be used by order's client company

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_partial_order_update import ExternalAPIPartialOrderUpdate
from openapi_client.models.external_api_partial_order_update_request import ExternalAPIPartialOrderUpdateRequest
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
    api_instance = openapi_client.OrdersApi(api_client)
    id = 56 # int | A unique integer value identifying this Order.
    external_api_partial_order_update_request = openapi_client.ExternalAPIPartialOrderUpdateRequest() # ExternalAPIPartialOrderUpdateRequest |  (optional)

    try:
        # Editing of an order transportation companies and vehicles
        api_response = api_instance.orders_transportation_update(id, external_api_partial_order_update_request=external_api_partial_order_update_request)
        print("The response of OrdersApi->orders_transportation_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->orders_transportation_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this Order. | 
 **external_api_partial_order_update_request** | [**ExternalAPIPartialOrderUpdateRequest**](ExternalAPIPartialOrderUpdateRequest.md)|  | [optional] 

### Return type

[**ExternalAPIPartialOrderUpdate**](ExternalAPIPartialOrderUpdate.md)

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

# **orders_update**
> ExternalAPIOrderUpdate orders_update(id, external_api_order_update_request=external_api_order_update_request)

Editing of an order

Edits order. It is allowed to be used by order's owner company

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_order_update import ExternalAPIOrderUpdate
from openapi_client.models.external_api_order_update_request import ExternalAPIOrderUpdateRequest
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
    api_instance = openapi_client.OrdersApi(api_client)
    id = 56 # int | A unique integer value identifying this Order.
    external_api_order_update_request = openapi_client.ExternalAPIOrderUpdateRequest() # ExternalAPIOrderUpdateRequest |  (optional)

    try:
        # Editing of an order
        api_response = api_instance.orders_update(id, external_api_order_update_request=external_api_order_update_request)
        print("The response of OrdersApi->orders_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->orders_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this Order. | 
 **external_api_order_update_request** | [**ExternalAPIOrderUpdateRequest**](ExternalAPIOrderUpdateRequest.md)|  | [optional] 

### Return type

[**ExternalAPIOrderUpdate**](ExternalAPIOrderUpdate.md)

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

