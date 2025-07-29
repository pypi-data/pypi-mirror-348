# ExternalAPIWaybillDispatchedAmountsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dispatched_amounts** | [**List[ExternalAPIWaybillRowDispatchedAmountRequest]**](ExternalAPIWaybillRowDispatchedAmountRequest.md) | Dispatched amounts | 

## Example

```python
from openapi_client.models.external_api_waybill_dispatched_amounts_request import ExternalAPIWaybillDispatchedAmountsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillDispatchedAmountsRequest from a JSON string
external_api_waybill_dispatched_amounts_request_instance = ExternalAPIWaybillDispatchedAmountsRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillDispatchedAmountsRequest.to_json())

# convert the object into a dict
external_api_waybill_dispatched_amounts_request_dict = external_api_waybill_dispatched_amounts_request_instance.to_dict()
# create an instance of ExternalAPIWaybillDispatchedAmountsRequest from a dict
external_api_waybill_dispatched_amounts_request_from_dict = ExternalAPIWaybillDispatchedAmountsRequest.from_dict(external_api_waybill_dispatched_amounts_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


