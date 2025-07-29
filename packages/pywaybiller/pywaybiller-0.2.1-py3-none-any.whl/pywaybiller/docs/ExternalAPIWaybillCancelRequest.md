# ExternalAPIWaybillCancelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cancelled_by_user_id** | **int** | The ID of the user that cancels the waybill (eg 28). Use GET Employments endpoint to query all available employments and get necessary &#x60;user_id&#x60; values. | 
**reason** | **str** | Reason for cancellation. | 

## Example

```python
from openapi_client.models.external_api_waybill_cancel_request import ExternalAPIWaybillCancelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillCancelRequest from a JSON string
external_api_waybill_cancel_request_instance = ExternalAPIWaybillCancelRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillCancelRequest.to_json())

# convert the object into a dict
external_api_waybill_cancel_request_dict = external_api_waybill_cancel_request_instance.to_dict()
# create an instance of ExternalAPIWaybillCancelRequest from a dict
external_api_waybill_cancel_request_from_dict = ExternalAPIWaybillCancelRequest.from_dict(external_api_waybill_cancel_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


