# ExternalAPIWaybillCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waybill_id** | **str** | The external ID of the waybill. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | 
**rows** | [**List[ExternalAPIWaybillRowRequest]**](ExternalAPIWaybillRowRequest.md) | Waybill rows. | 
**destination_raw_id** | **str** | The ID of the destination. | [optional] 
**destination_id** | **int** | The external ID of the destination. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [optional] 
**destination_name** | **str** | The name of the destination. | [optional] 
**destination_address** | **str** | The address of the destination. | [optional] 
**destination_latitude** | **float** | The latitude of the destination. | [optional] 
**destination_longitude** | **float** | The longitude of the destination. | [optional] 
**destination_company_name** | **str** | The name of the receiving company. Usually the owner company of the destination. | [optional] 
**destination_company_reg_code** | **str** | The registry code of the receiving company. Usually the owner company of the destination. | [optional] 
**destination_waybill_reached_destination_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill reaches destination. | [optional] 
**destination_waybill_accepted_emails** | **List[str]** | Comma separated list of e-mail addresses to whom send an e-mail when waybill is accepted. | [optional] 
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
**holding_rights** | [**List[ExternalAPIWaybillHoldingRightRequest]**](ExternalAPIWaybillHoldingRightRequest.md) |  | [optional] 
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
**confirmed_by_email** | **str** | The e-mail address of the user that accepted the waybill. | [optional] 
**cancelled_by_email** | **str** | The e-mail address of the user that cancelled the waybill. | [optional] 
**evr_waybill_number** | **str** | EVR waybill number. | [optional] 

## Example

```python
from openapi_client.models.external_api_waybill_create_request import ExternalAPIWaybillCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillCreateRequest from a JSON string
external_api_waybill_create_request_instance = ExternalAPIWaybillCreateRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillCreateRequest.to_json())

# convert the object into a dict
external_api_waybill_create_request_dict = external_api_waybill_create_request_instance.to_dict()
# create an instance of ExternalAPIWaybillCreateRequest from a dict
external_api_waybill_create_request_from_dict = ExternalAPIWaybillCreateRequest.from_dict(external_api_waybill_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


