# ExternalAPIPartialOrderUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transportation_companies** | [**List[ExternalAPIOrderTransportCompaniesRequest]**](ExternalAPIOrderTransportCompaniesRequest.md) | The transportation companies the client is using for transporting assortments from origins to destination. | [optional] 
**vehicles** | [**List[ExternalAPIOrderVehiclesRequest]**](ExternalAPIOrderVehiclesRequest.md) | The vehicles that the transportation companies are allowed to use for this order. | [optional] 

## Example

```python
from openapi_client.models.external_api_partial_order_update_request import ExternalAPIPartialOrderUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIPartialOrderUpdateRequest from a JSON string
external_api_partial_order_update_request_instance = ExternalAPIPartialOrderUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIPartialOrderUpdateRequest.to_json())

# convert the object into a dict
external_api_partial_order_update_request_dict = external_api_partial_order_update_request_instance.to_dict()
# create an instance of ExternalAPIPartialOrderUpdateRequest from a dict
external_api_partial_order_update_request_from_dict = ExternalAPIPartialOrderUpdateRequest.from_dict(external_api_partial_order_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


