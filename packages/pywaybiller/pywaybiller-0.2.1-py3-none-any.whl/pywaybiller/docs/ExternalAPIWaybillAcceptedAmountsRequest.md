# ExternalAPIWaybillAcceptedAmountsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accepted_amounts** | [**List[ExternalAPIWaybillRowAcceptedAmountRequest]**](ExternalAPIWaybillRowAcceptedAmountRequest.md) | Accepted amounts | 

## Example

```python
from openapi_client.models.external_api_waybill_accepted_amounts_request import ExternalAPIWaybillAcceptedAmountsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillAcceptedAmountsRequest from a JSON string
external_api_waybill_accepted_amounts_request_instance = ExternalAPIWaybillAcceptedAmountsRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillAcceptedAmountsRequest.to_json())

# convert the object into a dict
external_api_waybill_accepted_amounts_request_dict = external_api_waybill_accepted_amounts_request_instance.to_dict()
# create an instance of ExternalAPIWaybillAcceptedAmountsRequest from a dict
external_api_waybill_accepted_amounts_request_from_dict = ExternalAPIWaybillAcceptedAmountsRequest.from_dict(external_api_waybill_accepted_amounts_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


