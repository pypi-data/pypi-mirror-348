# ExternalAPIOrderTransportCompanies


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transportation_company_name** | **str** | Transportation company name. | [optional] 
**transportation_company_reg_code** | **str** | Transportation company reg code. | [optional] 

## Example

```python
from openapi_client.models.external_api_order_transport_companies import ExternalAPIOrderTransportCompanies

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderTransportCompanies from a JSON string
external_api_order_transport_companies_instance = ExternalAPIOrderTransportCompanies.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderTransportCompanies.to_json())

# convert the object into a dict
external_api_order_transport_companies_dict = external_api_order_transport_companies_instance.to_dict()
# create an instance of ExternalAPIOrderTransportCompanies from a dict
external_api_order_transport_companies_from_dict = ExternalAPIOrderTransportCompanies.from_dict(external_api_order_transport_companies_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


