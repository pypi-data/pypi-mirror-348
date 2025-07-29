# ExternalAPIWaybillHoldingRightRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cadaster_number** | **str** | Cadaster number. | 
**forest_notices** | **List[str]** | Origin forest notices. | [optional] 

## Example

```python
from openapi_client.models.external_api_waybill_holding_right_request import ExternalAPIWaybillHoldingRightRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillHoldingRightRequest from a JSON string
external_api_waybill_holding_right_request_instance = ExternalAPIWaybillHoldingRightRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillHoldingRightRequest.to_json())

# convert the object into a dict
external_api_waybill_holding_right_request_dict = external_api_waybill_holding_right_request_instance.to_dict()
# create an instance of ExternalAPIWaybillHoldingRightRequest from a dict
external_api_waybill_holding_right_request_from_dict = ExternalAPIWaybillHoldingRightRequest.from_dict(external_api_waybill_holding_right_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


