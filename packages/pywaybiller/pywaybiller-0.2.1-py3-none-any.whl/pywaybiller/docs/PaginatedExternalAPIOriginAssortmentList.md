# PaginatedExternalAPIOriginAssortmentList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Total number of objects matching the provided query | 
**next** | **str** | URL to the next page of results, or null if there are no additional pages | 
**previous** | **str** | URL to the previous page of results, or null if it&#39;s the first page | 
**results** | [**List[ExternalAPIOriginAssortment]**](ExternalAPIOriginAssortment.md) |  | 

## Example

```python
from openapi_client.models.paginated_external_api_origin_assortment_list import PaginatedExternalAPIOriginAssortmentList

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedExternalAPIOriginAssortmentList from a JSON string
paginated_external_api_origin_assortment_list_instance = PaginatedExternalAPIOriginAssortmentList.from_json(json)
# print the JSON string representation of the object
print(PaginatedExternalAPIOriginAssortmentList.to_json())

# convert the object into a dict
paginated_external_api_origin_assortment_list_dict = paginated_external_api_origin_assortment_list_instance.to_dict()
# create an instance of PaginatedExternalAPIOriginAssortmentList from a dict
paginated_external_api_origin_assortment_list_from_dict = PaginatedExternalAPIOriginAssortmentList.from_dict(paginated_external_api_origin_assortment_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


