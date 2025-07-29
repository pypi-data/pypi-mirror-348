# ExternalAPIOriginAssortment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique identifier of the origin-assortment relationship | [readonly] 
**origin** | **str** | Name of the origin where the assortment is available | [readonly] 
**assortment** | **str** | Name of the assortment | [readonly] 
**subset_type** | **str** | Type of the assortment subset | [readonly] 
**subset** | **str** | Specific value within the subset type | [readonly] 
**raw_data** | [**ExternalAPIOriginAssortmentRawData**](ExternalAPIOriginAssortmentRawData.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_origin_assortment import ExternalAPIOriginAssortment

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginAssortment from a JSON string
external_api_origin_assortment_instance = ExternalAPIOriginAssortment.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginAssortment.to_json())

# convert the object into a dict
external_api_origin_assortment_dict = external_api_origin_assortment_instance.to_dict()
# create an instance of ExternalAPIOriginAssortment from a dict
external_api_origin_assortment_from_dict = ExternalAPIOriginAssortment.from_dict(external_api_origin_assortment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


