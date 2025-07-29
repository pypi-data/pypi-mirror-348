# ExternalAPIEmployment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique identifier of the employment | [readonly] 
**name** | **str** | Full name of the employee | [readonly] 
**email** | **str** | Email address of the employee | [readonly] 
**user_id** | **str** | Unique identifier of the employee&#39;s user account in Waybiller | [readonly] 
**role** | [**RoleEnum**](RoleEnum.md) | User&#39;s role within the company  * &#x60;manager&#x60; - Manager * &#x60;project_manager&#x60; - Project Manager * &#x60;object_manager&#x60; - Object Manager * &#x60;dispatcher&#x60; - Dispatcher * &#x60;driver&#x60; - Driver * &#x60;acceptor&#x60; - Acceptor * &#x60;loader_operator&#x60; - Loader operator | [readonly] 
**obsolete** | **bool** | Whether the employment has been deactivated | [readonly] [default to False]
**company_name** | **str** | Name of the employing company | [readonly] 
**company_reg_code** | **str** | Registration code of the employing company | [readonly] 
**subcontractor_company_name** | **str** | Name of the subcontractor company, if applicable | [readonly] 
**subcontractor_company_reg_code** | **str** | Registration code of the subcontractor company, if applicable | [readonly] 

## Example

```python
from openapi_client.models.external_api_employment import ExternalAPIEmployment

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIEmployment from a JSON string
external_api_employment_instance = ExternalAPIEmployment.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIEmployment.to_json())

# convert the object into a dict
external_api_employment_dict = external_api_employment_instance.to_dict()
# create an instance of ExternalAPIEmployment from a dict
external_api_employment_from_dict = ExternalAPIEmployment.from_dict(external_api_employment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


