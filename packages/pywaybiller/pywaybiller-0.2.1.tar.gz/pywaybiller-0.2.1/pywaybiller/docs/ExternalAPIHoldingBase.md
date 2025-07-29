# ExternalAPIHoldingBase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**TypeEnum**](TypeEnum.md) |  | [optional] 
**contract_number** | **str** |  | [optional] 
**contract_date** | **str** |  | [optional] 
**previous_owner** | [**ExternalAPIHoldingBasePreviousOwner**](ExternalAPIHoldingBasePreviousOwner.md) |  | [optional] 

## Example

```python
from openapi_client.models.external_api_holding_base import ExternalAPIHoldingBase

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIHoldingBase from a JSON string
external_api_holding_base_instance = ExternalAPIHoldingBase.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIHoldingBase.to_json())

# convert the object into a dict
external_api_holding_base_dict = external_api_holding_base_instance.to_dict()
# create an instance of ExternalAPIHoldingBase from a dict
external_api_holding_base_from_dict = ExternalAPIHoldingBase.from_dict(external_api_holding_base_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


