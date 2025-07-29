# qubership-pipelines-modules-ops

## Description

This Python package provides functions to handle data for Qubership pipelines/modules.


## Operations

### Variables

#### Job variables transformation<a id="Jobvariablestransformation"></a>
Nested structures for certain `<root>` variables can be passed in two formats:
1.  string representation of yaml;
2.  hierarchical key representation.

Example:
```yaml
variables:
  <root>: |
    <string in yaml format>
  <root>__[<key>__...]PARAM: VALUE
```

Processing:
1.  Variable `<root>` is parsed as yaml.
2.  All variables with prefix `<root>` are combined:
    * Hierarchical keys are processed, using dot `.` or double underscore `__` as a delimiter.\
      **Note:** GitLab does not allow dots in variable names.
    * Elements of hierarchical keys can be:
      * strings - keys in mappings:\
        `keyA.keyB` and `keyA__keyB` where `keyB` is string, are treated as a hierarchical key for structure
        ```yaml
        keyA:
          keyB: value
        ```
      * integers - indexes in lists:\
        `keyA.N` and `keyA__N` where `N` is integer, are treated as a hierarchical key for structure
        ```yaml
        keyA:
          ...
          - value  # N'th position in the list, in 0-based numeration
          ...
        ```
3.  Then these two structures are merged as nested mappings.\
    Lists are treated as solid objects in this merge operation.\
    Priority is defined by the value of env variable `QUBERSHIP_PIPELINES_MODULES_OPS_PREFIXED_VARS_PRIORITY`.
    If `true` (default), prefixed parameters have greater priority.

#### Type casting
In GitLab, variable values ​​must be strings.

When collecting data, qubership_pipelines_modules_ops automatically applies type casting:
* `'true'` and `'false'` are converted into booleans;
* integer and float numbers are detected.

#### Variables substitution
GitLab substitutes variables given in notations `$VAR` and `${VAR}` when starting a job.
Only initially defined and predefined variables can be used in these substitutions.

Postponed substitution is implemented:
1. Escape variable in expression by doubling dollar symbol: `$$VAR` or `$${VAR}`.
   GitLab replaces double dollar sign with a single one, without substituting the variable:
   `$$VAR -> $VAR`, `$${VAR} -> ${VAR}`
2. qubership_pipelines_modules_ops performs substitution of these variables:
    * The following values are available for substitution:
        * Initially defined and predefined variables,
        * Parameters defined in the stored job data;
    * Nested variables substitution is implemented.

```yaml
variables:
  VAR_A: ${A}  # variable 'A' will be substituted by GitLab
  VAR_B: postponed $${B}  # variable 'B' will be substituted by qubership_pipelines_modules_ops
```


### Modules data
#### Input modules data
To compose input data (`input_params.yaml` and `input_params_secure.yaml`) for a module:
1. Stored data from previous jobs (parameters and files) is collected and combined.
   The order of the job stages is taken into account.
2. Then current job variables are added.

Variable `input` is processed as described in [Job variables transformation](#Jobvariablestransformation) section.

Additionally, the following shorthands can be used for prefixed variables:
``` yaml
<job_name>:
  variables:
    params__[<key>__...]PARAM: VALUE  # short for input__params__params__[<key>__...]PARAM: VALUE
    systems__[<key>__...]PARAM: VALUE  # short for input__params__systems__[<key>__...]PARAM: VALUE
```
I.e. prefix `input__params__` is optional in `input__params__params__` and `input__params__systems__` hierarchical keys.

Example:
```yaml
<job_name>:
  variables:
    input: |  # string in yaml format
      files:
        FILE_KEY: ... # <path, relative to input_files/>|<empty or null: means without renaming>
      params:
        params:
          PARAM: VALUE
        systems:
          PARAM: VALUE
      params_secure: {...}

    input__params__params__PARAM: VALUE
    params__PARAM: VALUE  # short for input__params__params__PARAM: VALUE
    systems__PARAM: VALUE  # short for input__params__systems__PARAM: VALUE
```


#### Output modules data
Module output parameters and files must be stored as artifacts, and be available in jobs in subsequent stages.

Variable `output` defines parameters and files that will be stored as module output.
It is processed as described in [Job variables transformation](#Jobvariablestransformation) section.

```yaml
<job_name>:
  variables:
    output: | # <string, in yaml format>
      params:
        NEW_PARAM_1: <hierarchical key in output_params.yaml or output_params_secure.yaml>|BUILD_STATUS|BUILD_URL|BUILD_DATE
        NEW_PARAM_2: ...
        PATH_IN_OUTPUT_YAML: '*'
      files:
        FILE_KEY_1: <file path relative to output_files/>
        FILE_KEY_2: ...
        PATH_IN_OUTPUT_YAML: '*'

    output__params__P: VALUE_OR_ASTERISK
    output__files__FILE_KEY: PATH_OR_ASTERISK
    ...
```

Under `output.params` mapping:
* *Key* defines parameter name.
* *Value* is the source for the parameter value. It can be:
    * a hierarchical key in `output_params.yaml` or `output_params_secure.yaml`;
    * one of the special environment variables: `BUILD_STATUS`, `BUILD_URL`, `BUILD_DATE` (must be provided)

* **Special case**: If the *value* is `*`, then the *key* is considered to be a path (i.e. hierarchical key)
  to a mapping in `output_params.yaml` or `output_params_secure.yaml` to get all values from, without renaming.
  For example, `output__params__params: '*'` instructs to import all parameters
  listed in `output_params.yaml` and in `output_params_secure.yaml`, under `params` section.

Under `output.files` mapping:
* *Key* defines file key (file identifier that can be used in later jobs as input parameter).
* *Value* is the file path, relative to `output_files` directory.
* **Special case**: If the *value* is `*`, then the *key* is considered to be a path (i.e. hierarchical key)
  to a mapping in `output_params.yaml` or `output_params_secure.yaml` to get all values from.
  For example, `output__files__files: '*'` instructs to import and copy all file keys
  listed in `output_params.yaml` and in `output_params_secure.yaml`, under `files` section.


#### Pipeline output
If `output__pipeline_output` parameter is present, then:
* Module output data is copied to `rt/pipeline/output` directory:
  * output params file,
  * output params secure file,
  * output files directory;
* Context descriptor `rt/pipeline/output/context.yaml` is created.
  Path in this context descriptor are relative to `rt/pipeline/output` directory.


#### Report
If variables contain `report` section and/or `report__` prefixed parameters,
an additional artifact will be generated in module input data: pipeline execution report.

During module input data preparation, variable `report` is processed as described in
[Job variables transformation](#Jobvariablestransformation) section.

Example of configuration:
```yaml
<job name>:
  variables:
    report: |
      version: v1  # Optional, default is 'v1'
      config:
        - name: PIPELINE_DATA
          value: ...
        ...
```
or equivalent in prefixed format:
```yaml
<job name>:
  variables:
    report__version: v1
    report__config__0__name: PIPELINE_DATA
    report__config__0__value: ...
    ...
```
Minimal configuration to activate report function:
```yaml
<job name>:
  variables:
    report: '{}'
```
`pipeline_execution_report.yaml` is generated and placed into `input_files/` directory.


#### Conditions
During module input data preparation, variable `when` is processed as described in
[Job variables transformation](#Jobvariablestransformation) section.

If variables contain `when.condition` (`when__condition`):
* its value is treated as a Python expression;
* the following entities can be used as variables in the expression:
  * parameters stored in previous jobs,
  * environment variables;
* if the expression evaluation gives Python falsy value (i.e. `bool(result) == False`), then:
  * an empty file `logs/.when_condition_false` is created (`logs` dir is in the same directory as context descriptor),
  * module_ops exits;
* Exit code is `0` by default,
  but can be changed by setting `QUBERSHIP_PIPELINES_MODULES_OPS_FALSE_CONDITION_EXIT_CODE` environment variable.

Example:
```yaml
<job_name>:
  variables:
    when:
      condition: rate > 95
```

## Development notes

### Storage layout
```txt
rt/
  job_data/    # not a part of public contract
    input_files/
    output_files/
    context.yaml
    input_params.yaml
    input_params_secure.yaml
    output_params.yaml
    output_params_secure.yaml
  stored_data/    # not a part of public contract
    <stage>/
      <job>/
        files/
        logs/
        files.yaml
        params.yaml
      stage.yaml
  pipeline/
    output/
      output_files/
      context.yaml
      output_params.yaml
      output_params_secure.yaml
```

### Testing
For testing purposes, a special handling of input files section is implemented:
```yaml
<job name>
  input:
    files:
      TEMP_FILE1: |
        file1.txt:
        file content
```
If the value of input files entry contains semicolon `:`, then it is treated as `<file_path>:<file_content>`.
* A new file is created in the input files directory, with the given path and content;
* One leading line break in the content is trimmed, if presents;
* The file key (`TEMP_FILE1` in the example above) is ignored.

