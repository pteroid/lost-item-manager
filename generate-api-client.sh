#!/usr/bin/env bash
openapi-generator generate \
    --input-spec http://localhost/api/v1/openapi.json \
    --generator-name typescript-axios \
    --output frontend/src/backend
