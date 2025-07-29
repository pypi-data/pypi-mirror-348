# ExternalAPIOrderUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**period** | **List[date]** | The date range when the order is active. | [optional] 
**client_id** | **str** | The company id (in your system) for whom the order is created for. | [optional] 
**client_company_reg_code** | **str** | The company reg code for whom the order is created for. Used as raw id to match the company, if it exists. | [optional] 
**client_company_name** | **str** | Name of the company for whom the order is created for. | [optional] 
**destination_raw_id** | **str** | Destination raw id. | [optional] 
**destination_id** | **int** | Destination id (in your system). | [optional] 
**destination_name** | **str** | Destination name. | [optional] 
**destination_address** | **str** | Destination address. | [optional] 
**destination_latitude** | **float** | Destination location - latitude. | [optional] 
**destination_longitude** | **float** | Destination location - longitude. | [optional] 
**origins** | [**List[ExternalAPIOrderOrigin]**](ExternalAPIOrderOrigin.md) | The origins for which the order is created for. | [optional] 
**rows** | [**List[ExternalAPIOrderOriginsAssortments]**](ExternalAPIOrderOriginsAssortments.md) | Origin&#39;s assortments. | [optional] 
**total_allowed_amount** | **decimal.Decimal** | Total allowed amount. | [optional] 
**transportation_companies** | [**List[ExternalAPIOrderTransportCompanies]**](ExternalAPIOrderTransportCompanies.md) | The transportation companies the client is using for transporting assortments from origins to destination. | [optional] 
**vehicles** | [**List[ExternalAPIOrderVehicles]**](ExternalAPIOrderVehicles.md) | The vehicles that the transportation companies are allowed to use for this order. | [optional] 
**client_can_edit_transportation_values** | **bool** | Client can edit transportation values. | [optional] 
**cancel_transport_orders_on_allowed_amount_exceeding** | **bool** | Cancel transport orders and do not allow to create new transport orders if the order amount has been exceeded. | [optional] 
**extra_information** | **str** | Extra information. | [optional] 

## Example

```python
from openapi_client.models.external_api_order_update import ExternalAPIOrderUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderUpdate from a JSON string
external_api_order_update_instance = ExternalAPIOrderUpdate.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderUpdate.to_json())

# convert the object into a dict
external_api_order_update_dict = external_api_order_update_instance.to_dict()
# create an instance of ExternalAPIOrderUpdate from a dict
external_api_order_update_from_dict = ExternalAPIOrderUpdate.from_dict(external_api_order_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


