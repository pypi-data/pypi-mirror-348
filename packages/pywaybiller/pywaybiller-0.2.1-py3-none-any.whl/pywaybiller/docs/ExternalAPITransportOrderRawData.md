# ExternalAPITransportOrderRawData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_order_id** | **int** |  | [readonly] 
**order_id** | **int** | Order which was used for creating | [readonly] 
**rows** | [**List[ExternalAPITransportOrderRowRawData]**](ExternalAPITransportOrderRowRawData.md) |  | [readonly] 
**destination_id** | **int** |  | [readonly] 
**origin_id** | **int** |  | [readonly] 
**organizer_user_id** | **int** |  | [readonly] 
**entity_code** | **str** |  | [readonly] 
**waybills_ids** | **List[int]** |  | [readonly] 

## Example

```python
from openapi_client.models.external_api_transport_order_raw_data import ExternalAPITransportOrderRawData

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderRawData from a JSON string
external_api_transport_order_raw_data_instance = ExternalAPITransportOrderRawData.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderRawData.to_json())

# convert the object into a dict
external_api_transport_order_raw_data_dict = external_api_transport_order_raw_data_instance.to_dict()
# create an instance of ExternalAPITransportOrderRawData from a dict
external_api_transport_order_raw_data_from_dict = ExternalAPITransportOrderRawData.from_dict(external_api_transport_order_raw_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


