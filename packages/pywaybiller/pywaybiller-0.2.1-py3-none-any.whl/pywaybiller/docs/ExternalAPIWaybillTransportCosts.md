# ExternalAPIWaybillTransportCosts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**incoterm** | [**IncotermEnum**](IncotermEnum.md) | The incoterm for which the transport cost is calculated.  * &#x60;EXW&#x60; - EXW (Ex Works) * &#x60;DAP&#x60; - DAP (Delivered At Place) | [readonly] 
**pricing_system** | [**ExternalAPIWaybillTransportCostsPricingSystem**](ExternalAPIWaybillTransportCostsPricingSystem.md) |  | 
**load_price** | **decimal.Decimal** | The price used to calculate the transport cost for load pricing system. | [readonly] 
**transport_coefficient** | **decimal.Decimal** | The transport coefficient used to calculate the transport cost. | [readonly] 
**minimum_unit_price** | **decimal.Decimal** | The minimum unit price used to calculate the transport cost. | [readonly] 
**weights_to_use** | [**ExternalAPIWaybillTransportCostsWeightsToUse**](ExternalAPIWaybillTransportCostsWeightsToUse.md) |  | 
**tonnes** | **decimal.Decimal** | Amount in tonnes to be used to calculate the transport cost. | [readonly] 
**ton_price** | **decimal.Decimal** | The price used to calculate the transport cost for ton pricing system. | [readonly] 
**mileage_price** | **decimal.Decimal** | The price used to calculate the transport cost for mileage pricing system. | [readonly] 
**mileage** | **int** | The distance in kilometers used to calculate the transport cost. | [readonly] 
**waiting_hours** | **decimal.Decimal** | The number of hours the driver waited. | [readonly] 
**waiting_hours_price** | **decimal.Decimal** | The cost of waiting for one hour. | [readonly] 
**extra_costs** | **decimal.Decimal** | Extra costs for the transport. | [readonly] 
**transport_cost_value** | **decimal.Decimal** | The calculated transport cost value. | [readonly] 
**transport_cost_calculation** | **str** | The calculation of the transport cost. | [readonly] 
**last_saved_by_email** | **str** | The e-mail address of the user that last saved the transport costs. If confirmation time is set, then this user confirmed the costs | [readonly] 
**last_saved_by_name** | **str** | The name of the user that last saved the transport costs | [readonly] 
**last_saved_by_company_name** | **str** | The company name of the user that last saved the transport costs | [readonly] 
**confirmed_at** | **datetime** | The time when the transport cost was confirmed. | [readonly] 

## Example

```python
from openapi_client.models.external_api_waybill_transport_costs import ExternalAPIWaybillTransportCosts

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillTransportCosts from a JSON string
external_api_waybill_transport_costs_instance = ExternalAPIWaybillTransportCosts.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillTransportCosts.to_json())

# convert the object into a dict
external_api_waybill_transport_costs_dict = external_api_waybill_transport_costs_instance.to_dict()
# create an instance of ExternalAPIWaybillTransportCosts from a dict
external_api_waybill_transport_costs_from_dict = ExternalAPIWaybillTransportCosts.from_dict(external_api_waybill_transport_costs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


