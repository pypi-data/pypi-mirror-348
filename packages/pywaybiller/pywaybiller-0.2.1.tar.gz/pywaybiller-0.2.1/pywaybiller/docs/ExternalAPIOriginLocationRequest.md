# ExternalAPIOriginLocationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | **str** | Physical address of the origin | 
**lat** | **float** | Latitude coordinate of the origin&#39;s location | 
**lng** | **float** | Longitude coordinate of the origin&#39;s location | 

## Example

```python
from openapi_client.models.external_api_origin_location_request import ExternalAPIOriginLocationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginLocationRequest from a JSON string
external_api_origin_location_request_instance = ExternalAPIOriginLocationRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginLocationRequest.to_json())

# convert the object into a dict
external_api_origin_location_request_dict = external_api_origin_location_request_instance.to_dict()
# create an instance of ExternalAPIOriginLocationRequest from a dict
external_api_origin_location_request_from_dict = ExternalAPIOriginLocationRequest.from_dict(external_api_origin_location_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


