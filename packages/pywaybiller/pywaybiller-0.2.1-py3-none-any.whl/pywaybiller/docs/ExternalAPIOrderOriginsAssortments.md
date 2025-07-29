# ExternalAPIOrderOriginsAssortments


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**origin_assortment_raw_id** | **str** | Origin assortment raw id. | [optional] 
**assortment_name** | **str** | Origin assortment name with subset value (if exists). | [readonly] 

## Example

```python
from openapi_client.models.external_api_order_origins_assortments import ExternalAPIOrderOriginsAssortments

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderOriginsAssortments from a JSON string
external_api_order_origins_assortments_instance = ExternalAPIOrderOriginsAssortments.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderOriginsAssortments.to_json())

# convert the object into a dict
external_api_order_origins_assortments_dict = external_api_order_origins_assortments_instance.to_dict()
# create an instance of ExternalAPIOrderOriginsAssortments from a dict
external_api_order_origins_assortments_from_dict = ExternalAPIOrderOriginsAssortments.from_dict(external_api_order_origins_assortments_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


