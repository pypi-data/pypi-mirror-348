# ExternalAPIOriginUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the origin | [optional] 
**location** | [**ExternalAPIOriginLocationRequest**](ExternalAPIOriginLocationRequest.md) | Physical location of the origin | [optional] 
**assortments** | [**List[ExternalAPIOriginAssortmentRequest]**](ExternalAPIOriginAssortmentRequest.md) | List of assortments available at the origin | [optional] 
**partner_companies** | **List[str]** | List of registry codes of partner companies | [optional] 
**public** | **bool** | Indicates whether the origin is visible to all companies or only to the owner company and authorized partners | [optional] 
**active** | **bool** | Indicates whether the origin is currently active and available for use | [optional] 
**holding_base** | [**ExternalAPIHoldingBaseRequest**](ExternalAPIHoldingBaseRequest.md) | Holding base data is provided as is, in internal WB format. It may change at any time without warning and may have a different schema for old and new origins | [optional] 
**cadaster_number** | **str** | Cadaster number of the origin in free form. Required if holding base is sent | [optional] 
**extra_information** | **str** | Additional information about the origin that doesn&#39;t fit in other fields | [optional] 
**representative_name** | **str** | Name of the person representing this origin | [optional] 
**representative_phone** | **str** | Contact phone number for the origin representative | [optional] 
**waybill_created_emails** | **List[str]** | E-mail addresses where notifications will be sent when a waybill is created | [optional] 
**waybill_accepted_emails** | **List[str]** | E-mail addresses where notifications will be sent when a waybill is accepted | [optional] 
**waybill_reached_destination_emails** | **List[str]** | E-mail addresses where notifications will be sent when a waybill reaches its destination | [optional] 
**transport_order_created_emails** | **List[str]** | E-mail addresses where notifications will be sent when a transport order is created | [optional] 
**waybill_created_emails_language** | [**ExternalAPIOriginUpdateWaybillCreatedEmailsLanguage**](ExternalAPIOriginUpdateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**waybill_accepted_emails_language** | [**ExternalAPIOriginUpdateWaybillCreatedEmailsLanguage**](ExternalAPIOriginUpdateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**waybill_reached_destination_emails_language** | [**ExternalAPIOriginUpdateWaybillCreatedEmailsLanguage**](ExternalAPIOriginUpdateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**transport_order_created_emails_language** | [**ExternalAPIOriginUpdateWaybillCreatedEmailsLanguage**](ExternalAPIOriginUpdateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**feature_single_transport_order_per_truck** | **bool** | Managers are not allowed to create transport orders for a vehicle if there is an active transport order for the vehicle from this origin | [optional] 
**feature_waybill_dispatched_amounts_changing_disabled** | **bool** | Drivers and receivers are not allowed to change dispatched amounts for waybills from this origin | [optional] 
**feature_waybill_destination_changing_disabled_for_drivers** | **bool** | Drivers are not allowed to change the destination of waybills from this origin | [optional] 

## Example

```python
from openapi_client.models.external_api_origin_update_request import ExternalAPIOriginUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginUpdateRequest from a JSON string
external_api_origin_update_request_instance = ExternalAPIOriginUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginUpdateRequest.to_json())

# convert the object into a dict
external_api_origin_update_request_dict = external_api_origin_update_request_instance.to_dict()
# create an instance of ExternalAPIOriginUpdateRequest from a dict
external_api_origin_update_request_from_dict = ExternalAPIOriginUpdateRequest.from_dict(external_api_origin_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


