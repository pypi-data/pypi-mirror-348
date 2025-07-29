# ExternalAPIOriginAssortmentRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Assortment ID | 
**subsets** | **List[int]** | List of subset IDs | [optional] [default to []]

## Example

```python
from openapi_client.models.external_api_origin_assortment_request import ExternalAPIOriginAssortmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginAssortmentRequest from a JSON string
external_api_origin_assortment_request_instance = ExternalAPIOriginAssortmentRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginAssortmentRequest.to_json())

# convert the object into a dict
external_api_origin_assortment_request_dict = external_api_origin_assortment_request_instance.to_dict()
# create an instance of ExternalAPIOriginAssortmentRequest from a dict
external_api_origin_assortment_request_from_dict = ExternalAPIOriginAssortmentRequest.from_dict(external_api_origin_assortment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


