# ExternalAPIWaybillCommentRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comment_by_user_id** | **int** | The ID of the user that adds the comment to the waybill. Use GET Employments endpoint to query all available employments and get necessary &#x60;user_id&#x60; values. | 
**comment** | **str** | Text of the comment. | 

## Example

```python
from openapi_client.models.external_api_waybill_comment_request import ExternalAPIWaybillCommentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillCommentRequest from a JSON string
external_api_waybill_comment_request_instance = ExternalAPIWaybillCommentRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillCommentRequest.to_json())

# convert the object into a dict
external_api_waybill_comment_request_dict = external_api_waybill_comment_request_instance.to_dict()
# create an instance of ExternalAPIWaybillCommentRequest from a dict
external_api_waybill_comment_request_from_dict = ExternalAPIWaybillCommentRequest.from_dict(external_api_waybill_comment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


