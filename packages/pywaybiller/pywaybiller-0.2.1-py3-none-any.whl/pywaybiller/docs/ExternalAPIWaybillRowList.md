# ExternalAPIWaybillRowList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assortment_id** | **str** | The ID of the assortment. | [readonly] 
**assortment_ids** | **List[str]** | The IDs of the assortments. | [readonly] 
**assortment_raw_id** | **int** | The ID of the assortment. | [optional] 
**scale_assortment_raw_id** | **int** | The ID of the destination scale assortment. | [readonly] 
**assortment_name** | **str** | The name of the assortment. | 
**assortment_unit** | **str** | The unit of the assortment. | 
**dispatched_amount** | **decimal.Decimal** | The dispatched assortment amount. | [readonly] 
**accepted_amount** | **decimal.Decimal** | The accepted assortment amount. | [readonly] 

## Example

```python
from openapi_client.models.external_api_waybill_row_list import ExternalAPIWaybillRowList

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillRowList from a JSON string
external_api_waybill_row_list_instance = ExternalAPIWaybillRowList.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillRowList.to_json())

# convert the object into a dict
external_api_waybill_row_list_dict = external_api_waybill_row_list_instance.to_dict()
# create an instance of ExternalAPIWaybillRowList from a dict
external_api_waybill_row_list_from_dict = ExternalAPIWaybillRowList.from_dict(external_api_waybill_row_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


