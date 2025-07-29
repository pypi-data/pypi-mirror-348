# ExternalAPIOriginLocation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique identifier of the origin&#39;s location | [readonly] 
**address** | **str** | Physical address of the origin | 
**lat** | **float** | Latitude coordinate of the origin&#39;s location | 
**lng** | **float** | Longitude coordinate of the origin&#39;s location | 
**gmaps_link** | **str** | Direct Google Maps link to the location for navigation purposes | [readonly] 

## Example

```python
from openapi_client.models.external_api_origin_location import ExternalAPIOriginLocation

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginLocation from a JSON string
external_api_origin_location_instance = ExternalAPIOriginLocation.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginLocation.to_json())

# convert the object into a dict
external_api_origin_location_dict = external_api_origin_location_instance.to_dict()
# create an instance of ExternalAPIOriginLocation from a dict
external_api_origin_location_from_dict = ExternalAPIOriginLocation.from_dict(external_api_origin_location_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


