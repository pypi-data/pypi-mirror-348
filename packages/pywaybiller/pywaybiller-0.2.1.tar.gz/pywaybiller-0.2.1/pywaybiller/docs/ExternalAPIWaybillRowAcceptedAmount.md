# ExternalAPIWaybillRowAcceptedAmount


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assortment_id** | **int** | The ID of the dispatched assortment (eg 1). Use Querying of a single waybill endpoint to see the available assortments inside rows field using the assortment_raw_id value. | 
**assortment_ids** | **List[str]** | The external IDs of the assortment. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [readonly] 
**accepted_assortment_id** | **int** | The ID of the accepted assortment (eg 1). Use Querying of a single waybill endpoint to see the available assortments inside rows field using the assortment_raw_id value. | [optional] 
**accepted_gross_weight** | **decimal.Decimal** | The accepted gross weight in tonnes. | [optional] 
**accepted_gross_weight_timestamp** | **datetime** | The timestamp of the accepted gross weight. | [optional] 
**accepted_tare_weight** | **decimal.Decimal** | The accepted tare weight in tonnes. | [optional] 
**accepted_tare_weight_timestamp** | **datetime** | The timestamp of the accepted tare weight. | [optional] 
**accepted_amount** | **decimal.Decimal** | The accepted amount in the unit that is attached to the assortment. | [optional] 

## Example

```python
from openapi_client.models.external_api_waybill_row_accepted_amount import ExternalAPIWaybillRowAcceptedAmount

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillRowAcceptedAmount from a JSON string
external_api_waybill_row_accepted_amount_instance = ExternalAPIWaybillRowAcceptedAmount.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillRowAcceptedAmount.to_json())

# convert the object into a dict
external_api_waybill_row_accepted_amount_dict = external_api_waybill_row_accepted_amount_instance.to_dict()
# create an instance of ExternalAPIWaybillRowAcceptedAmount from a dict
external_api_waybill_row_accepted_amount_from_dict = ExternalAPIWaybillRowAcceptedAmount.from_dict(external_api_waybill_row_accepted_amount_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


