# ExternalAPITransportOrder


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_order_id** | **str** |  | 
**order_raw_id** | **str** |  | [optional] 
**order_id** | **str** |  | [optional] 
**number** | **str** |  | [readonly] 
**status** | [**TransportOrderStatusEnum**](TransportOrderStatusEnum.md) |  | [readonly] 
**rows** | [**List[ExternalAPITransportOrderRow]**](ExternalAPITransportOrderRow.md) |  | 
**organizer_user_id** | **int** |  | 
**destination_raw_id** | **str** |  | [optional] 
**destination_id** | **int** |  | [optional] 
**destination_name** | **str** |  | [optional] 
**destination_address** | **str** |  | [optional] 
**destination_latitude** | **float** |  | [optional] 
**destination_longitude** | **float** |  | [optional] 
**destination_waybill_created_emails** | **List[str]** |  | [optional] 
**destination_waybill_reached_destination_emails** | **List[str]** |  | [optional] 
**destination_waybill_accepted_emails** | **List[str]** |  | [optional] 
**destination_transport_order_created_emails** | **List[str]** |  | [optional] 
**receiver_company_name** | **str** |  | [optional] 
**receiver_company_reg_code** | **str** |  | [optional] 
**origin_raw_id** | **str** |  | [optional] 
**origin_id** | **int** |  | [optional] 
**origin_name** | **str** |  | [optional] 
**origin_address** | **str** |  | [optional] 
**origin_latitude** | **float** |  | [optional] 
**origin_longitude** | **float** |  | [optional] 
**origin_waybill_created_emails** | **List[str]** |  | [optional] 
**origin_waybill_reached_destination_emails** | **List[str]** |  | [optional] 
**origin_waybill_accepted_emails** | **List[str]** |  | [optional] 
**origin_transport_order_created_emails** | **List[str]** |  | [optional] 
**shipper_company_name** | **str** |  | [optional] 
**shipper_company_reg_code** | **str** |  | [optional] 
**transportation_company_name** | **str** |  | [optional] 
**transportation_company_reg_code** | **str** |  | [optional] 
**truck_reg_number** | **str** |  | [optional] 
**trailer_reg_number** | **str** |  | [optional] 
**driver_email** | **str** |  | [optional] 
**driver_personal_code** | **str** |  | [optional] 
**driver_name** | **str** |  | [optional] 
**driver_phone** | **str** |  | [optional] [default to '']
**transport_date** | **date** |  | 
**transport_time** | **str** |  | [optional] 
**additional_info** | **str** |  | [optional] 
**waybills_ids** | **List[int]** |  | [readonly] 
**waybill_pdf_urls** | **List[str]** |  | [readonly] 
**raw_data** | [**ExternalAPITransportOrderRawData**](ExternalAPITransportOrderRawData.md) | The IDs of the Waybiller internal objects | [readonly] 
**pallets_number** | **int** |  | [optional] 

## Example

```python
from openapi_client.models.external_api_transport_order import ExternalAPITransportOrder

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrder from a JSON string
external_api_transport_order_instance = ExternalAPITransportOrder.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrder.to_json())

# convert the object into a dict
external_api_transport_order_dict = external_api_transport_order_instance.to_dict()
# create an instance of ExternalAPITransportOrder from a dict
external_api_transport_order_from_dict = ExternalAPITransportOrder.from_dict(external_api_transport_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


