# ExternalAPILoaderActionLogComment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**author_name** | **str** | Full name of the person who wrote the comment | [readonly] 
**author_company_name** | **str** | Company that the comment author represents | [readonly] 
**comment** | **str** | Full text content of the comment with no length restriction | [readonly] 
**created_timestamp** | **datetime** | Date and time when the comment was submitted (Format: &#x60;YYYY-MM-DDThh:mm:ss.ffffff+hh:mm&#x60;) | [readonly] 

## Example

```python
from openapi_client.models.external_api_loader_action_log_comment import ExternalAPILoaderActionLogComment

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPILoaderActionLogComment from a JSON string
external_api_loader_action_log_comment_instance = ExternalAPILoaderActionLogComment.from_json(json)
# print the JSON string representation of the object
print(ExternalAPILoaderActionLogComment.to_json())

# convert the object into a dict
external_api_loader_action_log_comment_dict = external_api_loader_action_log_comment_instance.to_dict()
# create an instance of ExternalAPILoaderActionLogComment from a dict
external_api_loader_action_log_comment_from_dict = ExternalAPILoaderActionLogComment.from_dict(external_api_loader_action_log_comment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


