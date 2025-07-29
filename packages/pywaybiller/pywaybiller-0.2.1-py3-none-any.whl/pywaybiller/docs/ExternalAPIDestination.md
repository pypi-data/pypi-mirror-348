# ExternalAPIDestination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | ID of the destination in your system | [readonly] 
**name** | **str** | Name of the destination | [readonly] 
**address** | **str** | Physical address of the destination | [readonly] 
**latitude** | **float** | Latitude coordinate of the destination&#39;s location (People also put X coordinate of Lambert-EST here) | [readonly] 
**longitude** | **float** | Longitude coordinate of the destination&#39;s location (People also put Y coordinate of Lambert-EST here) | [readonly] 
**owner_name** | **str** | Name of the destination&#39;s owner company | [readonly] 
**owner_reg_code** | **str** | Registration code of the destination&#39;s owner company | [readonly] 
**raw_data** | [**ExternalAPIDestinationRawData**](ExternalAPIDestinationRawData.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_destination import ExternalAPIDestination

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIDestination from a JSON string
external_api_destination_instance = ExternalAPIDestination.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIDestination.to_json())

# convert the object into a dict
external_api_destination_dict = external_api_destination_instance.to_dict()
# create an instance of ExternalAPIDestination from a dict
external_api_destination_from_dict = ExternalAPIDestination.from_dict(external_api_destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


