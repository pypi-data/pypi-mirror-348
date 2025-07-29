# ExternalAPITransportOrderUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pallets_number** | **int** |  | [optional] 
**origin_id** | **int** |  | [optional] 
**origin_raw_id** | **str** |  | [optional] 
**origin_name** | **str** |  | [optional] 
**origin_address** | **str** |  | [optional] 
**origin_latitude** | **float** |  | [optional] 
**origin_longitude** | **float** |  | [optional] 
**shipper_company_name** | **str** |  | [optional] 
**shipper_company_reg_code** | **str** |  | [optional] 
**destination_id** | **int** |  | [optional] 
**destination_raw_id** | **str** |  | [optional] 
**destination_name** | **str** |  | [optional] 
**destination_address** | **str** |  | [optional] 
**destination_latitude** | **float** |  | [optional] 
**destination_longitude** | **float** |  | [optional] 
**receiver_company_name** | **str** |  | [optional] 
**receiver_company_reg_code** | **str** |  | [optional] 
**truck_reg_number** | **str** |  | [optional] 
**trailer_reg_number** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.external_api_transport_order_update_request import ExternalAPITransportOrderUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderUpdateRequest from a JSON string
external_api_transport_order_update_request_instance = ExternalAPITransportOrderUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderUpdateRequest.to_json())

# convert the object into a dict
external_api_transport_order_update_request_dict = external_api_transport_order_update_request_instance.to_dict()
# create an instance of ExternalAPITransportOrderUpdateRequest from a dict
external_api_transport_order_update_request_from_dict = ExternalAPITransportOrderUpdateRequest.from_dict(external_api_transport_order_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


