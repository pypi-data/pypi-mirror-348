# ExternalAPIWaybillHoldingRight


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cadaster_number** | **str** | Cadaster number. | 
**forest_notices** | **List[str]** | Origin forest notices. | [optional] 

## Example

```python
from openapi_client.models.external_api_waybill_holding_right import ExternalAPIWaybillHoldingRight

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillHoldingRight from a JSON string
external_api_waybill_holding_right_instance = ExternalAPIWaybillHoldingRight.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillHoldingRight.to_json())

# convert the object into a dict
external_api_waybill_holding_right_dict = external_api_waybill_holding_right_instance.to_dict()
# create an instance of ExternalAPIWaybillHoldingRight from a dict
external_api_waybill_holding_right_from_dict = ExternalAPIWaybillHoldingRight.from_dict(external_api_waybill_holding_right_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


