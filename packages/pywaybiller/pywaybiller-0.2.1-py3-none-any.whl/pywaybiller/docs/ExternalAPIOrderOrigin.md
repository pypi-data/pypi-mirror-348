# ExternalAPIOrderOrigin


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**origin_raw_id** | **str** | Origin raw id. | [optional] 
**origin_name** | **str** | Origin name. | [optional] 
**origin_address** | **str** | Origin address. | [optional] 
**origin_latitude** | **float** | Origin location - latitude. | [optional] 
**origin_longitude** | **float** | Origin location - longitude. | [optional] 
**shipper_company_name** | **str** | Origin company name. | [optional] 
**shipper_company_reg_code** | **str** | Origin company reg code. | [optional] 

## Example

```python
from openapi_client.models.external_api_order_origin import ExternalAPIOrderOrigin

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderOrigin from a JSON string
external_api_order_origin_instance = ExternalAPIOrderOrigin.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderOrigin.to_json())

# convert the object into a dict
external_api_order_origin_dict = external_api_order_origin_instance.to_dict()
# create an instance of ExternalAPIOrderOrigin from a dict
external_api_order_origin_from_dict = ExternalAPIOrderOrigin.from_dict(external_api_order_origin_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


