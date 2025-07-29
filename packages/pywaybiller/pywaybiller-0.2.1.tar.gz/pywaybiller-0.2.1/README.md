# PyWaybiller

## Installation

```shell
poetry add pywaybiller
```

## Usage

### Get all waybills

```python
import pywaybiller
import datetime

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=7)


client = pywaybiller.WaybillerClient(
    api_key="xxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    host="https://staging.app.waybiller.com/external-api",
)

for waybill in client.waybills.all(
    dispatcher_timestamp__gt=start_date.strftime("%Y-%m-%dT%H:%M:%S"),
    dispatcher_timestamp__lt=end_date.strftime("%Y-%m-%dT%H:%M:%S"),
):
    print(waybill)
```

All endpoint uses generator. It will load data page by page, querying later pages only if you need them.

## Saving data for later

```python
import pywaybiller
from pywaybiller.openapi_client import ExternalAPIVehicle
from my_project.models import SomeDjangoModel

instance = SomeDjangoModel()
# Sanitize data for serialization for later use
instance.json_field = pywaybiller.WaybillerClient.sanitize_for_serialization(
    ExternalAPIVehicle(
        id=1,
        reg_number="839PVF",
        trailer_reg_number="042TST",
        inactive=False,
        company_name="Test company",
        company_reg_code="10000042"
    )
)

instance.save()
instance.refresh_from_db()

# Rehydrate the data saved earlier
api_model = pywaybiller.WaybillerClient.deserialize_data(
    instance.json_field, ExternalAPIVehicle
)
```

Deserialize data method calls pydantic from_dict internally, but hides implementation details
that may change in future from the code using the API client.

## Updating schema and testing

To update schema from waybiller, run `make openapi`. It is possible that
this command will fail if waybiller schema changed significantly and the patch
can not be applied anymore. In this case, you will have to follow the steps
below to create a new patch

It is possible that Waybiller schema is not actually compliant with the data
that waybiller system sends. This causes problems, as server response will
not validate and exception will be raised. To work around this, we patch the
schema.

### Creating new schema patch

To create a schema patch, get the fresh schema from WB and patch it with the
existing patch:
```shell
make openapi-fetch
# The next may fail, but then you would need to manually port existing
# patch to the new patched schema
make openapi-apply-patch
```

Then, copy over the schema from `pywaybiller/openapi/waybiller_schema.json` to
`pywaybiller/openapi/waybiller_schema-patched.json` and edit it to make it 
consistent with what server sends (usually this involves removing validation
for strings to be non-empty, as the most common issue with schema is that
server actually sends empty strings where schema says it can not).

Finally run
```shell
make openapi-patch
```

This will update schema-fixes.patch, which should be commited to the repository.

### Testing with waybiller data

Waybiller team can make a dump of all entities for particular endpoint into a big
json file, so that we try to deserialize it and see if there are no validation 
errors. As this kind of dump contains sensitive data, it is not possible to include
it in this repository.

To perform the manual test with this data dump, use `manual_test_json_dump.py`:
```shell
# in Waybiller - the management command is not merged to master yet, and may be gone in future
make docker-manage cmd="external_api_export --view waybill --endpoint list" > /tmp/waybills-list.json

# in pywaybiller
poetry run python tests/manual_test_json_dump.py --filename /tmp/waybills-list.json  --skip-lines 1 --model ExternalAPIWaybillList
```

To perform the manual test by direct API calls, use `manual_test_api.py`:
```shell
poetry run python tests/manual_test_api.py --model ExternalAPIWaybillList --api-key 'SECRET'
```

Note that you probably need to separately test list and detail endpoints, as schema is different.

This needs to be repeated for all endpoints you want to check. Currently, only waybill list and retrieve endpoints are
tested thoroughly with both staging and production data in this way. 

## Credits

This project is generated with help of dockerized openapi generator: https://hub.docker.com/r/openapitools/openapi-generator-cli