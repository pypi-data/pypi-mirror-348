# ExternalAPIWaybillCancel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cancelled_by_user_id** | **int** | The ID of the user that cancels the waybill (eg 28). Use GET Employments endpoint to query all available employments and get necessary &#x60;user_id&#x60; values. | 
**reason** | **str** | Reason for cancellation. | 

## Example

```python
from openapi_client.models.external_api_waybill_cancel import ExternalAPIWaybillCancel

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillCancel from a JSON string
external_api_waybill_cancel_instance = ExternalAPIWaybillCancel.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillCancel.to_json())

# convert the object into a dict
external_api_waybill_cancel_dict = external_api_waybill_cancel_instance.to_dict()
# create an instance of ExternalAPIWaybillCancel from a dict
external_api_waybill_cancel_from_dict = ExternalAPIWaybillCancel.from_dict(external_api_waybill_cancel_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


