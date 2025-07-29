# ExternalAPIWaybillAccept


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**updated_mileage** | **int** | Total mileage driven (in kilometres). This needs to be filled only if the mileage is updated as it overwrites the mileage entered by the driver. | [optional] 
**confirmed_by_user_id** | **int** | The ID of the user that accepts the waybill (eg 28). Use GET Employments endpoint to query all available employments and get necessary &#x60;user_id&#x60; values. | 
**accepted_amounts** | [**List[ExternalAPIWaybillRowAcceptedAmount]**](ExternalAPIWaybillRowAcceptedAmount.md) | Accepted amounts | 

## Example

```python
from openapi_client.models.external_api_waybill_accept import ExternalAPIWaybillAccept

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillAccept from a JSON string
external_api_waybill_accept_instance = ExternalAPIWaybillAccept.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillAccept.to_json())

# convert the object into a dict
external_api_waybill_accept_dict = external_api_waybill_accept_instance.to_dict()
# create an instance of ExternalAPIWaybillAccept from a dict
external_api_waybill_accept_from_dict = ExternalAPIWaybillAccept.from_dict(external_api_waybill_accept_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


