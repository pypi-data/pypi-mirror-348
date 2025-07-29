# ExternalAPIVehicleLocationDataRawData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waybill_id** | **int** | Unique identifier of the waybill | [readonly] 
**destination_id** | **int** | Unique identifier of the destination | [readonly] 
**origin_id** | **int** | Unique identifier of the origin | [readonly] 
**truck_id** | **int** | Unique identifier of the truck | [readonly] 

## Example

```python
from openapi_client.models.external_api_vehicle_location_data_raw_data import ExternalAPIVehicleLocationDataRawData

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIVehicleLocationDataRawData from a JSON string
external_api_vehicle_location_data_raw_data_instance = ExternalAPIVehicleLocationDataRawData.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIVehicleLocationDataRawData.to_json())

# convert the object into a dict
external_api_vehicle_location_data_raw_data_dict = external_api_vehicle_location_data_raw_data_instance.to_dict()
# create an instance of ExternalAPIVehicleLocationDataRawData from a dict
external_api_vehicle_location_data_raw_data_from_dict = ExternalAPIVehicleLocationDataRawData.from_dict(external_api_vehicle_location_data_raw_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


