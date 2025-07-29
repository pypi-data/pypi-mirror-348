# ExternalAPIOrderTransportCompaniesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transportation_company_name** | **str** | Transportation company name. | [optional] 
**transportation_company_reg_code** | **str** | Transportation company reg code. | [optional] 

## Example

```python
from openapi_client.models.external_api_order_transport_companies_request import ExternalAPIOrderTransportCompaniesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderTransportCompaniesRequest from a JSON string
external_api_order_transport_companies_request_instance = ExternalAPIOrderTransportCompaniesRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderTransportCompaniesRequest.to_json())

# convert the object into a dict
external_api_order_transport_companies_request_dict = external_api_order_transport_companies_request_instance.to_dict()
# create an instance of ExternalAPIOrderTransportCompaniesRequest from a dict
external_api_order_transport_companies_request_from_dict = ExternalAPIOrderTransportCompaniesRequest.from_dict(external_api_order_transport_companies_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


