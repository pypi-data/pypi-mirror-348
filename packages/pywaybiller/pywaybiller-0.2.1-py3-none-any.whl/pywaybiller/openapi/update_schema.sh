docker-entrypoint.sh generate -i $1 -g python -o /openapi --skip-validate-spec

# Import generated code from the correct place
find /openapi/openapi_client -type f -exec sed -i 's/openapi_client.models/pywaybiller.openapi_client.models/g' {} +
find /openapi/openapi_client -type f -exec sed -i 's/from openapi_client/from pywaybiller.openapi_client/g' {} +
