# ExternalAPIOrderOriginRequest


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
from openapi_client.models.external_api_order_origin_request import ExternalAPIOrderOriginRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderOriginRequest from a JSON string
external_api_order_origin_request_instance = ExternalAPIOrderOriginRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderOriginRequest.to_json())

# convert the object into a dict
external_api_order_origin_request_dict = external_api_order_origin_request_instance.to_dict()
# create an instance of ExternalAPIOrderOriginRequest from a dict
external_api_order_origin_request_from_dict = ExternalAPIOrderOriginRequest.from_dict(external_api_order_origin_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


