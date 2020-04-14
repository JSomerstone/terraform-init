import pytest
from unittest.mock import MagicMock, patch

from src import init_terraform


@patch('src.init_terraform.ptree')
@patch('src.init_terraform.Path')
@patch('src.init_terraform.create_file')
def test_main_with_modules(create_file, path, ptree, capsys):

  init_terraform.main(['--module', 'module-A,module-B',
                       '-v', '-v', 'terraform/test'])
  create_file.assert_called_with(
    'terraform/test/_modules/module-B/variables.tf',
    force=False,
    verbosity=2
  )
  path.assert_called_with('terraform/test/_modules/module-B')
  captured = capsys.readouterr()
  assert 'Module "module-A" created' in captured.out
  assert 'Module "module-B" created' in captured.out


@patch('src.init_terraform.ptree')
@patch('src.init_terraform.Path')
@patch('src.init_terraform.create_file')
def test_main_with_profiles(create_file, path, ptree, capsys):

  init_terraform.main([
    '--profile', 'demo,vip',
    '-v', '-v',
    '--awsregion', 'test-region',
    '--awsprofile', 'test-profile',
    'terraform/test'])
  create_file.assert_called_with(
      'terraform/test/profiles/vip/provider.tf',
      force=False,
      verbosity=2,
      content="""provider "aws" {
    region    = "test-region"
    profile   = "test-profile"
    version   = "~> 2.39.0"
  }"""
  )
  path.assert_called_with('terraform/test/profiles/vip')
  captured = capsys.readouterr()
  assert 'Profile "vip" created' in captured.out
  assert 'Profile "demo" created' in captured.out


@patch('src.init_terraform.ptree')
@patch('src.init_terraform.Path')
@patch('src.init_terraform.create_file')
def test_main_with_environments(create_file, path, ptree, capsys):

  init_terraform.main(['--env', 'test,prod', '--name', 'fake',
                       '-v', '-v', 'terraform/test'])
  create_file.assert_called_with(
      'terraform/test/environment/prod/input_vars.tfvars',
      force=False,
      verbosity=2,
      content="""bucket = "<fake-prod-backend-bucket>"
  key = "<alias/fake-prod-encryption-key>"
  region = "eu-west-1"
  dynamodb_table = "<fake-prod-backend-database>"
  encrypt = "true"
  profile = "default"
  """
  )
  path.assert_called_with('terraform/test/environment/prod')
  captured = capsys.readouterr()
  assert 'Environment "test" created' in captured.out
  assert 'Environment "prod" created' in captured.out
