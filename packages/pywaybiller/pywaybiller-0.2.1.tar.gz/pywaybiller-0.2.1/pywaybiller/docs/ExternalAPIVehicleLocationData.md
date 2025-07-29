# ExternalAPIVehicleLocationData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**truck_reg_number** | **str** | Vehicle registration number | [readonly] 
**waybill_number** | **str** | Unique waybill reference number | [readonly] 
**transportation_company_name** | **str** | Name of the transport service provider | [readonly] 
**receiver_company_name** | **str** | Name of the receiving company | [readonly] 
**origin_company_name** | **str** | Name of the shipping company | [readonly] 
**origin_name** | **str** | Name of the shipping location | [readonly] 
**destination_name** | **str** | Name of the delivery destination | [readonly] 
**raw_data** | [**ExternalAPIVehicleLocationDataRawData**](ExternalAPIVehicleLocationDataRawData.md) | The IDs of the Waybiller internal objects | [readonly] 
**vehicle_location_data** | **List[Dict[str, ExternalAPIVehicleLocationDataVehicleLocationDataInnerValue]]** | Collection of vehicle location tracking points | [readonly] 

## Example

```python
from openapi_client.models.external_api_vehicle_location_data import ExternalAPIVehicleLocationData

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIVehicleLocationData from a JSON string
external_api_vehicle_location_data_instance = ExternalAPIVehicleLocationData.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIVehicleLocationData.to_json())

# convert the object into a dict
external_api_vehicle_location_data_dict = external_api_vehicle_location_data_instance.to_dict()
# create an instance of ExternalAPIVehicleLocationData from a dict
external_api_vehicle_location_data_from_dict = ExternalAPIVehicleLocationData.from_dict(external_api_vehicle_location_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


