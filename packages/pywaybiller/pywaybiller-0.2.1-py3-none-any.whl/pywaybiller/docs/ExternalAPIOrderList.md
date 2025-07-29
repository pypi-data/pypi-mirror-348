# ExternalAPIOrderList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | Order id. | [readonly] 
**number** | **str** | Order number. | [readonly] 
**status** | **str** | The status of the order. | [readonly] 
**period** | **List[date]** | The date range when the order is active. | 
**origins** | [**List[ExternalAPIOrderOrigin]**](ExternalAPIOrderOrigin.md) | The origins for which the order is created for. | [readonly] 
**owner_company_name** | **str** | Name of the company who owns the order. | [readonly] 
**client_company_name** | **str** | Name of the company for whom the order is created for. | [readonly] 
**destination_name** | **str** | Destination name. | [readonly] 
**total_allowed_amount** | **decimal.Decimal** | Total allowed amount. | [readonly] 
**raw_data** | [**ExternalAPIOrderRawData**](ExternalAPIOrderRawData.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_order_list import ExternalAPIOrderList

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderList from a JSON string
external_api_order_list_instance = ExternalAPIOrderList.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderList.to_json())

# convert the object into a dict
external_api_order_list_dict = external_api_order_list_instance.to_dict()
# create an instance of ExternalAPIOrderList from a dict
external_api_order_list_from_dict = ExternalAPIOrderList.from_dict(external_api_order_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


