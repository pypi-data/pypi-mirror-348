# ExternalAPITransportOrderList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_order_id** | **str** |  | [readonly] 
**transport_date** | **date** |  | [readonly] 
**origin_id** | **str** | Unique identifier of the origin in your system | 
**origin_name** | **str** |  | [optional] 
**origin_address** | **str** |  | [optional] 
**destination_id** | **str** | Unique identifier of the destination in your system | 
**destination_name** | **str** |  | [optional] 
**destination_address** | **str** |  | [optional] 
**assortment_name** | **str** |  | [readonly] 
**transportation_company_name** | **str** |  | [optional] 
**truck_reg_number** | **str** |  | [optional] 
**trailer_reg_number** | **str** |  | [optional] 
**waybills_ids** | **List[int]** |  | [readonly] 
**raw_data** | [**ExternalAPITransportOrderRawDataList**](ExternalAPITransportOrderRawDataList.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_transport_order_list import ExternalAPITransportOrderList

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderList from a JSON string
external_api_transport_order_list_instance = ExternalAPITransportOrderList.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderList.to_json())

# convert the object into a dict
external_api_transport_order_list_dict = external_api_transport_order_list_instance.to_dict()
# create an instance of ExternalAPITransportOrderList from a dict
external_api_transport_order_list_from_dict = ExternalAPITransportOrderList.from_dict(external_api_transport_order_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


