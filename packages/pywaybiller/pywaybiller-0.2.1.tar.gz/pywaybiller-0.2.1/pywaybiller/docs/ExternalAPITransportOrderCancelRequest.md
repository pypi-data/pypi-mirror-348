# ExternalAPITransportOrderCancelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cancelling_reason** | **str** |  | 
**cancelled_by_user_id** | **int** |  | 

## Example

```python
from openapi_client.models.external_api_transport_order_cancel_request import ExternalAPITransportOrderCancelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderCancelRequest from a JSON string
external_api_transport_order_cancel_request_instance = ExternalAPITransportOrderCancelRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderCancelRequest.to_json())

# convert the object into a dict
external_api_transport_order_cancel_request_dict = external_api_transport_order_cancel_request_instance.to_dict()
# create an instance of ExternalAPITransportOrderCancelRequest from a dict
external_api_transport_order_cancel_request_from_dict = ExternalAPITransportOrderCancelRequest.from_dict(external_api_transport_order_cancel_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


