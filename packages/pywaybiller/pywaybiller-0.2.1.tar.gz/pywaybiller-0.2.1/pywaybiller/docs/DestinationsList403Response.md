# DestinationsList403Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**detail** | **str** | Provided API key is not correct or expired | [optional] 

## Example

```python
from openapi_client.models.destinations_list403_response import DestinationsList403Response

# TODO update the JSON string below
json = "{}"
# create an instance of DestinationsList403Response from a JSON string
destinations_list403_response_instance = DestinationsList403Response.from_json(json)
# print the JSON string representation of the object
print(DestinationsList403Response.to_json())

# convert the object into a dict
destinations_list403_response_dict = destinations_list403_response_instance.to_dict()
# create an instance of DestinationsList403Response from a dict
destinations_list403_response_from_dict = DestinationsList403Response.from_dict(destinations_list403_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


