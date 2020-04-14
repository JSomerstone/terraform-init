# Terraform-init

Python tool for initializing Terraform (AWS) projects

## Usage

```
usage: init-terraform.py [-h] [--target TARGET] [--module MODULE]
                         [--profile PROFILE] [--env ENV]
                         [--awsprofile AWSPROFILE] [--awsregion AWSREGION]
                         [--force] [-v]
                         project

Terraform project initializer, creates basic folder structure and placeholder
files

positional arguments:
  project               Name of the project to be initialized

optional arguments:
  -h, --help            show this help message and exit
  --target TARGET       Where to create the project to, defaults to current
                        working directory
  --module MODULE, -m MODULE
                        Name(s) of the module(s) to create
  --profile PROFILE, -p PROFILE
                        Name(s) of the profile(s) to be initialized
  --env ENV             The environment(s) to create
  --awsprofile AWSPROFILE, -a AWSPROFILE
                        The profile in your AWS configuration to use
  --awsregion AWSREGION
                        AWS region, defaults to 'eu-west-1'
  --force, -f           Force overwrite of any existing files
  -v, --verbosity
```

## Examples

Create project with modules "lambda" and "api_gateway", environments "test" and "prod" and profile "sandbox"

`src/init-terraform.py example_project --module lambda,api_gateway --env test,prod --profile sandbox`

Will create directory structure: 
```
example_project
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

Create new module to existing project "pre_existing" in folder projectes/

`src/init-terraform.py pre_existing --module permission --target projects/` 

Will create folder `projects/pre_existing/_modules/permissions` with files base.tf and variables.tf