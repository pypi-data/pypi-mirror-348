# PaginatedExternalAPIWaybillListList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Total number of objects matching the provided query | 
**next** | **str** | URL to the next page of results, or null if there are no additional pages | 
**previous** | **str** | URL to the previous page of results, or null if it&#39;s the first page | 
**results** | [**List[ExternalAPIWaybillList]**](ExternalAPIWaybillList.md) |  | 

## Example

```python
from openapi_client.models.paginated_external_api_waybill_list_list import PaginatedExternalAPIWaybillListList

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedExternalAPIWaybillListList from a JSON string
paginated_external_api_waybill_list_list_instance = PaginatedExternalAPIWaybillListList.from_json(json)
# print the JSON string representation of the object
print(PaginatedExternalAPIWaybillListList.to_json())

# convert the object into a dict
paginated_external_api_waybill_list_list_dict = paginated_external_api_waybill_list_list_instance.to_dict()
# create an instance of PaginatedExternalAPIWaybillListList from a dict
paginated_external_api_waybill_list_list_from_dict = PaginatedExternalAPIWaybillListList.from_dict(paginated_external_api_waybill_list_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


