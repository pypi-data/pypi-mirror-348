# ExternalAPIOrderRawData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **int** | Order raw id. | [readonly] 
**number** | **str** | Order number. | [readonly] 
**status** | **int** | The number representing the status of the order. 1 - Mustand, 2 - Aktiivne, 3 - Mitteaktiivne, 4 - Arhiveeritud | [readonly] 
**origins** | **List[int]** | The origins for which the order is created for. | [readonly] 
**owner_company_id** | **str** | Owner company raw id. | [readonly] 
**client_id** | **str** | Client company raw id. | [readonly] 
**origins_assortment** | **List[int]** | The assortment that can be grabbed by an order&#39;s executor. | [readonly] 
**transportation_companies** | **List[int]** | The transportation companies the &#x60;client&#x60; is using for transporting assortments from &#x60;origins&#x60;to &#x60;destination&#x60; | [readonly] 
**vehicles** | **List[int]** | The vehicles that the &#x60;transportation_companies&#x60; are allowed to use for this order. | [readonly] 
**destination** | **int** | The destination to where is order allows transporting assortments. | [readonly] 

## Example

```python
from openapi_client.models.external_api_order_raw_data import ExternalAPIOrderRawData

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderRawData from a JSON string
external_api_order_raw_data_instance = ExternalAPIOrderRawData.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderRawData.to_json())

# convert the object into a dict
external_api_order_raw_data_dict = external_api_order_raw_data_instance.to_dict()
# create an instance of ExternalAPIOrderRawData from a dict
external_api_order_raw_data_from_dict = ExternalAPIOrderRawData.from_dict(external_api_order_raw_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


