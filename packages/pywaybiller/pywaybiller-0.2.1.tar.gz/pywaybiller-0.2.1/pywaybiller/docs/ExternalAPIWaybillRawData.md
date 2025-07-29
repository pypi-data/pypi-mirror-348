# ExternalAPIWaybillRawData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waybill_id** | **int** | The ID of the waybill. | [readonly] 
**truck_id** | **int** | The ID of the truck. | [readonly] 
**driver_user_id** | **int** | The ID of the driver. | [readonly] 
**origin_id** | **int** | The ID of the origin. | [readonly] 
**destination_id** | **int** | The ID of the destination. | [readonly] 
**rows** | [**List[ExternalAPIWaybillRowRawData]**](ExternalAPIWaybillRowRawData.md) | Waybill rows. | [readonly] 
**user_defined_fields** | **Dict[str, object]** | User defined fields. | [readonly] 

## Example

```python
from openapi_client.models.external_api_waybill_raw_data import ExternalAPIWaybillRawData

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillRawData from a JSON string
external_api_waybill_raw_data_instance = ExternalAPIWaybillRawData.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillRawData.to_json())

# convert the object into a dict
external_api_waybill_raw_data_dict = external_api_waybill_raw_data_instance.to_dict()
# create an instance of ExternalAPIWaybillRawData from a dict
external_api_waybill_raw_data_from_dict = ExternalAPIWaybillRawData.from_dict(external_api_waybill_raw_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


