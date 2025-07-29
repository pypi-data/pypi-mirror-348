# ExternalAPIWaybillVehicleLocation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**latitude** | **float** | The latitude coordinate of the vehicle (eg 59.401034). | [readonly] 
**longitude** | **float** | The longitude coordinate of the vehicle (eg 24.791717). | [readonly] 
**location_timestamp** | **str** | UTC timestamp when vehicle was in that position (eg 2020-05-08T19:06:33). | [readonly] 

## Example

```python
from openapi_client.models.external_api_waybill_vehicle_location import ExternalAPIWaybillVehicleLocation

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillVehicleLocation from a JSON string
external_api_waybill_vehicle_location_instance = ExternalAPIWaybillVehicleLocation.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillVehicleLocation.to_json())

# convert the object into a dict
external_api_waybill_vehicle_location_dict = external_api_waybill_vehicle_location_instance.to_dict()
# create an instance of ExternalAPIWaybillVehicleLocation from a dict
external_api_waybill_vehicle_location_from_dict = ExternalAPIWaybillVehicleLocation.from_dict(external_api_waybill_vehicle_location_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


