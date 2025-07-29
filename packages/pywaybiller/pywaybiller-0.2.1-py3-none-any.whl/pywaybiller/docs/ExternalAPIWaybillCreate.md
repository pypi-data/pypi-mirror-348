# ExternalAPIWaybillCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waybill_id** | **str** | The external ID of the waybill. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | 
**number** | **str** |  | [readonly] 
**status** | [**WaybillStatusEnum**](WaybillStatusEnum.md) |  | [readonly] 
**status_description** | **str** | Human readable status description (&#x60;Created&#x60;, &#x60;In progress&#x60;, &#x60;At destination&#x60;, &#x60;Confirmed&#x60; or &#x60;Cancelled&#x60;). | [readonly] 
**rows** | [**List[ExternalAPIWaybillRow]**](ExternalAPIWaybillRow.md) | Waybill rows. | 
**destination_raw_id** | **str** | The ID of the destination. | [optional] 
**destination_id** | **int** | The external ID of the destination. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [optional] 
**destination_name** | **str** | The name of the destination. | [optional] 
**destination_address** | **str** | The address of the destination. | [optional] 
**destination_latitude** | **float** | The latitude of the destination. | [optional] 
**destination_longitude** | **float** | The longitude of the destination. | [optional] 
**destination_waybill_reached_destination_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill reaches destination. | [optional] 
**destination_waybill_accepted_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill is accepted. | [optional] 
**receiver_company_name** | **str** | The name of the receiving company. | [readonly] 
**receiver_company_reg_code** | **str** | The registry code of the receiving company. | [readonly] 
**origin_raw_id** | **str** | The ID of the origin. | [optional] 
**origin_id** | **int** | The external ID of the origin. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [optional] 
**origin_name** | **str** | The name of the origin. | [optional] 
**origin_address** | **str** | The address of the origin. | [optional] 
**origin_latitude** | **float** | The latitude of the origin. | [optional] 
**origin_longitude** | **float** | The longitude of the origin. | [optional] 
**origin_waybill_reached_destination_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill reaches destination. | [optional] 
**origin_waybill_accepted_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill is accepted. | [optional] 
**cadaster_number** | **str** | Cadaster number. Field is deprecated, please use &#x60;holding_rights&#x60; instead. | [optional] 
**dispatcher_name** | **str** |  | [optional] 
**dispatcher_phone** | **str** |  | [optional] 
**holding_rights** | [**List[ExternalAPIWaybillHoldingRight]**](ExternalAPIWaybillHoldingRight.md) |  | [optional] 
**shipper_company_name** | **str** | The name of the shipper company. | [optional] 
**shipper_company_reg_code** | **str** | The registry code of the shipper company. | [optional] 
**transportation_company_name** | **str** | The name of the transportation company. | 
**transportation_company_reg_code** | **str** | The registry code of the transportation company. | 
**truck_reg_number** | **str** | The registration number of the vehicle. | 
**trailer_reg_number** | **str** | The registration number of the trailer. | [optional] 
**driver_email** | **str** | The e-mail address of the driver user. | [optional] 
**driver_name** | **str** | The name of the driver. | [optional] 
**driver_phone** | **str** | The phone number of the driver. | [optional] 
**driver_personal_code** | **str** | The personal code of the driver. | [optional] 
**mileage** | **int** | The mileage can be calculated using a map or can be taken from Distance object if exist | [readonly] 
**mileage_by_driver** | **int** |  | [readonly] 
**confirmed_by_email** | **str** | The e-mail address of the user that accepted the waybill. | [optional] 
**confirmed_by_name** | **str** |  | [readonly] 
**confirmed_by_phone** | **str** |  | [readonly] 
**cancelled_by_email** | **str** | The e-mail address of the user that cancelled the waybill. | [optional] 
**cancelled_by_name** | **str** |  | [readonly] 
**cancelled_by_phone** | **str** |  | [readonly] 
**cancelling_reason** | **str** |  | [readonly] 
**dispatcher_timestamp** | **datetime** | Waybill creation timestamp | [readonly] 
**driver_timestamp** | **datetime** | Timestamp when driver started driving | [readonly] 
**destination_timestamp** | **datetime** | Time when waybill reached destination. | [readonly] 
**confirmed_timestamp** | **datetime** | Time of confirmation in the destination | [readonly] 
**cancelled_timestamp** | **datetime** | Time of waybill cancelling | [readonly] 
**pdf_url** | **str** |  | [readonly] 
**navision_bin_code** | **str** | Bin code. | [readonly] 
**evr_waybill_number** | **str** | EVR waybill number. | [optional] 
**raw_data** | [**ExternalAPIWaybillRawData**](ExternalAPIWaybillRawData.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_waybill_create import ExternalAPIWaybillCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillCreate from a JSON string
external_api_waybill_create_instance = ExternalAPIWaybillCreate.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillCreate.to_json())

# convert the object into a dict
external_api_waybill_create_dict = external_api_waybill_create_instance.to_dict()
# create an instance of ExternalAPIWaybillCreate from a dict
external_api_waybill_create_from_dict = ExternalAPIWaybillCreate.from_dict(external_api_waybill_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


