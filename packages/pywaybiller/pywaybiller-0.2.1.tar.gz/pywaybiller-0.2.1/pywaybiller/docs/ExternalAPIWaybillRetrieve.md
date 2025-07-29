# ExternalAPIWaybillRetrieve


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waybill_id** | **str** | The external ID of the waybill. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [readonly] 
**number** | **str** |  | [readonly] 
**status** | [**WaybillStatusEnum**](WaybillStatusEnum.md) |  | [readonly] 
**status_description** | **str** | Human readable status description (&#x60;Created&#x60;, &#x60;In progress&#x60;, &#x60;At destination&#x60;, &#x60;Confirmed&#x60; or &#x60;Cancelled&#x60;). | [readonly] 
**rows** | [**List[ExternalAPIWaybillRow]**](ExternalAPIWaybillRow.md) | Waybill rows. | 
**destination_raw_id** | **str** | The ID of the destination. | [optional] 
**destination_id** | **str** | The external ID of the destination. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [readonly] 
**destination_name** | **str** | The name of the destination. | [readonly] 
**destination_address** | **str** | The address of the destination. | [readonly] 
**destination_latitude** | **float** | The latitude of the destination. | [optional] 
**destination_longitude** | **float** | The longitude of the destination. | [optional] 
**destination_waybill_reached_destination_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill reaches destination. | [readonly] 
**destination_waybill_accepted_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill is accepted. | [readonly] 
**receiver_company_name** | **str** | The name of the receiving company. | [readonly] 
**receiver_company_reg_code** | **str** | The registry code of the receiving company. | [readonly] 
**origin_raw_id** | **str** | The ID of the origin. | [optional] 
**origin_id** | **int** | The external ID of the origin. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [optional] 
**origin_name** | **str** | The name of the origin. | [optional] 
**origin_address** | **str** | The address of the origin. | [optional] 
**origin_latitude** | **float** | The latitude of the origin. | [optional] 
**origin_longitude** | **float** | The longitude of the origin. | [optional] 
**origin_waybill_reached_destination_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill reaches destination. | [readonly] 
**origin_waybill_accepted_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill is accepted. | [readonly] 
**cadaster_number** | **str** | Cadaster number. | [readonly] 
**dispatcher_name** | **str** |  | [readonly] 
**dispatcher_phone** | **str** |  | [readonly] 
**holding_rights** | [**List[ExternalAPIWaybillHoldingRight]**](ExternalAPIWaybillHoldingRight.md) |  | [optional] 
**shipper_company_name** | **str** | The name of the shipper company. | [readonly] 
**shipper_company_reg_code** | **str** | The registry code of the shipper company. | [readonly] 
**transportation_company_name** | **str** | The name of the transportation company. | [readonly] 
**transportation_company_reg_code** | **str** | The registry code of the transportation company. | [readonly] 
**truck_reg_number** | **str** | The registration number of the vehicle. | 
**trailer_reg_number** | **str** | The registration number of the trailer. | [optional] 
**driver_email** | **str** | The e-mail address of the driver user. | [optional] 
**driver_name** | **str** | The name of the driver. | [readonly] 
**driver_phone** | **str** | The phone number of the driver. | [readonly] 
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
**evr_waybill_number** | **str** | EVR waybill number. | [readonly] 
**project** | **str** | Project code in your system. | [readonly] 
**transport_costs** | [**ExternalAPIWaybillTransportCosts**](ExternalAPIWaybillTransportCosts.md) | Information about transport costs | 
**raw_data** | [**ExternalAPIWaybillRawData**](ExternalAPIWaybillRawData.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_waybill_retrieve import ExternalAPIWaybillRetrieve

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillRetrieve from a JSON string
external_api_waybill_retrieve_instance = ExternalAPIWaybillRetrieve.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillRetrieve.to_json())

# convert the object into a dict
external_api_waybill_retrieve_dict = external_api_waybill_retrieve_instance.to_dict()
# create an instance of ExternalAPIWaybillRetrieve from a dict
external_api_waybill_retrieve_from_dict = ExternalAPIWaybillRetrieve.from_dict(external_api_waybill_retrieve_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


