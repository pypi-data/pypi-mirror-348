# ExternalAPIWaybillDispatchedAmounts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dispatched_amounts** | [**List[ExternalAPIWaybillRowDispatchedAmount]**](ExternalAPIWaybillRowDispatchedAmount.md) | Dispatched amounts | 

## Example

```python
from openapi_client.models.external_api_waybill_dispatched_amounts import ExternalAPIWaybillDispatchedAmounts

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillDispatchedAmounts from a JSON string
external_api_waybill_dispatched_amounts_instance = ExternalAPIWaybillDispatchedAmounts.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillDispatchedAmounts.to_json())

# convert the object into a dict
external_api_waybill_dispatched_amounts_dict = external_api_waybill_dispatched_amounts_instance.to_dict()
# create an instance of ExternalAPIWaybillDispatchedAmounts from a dict
external_api_waybill_dispatched_amounts_from_dict = ExternalAPIWaybillDispatchedAmounts.from_dict(external_api_waybill_dispatched_amounts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


