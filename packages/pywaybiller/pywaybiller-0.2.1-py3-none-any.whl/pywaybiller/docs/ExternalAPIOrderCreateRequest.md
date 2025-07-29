# ExternalAPIOrderCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | Order id (in your system). | 
**period** | **List[date]** | The date range when the order is active. | 
**client_id** | **str** | The company id (in your system) for whom the order is created for. | [optional] 
**client_company_reg_code** | **str** | The company reg code for whom the order is created for. Used as raw id to match the company, if it exists. | [optional] 
**client_company_name** | **str** | Name of the company for whom the order is created for. | [optional] 
**destination_raw_id** | **str** | Destination raw id. | [optional] 
**destination_id** | **int** | Destination id (in your system). | [optional] 
**destination_name** | **str** | Destination name. | [optional] 
**destination_address** | **str** | Destination address. | [optional] 
**destination_latitude** | **float** | Destination location - latitude. | [optional] 
**destination_longitude** | **float** | Destination location - longitude. | [optional] 
**origins** | [**List[ExternalAPIOrderOriginRequest]**](ExternalAPIOrderOriginRequest.md) | The origins for which the order is created for. | [optional] 
**total_allowed_amount** | **decimal.Decimal** | Total allowed amount. | [optional] 
**rows** | [**List[ExternalAPIOrderOriginsAssortmentsRequest]**](ExternalAPIOrderOriginsAssortmentsRequest.md) | Origin&#39;s assortments. | [optional] 
**transportation_companies** | [**List[ExternalAPIOrderTransportCompaniesRequest]**](ExternalAPIOrderTransportCompaniesRequest.md) | The transportation companies the client is using for transporting assortments from origins to destination. | [optional] 
**client_can_edit_transportation_values** | **bool** | Client can edit transportation values. | [optional] 
**vehicles** | [**List[ExternalAPIOrderVehiclesRequest]**](ExternalAPIOrderVehiclesRequest.md) | The vehicles that the transportation companies are allowed to use for this order. | [optional] 
**extra_information** | **str** | Extra information. | [optional] 
**user_id** | **int** | User who created this order. | 

## Example

```python
from openapi_client.models.external_api_order_create_request import ExternalAPIOrderCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderCreateRequest from a JSON string
external_api_order_create_request_instance = ExternalAPIOrderCreateRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderCreateRequest.to_json())

# convert the object into a dict
external_api_order_create_request_dict = external_api_order_create_request_instance.to_dict()
# create an instance of ExternalAPIOrderCreateRequest from a dict
external_api_order_create_request_from_dict = ExternalAPIOrderCreateRequest.from_dict(external_api_order_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


