# ExternalAPIHoldingBaseRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**TypeEnum**](TypeEnum.md) |  | [optional] 
**contract_number** | **str** |  | [optional] 
**contract_date** | **str** |  | [optional] 
**previous_owner** | [**ExternalAPIHoldingBasePreviousOwnerRequest**](ExternalAPIHoldingBasePreviousOwnerRequest.md) |  | [optional] 

## Example

```python
from openapi_client.models.external_api_holding_base_request import ExternalAPIHoldingBaseRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIHoldingBaseRequest from a JSON string
external_api_holding_base_request_instance = ExternalAPIHoldingBaseRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIHoldingBaseRequest.to_json())

# convert the object into a dict
external_api_holding_base_request_dict = external_api_holding_base_request_instance.to_dict()
# create an instance of ExternalAPIHoldingBaseRequest from a dict
external_api_holding_base_request_from_dict = ExternalAPIHoldingBaseRequest.from_dict(external_api_holding_base_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


