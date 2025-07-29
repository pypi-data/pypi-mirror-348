# ExternalAPIOrderVehiclesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**truck_reg_number** | **str** | Truck reg number. | [optional] 
**trailer_reg_number** | **str** | Trailer reg number. | [optional] 
**company_reg_code** | **str** | Company reg code that owns the truck. | [optional] 

## Example

```python
from openapi_client.models.external_api_order_vehicles_request import ExternalAPIOrderVehiclesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderVehiclesRequest from a JSON string
external_api_order_vehicles_request_instance = ExternalAPIOrderVehiclesRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderVehiclesRequest.to_json())

# convert the object into a dict
external_api_order_vehicles_request_dict = external_api_order_vehicles_request_instance.to_dict()
# create an instance of ExternalAPIOrderVehiclesRequest from a dict
external_api_order_vehicles_request_from_dict = ExternalAPIOrderVehiclesRequest.from_dict(external_api_order_vehicles_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


