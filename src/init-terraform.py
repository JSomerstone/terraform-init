#!/usr/bin/env python
import os
from pathlib import Path
import argparse

from tools import ptree


def create_file(path, content = "", force = False, verbosity = 0):
  if not os.path.exists(path) or force:
      if verbosity > 0:
          print(f"[+] {path}")
      with open(path, 'w') as file_tf:
          if force:
            file_tf.write(content)
  elif verbosity > 1:
    print(f"[s] {path}")

parser = argparse.ArgumentParser(description='Terraform project initializer, creates basic folder structure and placeholder files')
parser.add_argument(
    "target", help="Where to create the project to, defaults to current working directory (.)", type=str, default=".")
parser.add_argument('--name', '-n', help="Name of the project, defaults to name of the <target> directory", type=str, default="")
parser.add_argument(
    "--module", "-m", help="Name(s) of the module(s) to create", type=str)
parser.add_argument(
    "--profile", "-p", help="Name(s) of the profile(s) to be initialized", type=str)
parser.add_argument(
    "--env", help="The environment(s) to create", type=str)

parser.add_argument(
    "--awsprofile", "-a", help="The profile in your AWS configuration to use", type=str, default='default')
parser.add_argument(
    "--awsregion", help="AWS region, defaults to 'eu-west-1'", default="eu-west-1", type=str)


parser.add_argument(
    "--force", "-f", help="Force overwrite of any existing files", action="store_true"
)
parser.add_argument("-v", "--verbosity", action="count", default=0)


args = parser.parse_args()
modules = []
profiles = []
environments = []

if args.target == '.':
  target = os.getcwd()
else:
  target = args.target

if args.name:
  project = args.name
else:
  project = target.split('/')[-1]

if args.module:
  for item in args.module.split(","):
    modules.append(item.strip())

if args.profile:
  for item in args.profile.split(","):
    profiles.append(item.strip())

if args.env:
  for item in args.env.split(","):
    environments.append(item.strip())


if modules and args.verbosity > 0:
  print(f'\nCreating {len(modules)} module(s)... ')

for module in modules:
  Path(f"{target}/_modules/{module}").mkdir(parents=True, exist_ok=True)
  for tf in ['base.tf', 'variables.tf']:
    path = f"{target}/_modules/{module}/{tf}"
    create_file(path, force=args.force, verbosity=args.verbosity)

  if args.verbosity > 1:
    print(f'Module "{module}" created')

if profiles and args.verbosity > 0:
  print(f'\nCreating {len(profiles)} profile(s)...')

for profile in profiles:
  Path(f"{target}/profiles/{profile}").mkdir(parents=True, exist_ok=True)
  for tf in ['main.tf', 'variables.tf']:
    path = f"{target}/profiles/{profile}/{tf}"
    create_file(path, force=args.force, verbosity=args.verbosity)
  
  create_file(
      f"{target}/profiles/{profile}/backend.tf",
      force=args.force,
      verbosity=args.verbosity,
      content="""terraform {
  backend "local" {
  }
  required_version = "~> 0.12.0"
}"""
  )

  create_file(
      f"{target}/profiles/{profile}/provider.tf",
      force=args.force,
      verbosity=args.verbosity,
      content=f"""provider "aws" {{
  region    = "{args.awsregion}"
  profile   = "{args.awsprofile}"
  version   = "~> 2.39.0"
}}"""
  )
  if args.verbosity > 1:
    print(f'Profile "{profile}" created')

    
if environments and args.verbosity > 0:
  print(f'\nCreating {len(environments)} environment(s)...')
for env in environments:
  Path(f"{target}/environment/{env}").mkdir(parents=True, exist_ok=True)
  path = f"{target}/environment/{env}/input_vars.tfvars"
  create_file(path, force=args.force, verbosity=args.verbosity, content=
              f"""bucket = "<{project}-{env}-backend-bucket>"
key = "<alias/{project}-{env}-encryption-key>"
region = "{args.awsregion}"
dynamodb_table = "<{project}-{env}-backend-database>"
encrypt = "true"
profile = "{args.awsprofile}"
"""
  )

  if args.verbosity > 1:
    print(f'Environment "{env}" created')

if args.verbosity > 0:
  print('\nDone; project structure:\n')
  ptree(target)
