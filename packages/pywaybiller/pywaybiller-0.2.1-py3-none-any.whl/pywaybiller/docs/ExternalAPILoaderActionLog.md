# ExternalAPILoaderActionLog


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**log_timestamp** | **datetime** | Exact date and time when the loading action was recorded (Format: &#x60;YYYY-MM-DDThh:mm:ss.ffffff+hh:mm&#x60;) | [readonly] 
**log_description** | **str** | Detailed description of the loading action and its associated context | [readonly] 
**loader_operator_user_name** | **str** | The full name of the loader operator | [readonly] 
**action_name** | **str** | Name of the loader action that was performed | [readonly] 
**origin_name** | **str** | Name of the origin where the loading action was performed | [readonly] 
**order_number** | **str** | Number of the order associated with the action, if applicable | [readonly] 
**vehicle_reg_number** | **str** | Registration number of the vehicle associated with the action, if applicable | [readonly] 
**trailer_reg_number** | **str** | Registration number of the attached trailer, if applicable | [readonly] 
**waybill_number** | **str** | Number of the waybill associated with the action, if applicable | [readonly] 
**loader_unit_name** | **str** | Identification or name of the loading equipment that was used | [readonly] 
**assortment_name** | **str** | Name of the assortment associated with the action | [readonly] 
**subset_name** | **str** | Name of the subset associated with the action | [readonly] 
**weight** | **str** | Weight that was loaded or unloaded (e.g., &#x60;\&quot;12.345\&quot;&#x60;) | [readonly] 
**log_comments** | [**List[ExternalAPILoaderActionLogComment]**](ExternalAPILoaderActionLogComment.md) | List of all comments added to this action | [readonly] 
**raw_data** | [**ExternalAPILoaderActionLogRawData**](ExternalAPILoaderActionLogRawData.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_loader_action_log import ExternalAPILoaderActionLog

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPILoaderActionLog from a JSON string
external_api_loader_action_log_instance = ExternalAPILoaderActionLog.from_json(json)
# print the JSON string representation of the object
print(ExternalAPILoaderActionLog.to_json())

# convert the object into a dict
external_api_loader_action_log_dict = external_api_loader_action_log_instance.to_dict()
# create an instance of ExternalAPILoaderActionLog from a dict
external_api_loader_action_log_from_dict = ExternalAPILoaderActionLog.from_dict(external_api_loader_action_log_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


