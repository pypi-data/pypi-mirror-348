# ExternalAPIOriginCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the origin | 
**location** | [**ExternalAPIOriginLocationRequest**](ExternalAPIOriginLocationRequest.md) | Physical location of the origin | 
**assortments** | [**List[ExternalAPIOriginAssortmentRequest]**](ExternalAPIOriginAssortmentRequest.md) | List of assortments available at the origin | 
**partner_companies** | **List[str]** | List of registry codes of partner companies | [optional] 
**public** | **bool** | Indicates whether the origin is visible to all companies or only to the owner company and authorized partners | [optional] [default to False]
**active** | **bool** | Indicates whether the origin is currently active and available for use | [optional] [default to True]
**holding_base** | [**ExternalAPIHoldingBaseRequest**](ExternalAPIHoldingBaseRequest.md) | Holding base data is provided as is, in internal WB format. It may change at any time without warning and may have a different schema for old and new origins | [optional] 
**cadaster_number** | **str** | Cadaster number of the origin in free form. Required if holding base is sent | [optional] 
**extra_information** | **str** | Additional information about the origin that doesn&#39;t fit in other fields | [optional] 
**representative_name** | **str** | Name of the person representing this origin | [optional] 
**representative_phone** | **str** | Contact phone number for the origin representative | [optional] 
**waybill_created_emails** | **List[str]** | E-mail addresses where notifications will be sent when a waybill is created | [optional] 
**waybill_accepted_emails** | **List[str]** | E-mail addresses where notifications will be sent when a waybill is accepted | [optional] 
**waybill_reached_destination_emails** | **List[str]** | E-mail addresses where notifications will be sent when a waybill reaches its destination | [optional] 
**transport_order_created_emails** | **List[str]** | E-mail addresses where notifications will be sent when a transport order is created | [optional] 
**waybill_created_emails_language** | [**ExternalAPIOriginCreateWaybillCreatedEmailsLanguage**](ExternalAPIOriginCreateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**waybill_accepted_emails_language** | [**ExternalAPIOriginCreateWaybillCreatedEmailsLanguage**](ExternalAPIOriginCreateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**waybill_reached_destination_emails_language** | [**ExternalAPIOriginCreateWaybillCreatedEmailsLanguage**](ExternalAPIOriginCreateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**transport_order_created_emails_language** | [**ExternalAPIOriginCreateWaybillCreatedEmailsLanguage**](ExternalAPIOriginCreateWaybillCreatedEmailsLanguage.md) |  | [optional] 
**feature_single_transport_order_per_truck** | **bool** | Managers are not allowed to create transport orders for a vehicle if there is an active transport order for the vehicle from this origin | [optional] [default to False]
**feature_waybill_dispatched_amounts_changing_disabled** | **bool** | Drivers and receivers are not allowed to change dispatched amounts for waybills from this origin | [optional] [default to False]
**feature_waybill_destination_changing_disabled_for_drivers** | **bool** | Drivers are not allowed to change the destination of waybills from this origin | [optional] [default to False]
**company** | **str** | Registry code of the owner company. By default, API KEY company is used. Note, origin company can not be changed | [optional] 

## Example

```python
from openapi_client.models.external_api_origin_create_request import ExternalAPIOriginCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginCreateRequest from a JSON string
external_api_origin_create_request_instance = ExternalAPIOriginCreateRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginCreateRequest.to_json())

# convert the object into a dict
external_api_origin_create_request_dict = external_api_origin_create_request_instance.to_dict()
# create an instance of ExternalAPIOriginCreateRequest from a dict
external_api_origin_create_request_from_dict = ExternalAPIOriginCreateRequest.from_dict(external_api_origin_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


