# ExternalAPIWaybillAcceptedAmounts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accepted_amounts** | [**List[ExternalAPIWaybillRowAcceptedAmount]**](ExternalAPIWaybillRowAcceptedAmount.md) | Accepted amounts | 

## Example

```python
from openapi_client.models.external_api_waybill_accepted_amounts import ExternalAPIWaybillAcceptedAmounts

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillAcceptedAmounts from a JSON string
external_api_waybill_accepted_amounts_instance = ExternalAPIWaybillAcceptedAmounts.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillAcceptedAmounts.to_json())

# convert the object into a dict
external_api_waybill_accepted_amounts_dict = external_api_waybill_accepted_amounts_instance.to_dict()
# create an instance of ExternalAPIWaybillAcceptedAmounts from a dict
external_api_waybill_accepted_amounts_from_dict = ExternalAPIWaybillAcceptedAmounts.from_dict(external_api_waybill_accepted_amounts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


