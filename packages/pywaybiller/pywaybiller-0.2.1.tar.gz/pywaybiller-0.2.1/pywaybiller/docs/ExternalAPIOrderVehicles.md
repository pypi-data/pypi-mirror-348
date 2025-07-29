# ExternalAPIOrderVehicles


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**truck_reg_number** | **str** | Truck reg number. | [optional] 
**trailer_reg_number** | **str** | Trailer reg number. | [optional] 
**company_reg_code** | **str** | Company reg code that owns the truck. | [optional] 

## Example

```python
from openapi_client.models.external_api_order_vehicles import ExternalAPIOrderVehicles

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderVehicles from a JSON string
external_api_order_vehicles_instance = ExternalAPIOrderVehicles.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderVehicles.to_json())

# convert the object into a dict
external_api_order_vehicles_dict = external_api_order_vehicles_instance.to_dict()
# create an instance of ExternalAPIOrderVehicles from a dict
external_api_order_vehicles_from_dict = ExternalAPIOrderVehicles.from_dict(external_api_order_vehicles_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


