# ExternalAPIVehicle


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique identifier for the vehicle | [readonly] 
**reg_number** | **str** | Registration number of the truck | [readonly] 
**trailer_reg_number** | **str** | Registration number of the attached trailer, if applicable | [readonly] 
**inactive** | **bool** | Indicates if the vehicle has been deactivated | [readonly] 
**company_name** | **str** | Name of the company owning the vehicle | [readonly] 
**company_reg_code** | **str** | Registration code of the company owning the vehicle | [readonly] 

## Example

```python
from openapi_client.models.external_api_vehicle import ExternalAPIVehicle

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIVehicle from a JSON string
external_api_vehicle_instance = ExternalAPIVehicle.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIVehicle.to_json())

# convert the object into a dict
external_api_vehicle_dict = external_api_vehicle_instance.to_dict()
# create an instance of ExternalAPIVehicle from a dict
external_api_vehicle_from_dict = ExternalAPIVehicle.from_dict(external_api_vehicle_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


