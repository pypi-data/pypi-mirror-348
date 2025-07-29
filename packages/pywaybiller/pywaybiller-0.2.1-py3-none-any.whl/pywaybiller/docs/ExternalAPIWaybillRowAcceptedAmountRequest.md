# ExternalAPIWaybillRowAcceptedAmountRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assortment_id** | **int** | The ID of the dispatched assortment (eg 1). Use Querying of a single waybill endpoint to see the available assortments inside rows field using the assortment_raw_id value. | 
**accepted_assortment_id** | **int** | The ID of the accepted assortment (eg 1). Use Querying of a single waybill endpoint to see the available assortments inside rows field using the assortment_raw_id value. | [optional] 
**accepted_gross_weight** | **decimal.Decimal** | The accepted gross weight in tonnes. | [optional] 
**accepted_gross_weight_timestamp** | **datetime** | The timestamp of the accepted gross weight. | [optional] 
**accepted_tare_weight** | **decimal.Decimal** | The accepted tare weight in tonnes. | [optional] 
**accepted_tare_weight_timestamp** | **datetime** | The timestamp of the accepted tare weight. | [optional] 
**accepted_amount** | **decimal.Decimal** | The accepted amount in the unit that is attached to the assortment. | [optional] 

## Example

```python
from openapi_client.models.external_api_waybill_row_accepted_amount_request import ExternalAPIWaybillRowAcceptedAmountRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillRowAcceptedAmountRequest from a JSON string
external_api_waybill_row_accepted_amount_request_instance = ExternalAPIWaybillRowAcceptedAmountRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillRowAcceptedAmountRequest.to_json())

# convert the object into a dict
external_api_waybill_row_accepted_amount_request_dict = external_api_waybill_row_accepted_amount_request_instance.to_dict()
# create an instance of ExternalAPIWaybillRowAcceptedAmountRequest from a dict
external_api_waybill_row_accepted_amount_request_from_dict = ExternalAPIWaybillRowAcceptedAmountRequest.from_dict(external_api_waybill_row_accepted_amount_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


