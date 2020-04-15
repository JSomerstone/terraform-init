# Terraform-init

Python tool for initializing Terraform (AWS) projects

## Usage

```
usage: tfinit.py [-h] [--name NAME] [--module MODULE] [--profile PROFILE]
                 [--env ENV] [--awsprofile AWSPROFILE] [--awsregion AWSREGION]
                 [--force] [-v]
                 target

Terraform project initializer, creates basic folder structure and placeholder
files

positional arguments:
  target                Where to create the project to, defaults to current
                        working directory (.)

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  Name of the project, defaults to name of the <target>
                        directory
  --module MODULE, -m MODULE
                        Name(s) of the module(s) to create
  --profile PROFILE, -p PROFILE
                        Name(s) of the profile(s) to be initialized
  --env ENV, -e ENV     The environment(s) to create
  --awsprofile AWSPROFILE, -a AWSPROFILE
                        The profile in your AWS configuration to use
  --awsregion AWSREGION, -r AWSREGION
                        AWS region, defaults to 'eu-west-1'
  --force, -f           Force overwrite of any existing files
  -v, --verbosity
```

## Examples

*Create terraform modules, environment and profile*

`tfinit.py --module lambda,api_gateway --env test,prod --profile sandbox`

Will create directory structure: 
```
/path/to/work/dir
├── _modules
│   ├── api_gateway
│   │   ├── base.tf
│   │   └── variables.tf
│   └── lambda
│       ├── base.tf
│       └── variables.tf
├── environment
│   ├── prod
│   │   └── input_vars.tfvars
│   └── test
│       └── input_vars.tfvars
└── profiles
    └── sandbox
        ├── main.tf
        ├── variables.tf
        ├── provider.tf
        └── backend.tf
```

*Create new module to existing project*

`tfinit.py --module permission projects/pre_existing` 

Will create folder `projects/pre_existing/_modules/permissions` with files base.tf and variables.tf

*Overwrite existing environment*

`tfinit.py --env sandbox --awsprofile development --awsregion eu-central-1 --force .` 

Will overwrite file `./environment/sandbox/input_vars.tfvars` with content:
```
bucket = "<tf-sandbox-backend-bucket>"
key = "<alias/tf-sandbox-encryption-key>"
region = "eu-central-1"
dynamodb_table = "<tf-sandbox-backend-database>"
encrypt = "true"
profile = "development"
```

## Development

### Pre-requirements
- pip
- pipenv

### Setting up
`pipenv sync -d`

### Running tests
```
# All tests
pipenv run test

# with coverage
pipenv run test:coverage
# open coverage report
open htmlcov/index.html
```

### House keeping
```
# linting
pipenv run lint

# auto-formatting
pipenv run autoformat
```