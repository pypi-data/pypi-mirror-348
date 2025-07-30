
# ossbomer-schema

SBOM Schema Validation for SPDX and CycloneDX.

ossbomer-schema is a Python library that validates Software Bill of Materials (SBOMs) against SPDX and CycloneDX schemas. It ensures SBOMs are properly formatted in JSON and XML before further analysis.

## Features

* Supports SPDX 3.0, SPDX 2.3, and CycloneDX 1.3–1.6
* Validates both JSON and XML formats
* Uses local schemas (no remote dependency issues)
* Outputs results in both human-readable and JSON formats for API integration

## Usage

You can also use ossbomer-schema as a Python library:

```
from ossbomer_schema.validator import SBOMSchemaValidator

validator = SBOMSchemaValidator()
```

### Validate SPDX JSON
```
result = validator.validate_spdx_json("test_sbom.spdx.json")
print(result)  # "Valid" or error message
```

### Validate CycloneDX XML
```
result = validator.validate_cyclonedx_xml("test_sbom.cdx.xml")
print(result)  # "Valid" or error message
```

📂 SBOM Schema Support

| SBOM Format | Version | JSON | XML |
| ----------- | ------- | ---- | --- |
|    SPDX     | 2.3 | ✅   | 🚫 (No official schema) |
|    SPDX     | 3.0 | ✅   | 🚫 (No official schema) |
| CycloneDX   | 1.3 | ✅   | ✅ |
| CycloneDX   | 1.4 | ✅   | ✅ |
| CycloneDX   | 1.5 | ✅   | ✅ |
| CycloneDX   | 1.6 | ✅   | ✅ |

Note: SPDX 3.0 does not have an official XML schema, so XML validation is unavailable for that version.


### Testing

Run the test suite with:
```
$ python3 -m unittest discover tests
$ python3 -m tests.test_schema
```

## License

This project is licensed under MIT.

## Future Improvements

* Add official SPDX 3.0 XML validation (when available).
* Extend schema validation for new CycloneDX versions.
* Integrate with ossbomer-conformance for regulatory compliance checks.

## Questions?

Feel free to open an issue or contribute to the project! 🚀
