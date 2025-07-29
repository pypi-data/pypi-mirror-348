# ExternalAPIWaybillStartDriveRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**driver_user_id** | **int** | The ID of the driver user (eg 28). Use GET Employments endpoint to query all available employments and get necessary &#x60;user_id&#x60; values. | 
**truck_id** | **int** | The ID of the vehicle (eg 1410). Use GET Vehicles endpoint to query all available vehicles and get necessary &#x60;id&#x60; values. | [optional] 
**destination_id** | **str** | The ID of the destination (eg 330). This value is required if the Waybill is missing Destination. Use GET Destinations endpoint to query all available destinations and get necessary &#x60;id&#x60; values. | [optional] 

## Example

```python
from openapi_client.models.external_api_waybill_start_drive_request import ExternalAPIWaybillStartDriveRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillStartDriveRequest from a JSON string
external_api_waybill_start_drive_request_instance = ExternalAPIWaybillStartDriveRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillStartDriveRequest.to_json())

# convert the object into a dict
external_api_waybill_start_drive_request_dict = external_api_waybill_start_drive_request_instance.to_dict()
# create an instance of ExternalAPIWaybillStartDriveRequest from a dict
external_api_waybill_start_drive_request_from_dict = ExternalAPIWaybillStartDriveRequest.from_dict(external_api_waybill_start_drive_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


