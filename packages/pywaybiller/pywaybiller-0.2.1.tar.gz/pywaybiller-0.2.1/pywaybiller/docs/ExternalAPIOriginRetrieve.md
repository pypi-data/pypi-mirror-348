# ExternalAPIOriginRetrieve


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique identifier of the origin | [readonly] 
**name** | **str** | Name of the origin | [readonly] 
**location** | [**ExternalAPIOriginLocation**](ExternalAPIOriginLocation.md) | Physical location of the origin | [readonly] 
**assortments** | [**List[ExternalAPIOriginAssortment]**](ExternalAPIOriginAssortment.md) | List of assortments available at the origin | [readonly] 
**partner_companies** | **List[str]** | List of registry codes of partner companies | [readonly] 
**public** | **bool** | Indicates whether the origin is visible to all companies or only to the owner company and authorized partners | [readonly] 
**active** | **bool** | Indicates whether the origin is currently active and available for use | [readonly] 
**holding_base** | [**ExternalAPIHoldingBase**](ExternalAPIHoldingBase.md) | Holding base data is provided as is, in internal WB format. It may change at any time without warning and may have a different schema for old and new origins | [readonly] 
**cadaster_number** | **str** | Cadaster number of the origin in free form. Required if holding base is sent | [readonly] 
**extra_information** | **str** | Additional information about the origin that doesn&#39;t fit in other fields | [readonly] 
**representative_name** | **str** | Name of the person representing this origin | [readonly] 
**representative_phone** | **str** | Contact phone number for the origin representative | [readonly] 
**waybill_created_emails** | **List[str]** | E-mail addresses where notifications will be sent when a waybill is created | [readonly] 
**waybill_accepted_emails** | **List[str]** | E-mail addresses where notifications will be sent when a waybill is accepted | [readonly] 
**waybill_reached_destination_emails** | **List[str]** | E-mail addresses where notifications will be sent when a waybill reaches its destination | [readonly] 
**transport_order_created_emails** | **List[str]** | E-mail addresses where notifications will be sent when a transport order is created | [readonly] 
**waybill_created_emails_language** | [**ExternalAPIOriginRetrieveWaybillCreatedEmailsLanguage**](ExternalAPIOriginRetrieveWaybillCreatedEmailsLanguage.md) |  | 
**waybill_accepted_emails_language** | [**ExternalAPIOriginRetrieveWaybillCreatedEmailsLanguage**](ExternalAPIOriginRetrieveWaybillCreatedEmailsLanguage.md) |  | 
**waybill_reached_destination_emails_language** | [**ExternalAPIOriginRetrieveWaybillCreatedEmailsLanguage**](ExternalAPIOriginRetrieveWaybillCreatedEmailsLanguage.md) |  | 
**transport_order_created_emails_language** | [**ExternalAPIOriginRetrieveWaybillCreatedEmailsLanguage**](ExternalAPIOriginRetrieveWaybillCreatedEmailsLanguage.md) |  | 
**feature_single_transport_order_per_truck** | **bool** | Managers are not allowed to create transport orders for a vehicle if there is an active transport order for the vehicle from this origin | [readonly] 
**feature_waybill_dispatched_amounts_changing_disabled** | **bool** | Drivers and receivers are not allowed to change dispatched amounts for waybills from this origin | [readonly] 
**feature_waybill_destination_changing_disabled_for_drivers** | **bool** | Drivers are not allowed to change the destination of waybills from this origin | [readonly] 
**company** | **str** | Registry code of the owner company | [readonly] 

## Example

```python
from openapi_client.models.external_api_origin_retrieve import ExternalAPIOriginRetrieve

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOriginRetrieve from a JSON string
external_api_origin_retrieve_instance = ExternalAPIOriginRetrieve.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOriginRetrieve.to_json())

# convert the object into a dict
external_api_origin_retrieve_dict = external_api_origin_retrieve_instance.to_dict()
# create an instance of ExternalAPIOriginRetrieve from a dict
external_api_origin_retrieve_from_dict = ExternalAPIOriginRetrieve.from_dict(external_api_origin_retrieve_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


