# ExternalAPILoaderActionLogRawData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**log_id** | **int** | Unique identifier of the loader action log | [readonly] 
**loader_operator_user_id** | **int** | Unique identifier of the user operating the loader | [readonly] 
**origin_id** | **int** | Unique identifier of the origin where the action was performed | [readonly] 
**order_id** | **int** | Unique identifier of the associated order, if applicable | [readonly] 
**vehicle_id** | **int** | Unique identifier of the vehicle involved in the action, if applicable | [readonly] 
**loader_unit_id** | **int** | Unique identifier of the used loader unit | [readonly] 
**assortment_id** | **int** | Unique identifier of the loaded assortment, if applicable | [readonly] 
**subset_id** | **int** | Unique identifier of the assortment subset, if applicable | [readonly] 

## Example

```python
from openapi_client.models.external_api_loader_action_log_raw_data import ExternalAPILoaderActionLogRawData

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPILoaderActionLogRawData from a JSON string
external_api_loader_action_log_raw_data_instance = ExternalAPILoaderActionLogRawData.from_json(json)
# print the JSON string representation of the object
print(ExternalAPILoaderActionLogRawData.to_json())

# convert the object into a dict
external_api_loader_action_log_raw_data_dict = external_api_loader_action_log_raw_data_instance.to_dict()
# create an instance of ExternalAPILoaderActionLogRawData from a dict
external_api_loader_action_log_raw_data_from_dict = ExternalAPILoaderActionLogRawData.from_dict(external_api_loader_action_log_raw_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


