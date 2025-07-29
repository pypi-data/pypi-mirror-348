# ExternalAPIOriginAssortmentRawData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique identifier of the origin-assortment relationship | [readonly] 
**origin_id** | **int** | Unique identifier of the origin | [readonly] 
**assortment_id** | **int** | Unique identifier of the assortment | [readonly] 
**subset_type_id** | **int** | Unique identifier of the subset type that categorizes the assortment | [readonly] 
**subset_id** | **int** | Unique identifier of the assortment subset | [readonly] 

## Example

```python
from openapi_client.models.external_api_origin_assortment_raw_data import ExternalAPIOriginAssortmentRawData

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginAssortmentRawData from a JSON string
external_api_origin_assortment_raw_data_instance = ExternalAPIOriginAssortmentRawData.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginAssortmentRawData.to_json())

# convert the object into a dict
external_api_origin_assortment_raw_data_dict = external_api_origin_assortment_raw_data_instance.to_dict()
# create an instance of ExternalAPIOriginAssortmentRawData from a dict
external_api_origin_assortment_raw_data_from_dict = ExternalAPIOriginAssortmentRawData.from_dict(external_api_origin_assortment_raw_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


