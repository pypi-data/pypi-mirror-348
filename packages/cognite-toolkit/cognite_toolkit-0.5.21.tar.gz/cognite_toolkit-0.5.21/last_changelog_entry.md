## cdf 

### Fixed

- In `cdf build`, when setting a `extractionPipelinesAcl` capability
with scope `idScope`, Toolkit no longer gives an incorrect warning.

### Improved

- When running `cdf build` and you get a `ResourceFormatWarning` the
json-path describing the location of the warning is now 1-based instead
of 0-based indexing
- Improved wording in `ResourceFormatWarning` error types.

## templates

No changes.