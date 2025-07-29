# ExternalAPIWaybillList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waybill_id** | **str** | The external ID of the waybill. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [readonly] 
**destination_id** | **str** | The external ID of the destination. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [readonly] 
**dispatcher_timestamp** | **datetime** | Waybill creation timestamp | [readonly] 
**driver_timestamp** | **datetime** | Timestamp when driver started driving | [readonly] 
**destination_timestamp** | **datetime** |  | [readonly] 
**confirmed_timestamp** | **datetime** | Time of confirmation in the destination | [readonly] 
**cancelled_timestamp** | **datetime** | Time of waybill cancelling | [readonly] 
**status** | [**WaybillStatusEnum**](WaybillStatusEnum.md) |  | [readonly] 
**number** | **str** |  | [readonly] 
**navision_bin_code** | **str** | Bin code. | [readonly] 
**project** | **str** | Project code in your system. | [readonly] 
**raw_data** | [**ExternalAPIWaybillRawDataList**](ExternalAPIWaybillRawDataList.md) | The IDs of the Waybiller internal objects | [readonly] 
**shipper_company_name** | **str** | The name of the shipper company. | [readonly] 
**origin_id** | **str** | The external ID of the origin. Usually &#x60;null&#x60; if waybill was created in Waybiller UI and not over Waybiller External API. | [readonly] 
**origin_name** | **str** |  | [readonly] 
**origin_address** | **str** |  | [readonly] 
**transportation_company_name** | **str** | The name of the transportation company. | [readonly] 
**driver_name** | **str** | The name of the driver. | [readonly] 
**truck_reg_number** | **str** | The registration number of the vehicle. | [readonly] 
**trailer_reg_number** | **str** | The registration number of the trailer. | [readonly] 
**receiver_company_name** | **str** | The name of the receiving company. | [readonly] 
**receiver_company_reg_code** | **str** | The registry code of the receiving company. | [readonly] 
**last_vehicle_location** | **Dict[str, object]** |  | [readonly] 
**destination_name** | **str** | The name of the destination. | [readonly] 
**destination_address** | **str** | The address of the destination. | [readonly] 
**dispatched_amount** | **decimal.Decimal** | The total dispatched amount. | [readonly] 
**rows** | [**List[ExternalAPIWaybillRowList]**](ExternalAPIWaybillRowList.md) | Waybill rows. | [readonly] 

## Example

```python
from openapi_client.models.external_api_waybill_list import ExternalAPIWaybillList

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIWaybillList from a JSON string
external_api_waybill_list_instance = ExternalAPIWaybillList.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIWaybillList.to_json())

# convert the object into a dict
external_api_waybill_list_dict = external_api_waybill_list_instance.to_dict()
# create an instance of ExternalAPIWaybillList from a dict
external_api_waybill_list_from_dict = ExternalAPIWaybillList.from_dict(external_api_waybill_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


