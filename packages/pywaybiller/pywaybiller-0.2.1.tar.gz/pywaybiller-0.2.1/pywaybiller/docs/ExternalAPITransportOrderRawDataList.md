# ExternalAPITransportOrderRawDataList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_order_id** | **int** |  | [readonly] 
**status** | [**TransportOrderStatusEnum**](TransportOrderStatusEnum.md) |  | [readonly] 
**number** | **str** |  | [readonly] 
**origin_id** | **int** |  | [readonly] 
**destination_id** | **int** |  | [readonly] 
**entity_code** | **str** |  | [readonly] 
**waybills_ids** | **List[int]** |  | [readonly] 

## Example

```python
from openapi_client.models.external_api_transport_order_raw_data_list import ExternalAPITransportOrderRawDataList

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderRawDataList from a JSON string
external_api_transport_order_raw_data_list_instance = ExternalAPITransportOrderRawDataList.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderRawDataList.to_json())

# convert the object into a dict
external_api_transport_order_raw_data_list_dict = external_api_transport_order_raw_data_list_instance.to_dict()
# create an instance of ExternalAPITransportOrderRawDataList from a dict
external_api_transport_order_raw_data_list_from_dict = ExternalAPITransportOrderRawDataList.from_dict(external_api_transport_order_raw_data_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


