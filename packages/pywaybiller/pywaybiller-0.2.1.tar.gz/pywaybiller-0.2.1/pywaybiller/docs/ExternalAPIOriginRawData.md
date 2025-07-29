# ExternalAPIOriginRawData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique identifier of the origin | [readonly] 
**only_origin_owner_can_create_waybills** | **bool** | Only origin owner can create waybills from this origin | [readonly] 

## Example

```python
from openapi_client.models.external_api_origin_raw_data import ExternalAPIOriginRawData

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginRawData from a JSON string
external_api_origin_raw_data_instance = ExternalAPIOriginRawData.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginRawData.to_json())

# convert the object into a dict
external_api_origin_raw_data_dict = external_api_origin_raw_data_instance.to_dict()
# create an instance of ExternalAPIOriginRawData from a dict
external_api_origin_raw_data_from_dict = ExternalAPIOriginRawData.from_dict(external_api_origin_raw_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


