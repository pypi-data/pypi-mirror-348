# ExternalAPITransportOrderRow


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assortment_id** | **int** |  | 
**assortment_name** | **str** |  | [optional] 
**amount** | **decimal.Decimal** |  | 

## Example

```python
from openapi_client.models.external_api_transport_order_row import ExternalAPITransportOrderRow

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderRow from a JSON string
external_api_transport_order_row_instance = ExternalAPITransportOrderRow.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderRow.to_json())

# convert the object into a dict
external_api_transport_order_row_dict = external_api_transport_order_row_instance.to_dict()
# create an instance of ExternalAPITransportOrderRow from a dict
external_api_transport_order_row_from_dict = ExternalAPITransportOrderRow.from_dict(external_api_transport_order_row_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


