# ExternalAPIPartialOrderUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transportation_companies** | [**List[ExternalAPIOrderTransportCompanies]**](ExternalAPIOrderTransportCompanies.md) | The transportation companies the client is using for transporting assortments from origins to destination. | [optional] 
**vehicles** | [**List[ExternalAPIOrderVehicles]**](ExternalAPIOrderVehicles.md) | The vehicles that the transportation companies are allowed to use for this order. | [optional] 

## Example

```python
from openapi_client.models.external_api_partial_order_update import ExternalAPIPartialOrderUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIPartialOrderUpdate from a JSON string
external_api_partial_order_update_instance = ExternalAPIPartialOrderUpdate.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIPartialOrderUpdate.to_json())

# convert the object into a dict
external_api_partial_order_update_dict = external_api_partial_order_update_instance.to_dict()
# create an instance of ExternalAPIPartialOrderUpdate from a dict
external_api_partial_order_update_from_dict = ExternalAPIPartialOrderUpdate.from_dict(external_api_partial_order_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


