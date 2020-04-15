from unittest.mock import patch

from terraform_init import tfinit


@patch("terraform_init.tfinit.Path")
@patch("terraform_init.tfinit.create_file")
def test_main_with_modules(create_file, path, capsys):

    tfinit.main("--module module-A,module-B -vv tf".split())
    create_file.assert_called_with(
        "tf/_modules/module-B/variables.tf", force=False, verbosity=2
    )
    path.assert_called_with("tf/_modules/module-B")
    captured = capsys.readouterr()
    assert 'Module "module-A" created' in captured.out
    assert 'Module "module-B" created' in captured.out


@patch("terraform_init.tfinit.Path")
@patch("terraform_init.tfinit.create_file")
def test_main_with_profiles(create_file, path, capsys):

    tfinit.main(
        [
            "--profile",
            "demo,vip",
            "-vv",
            "--awsregion",
            "test-region",
            "--awsprofile",
            "test-profile",
            "terraform/test",
        ]
    )
    create_file.assert_called_with(
        "terraform/test/profiles/vip/provider.tf",
        force=False,
        verbosity=2,
        content="""provider "aws" {
    region    = "test-region"
    profile   = "test-profile"
    version   = "~> 2.39.0"
  }""",
    )
    path.assert_called_with("terraform/test/profiles/vip")
    captured = capsys.readouterr()
    assert 'Profile "vip" created' in captured.out
    assert 'Profile "demo" created' in captured.out


@patch("terraform_init.tfinit.Path")
@patch("terraform_init.tfinit.create_file")
def test_main_with_environments(create_file, path, capsys):

    tfinit.main(["--env", "test,prod", "--name", "fake", "-vv", "terraform/test"])
    create_file.assert_called_with(
        "terraform/test/environment/prod/input_vars.tfvars",
        force=False,
        verbosity=2,
        content="""bucket = "<fake-prod-backend-bucket>"
  key = "<alias/fake-prod-encryption-key>"
  region = "eu-west-1"
  dynamodb_table = "<fake-prod-backend-database>"
  encrypt = "true"
  profile = "default"
  """,
    )
    path.assert_called_with("terraform/test/environment/prod")
    captured = capsys.readouterr()
    assert 'Environment "test" created' in captured.out
    assert 'Environment "prod" created' in captured.out


@patch("terraform_init.tfinit.Path")
@patch("terraform_init.tfinit.create_file")
def test_main_with_all(create_file, path):
    tfinit.main(
        "-m sample_module -p sample_profile --env sample_env -n project -r sample-region .".split(
            " "
        )
    )
    expected_file_write_count = 2 + 4 + 1
    assert create_file.call_count == expected_file_write_count


def test_create_file(tmp_path, capsys):
    target = tmp_path / "bogus.tf"
    tfinit.create_file(path=str(target), content="content of the file", verbosity=0)
    assert target.read_text() == "content of the file"
    captured = capsys.readouterr()
    assert captured.out == ""


def test_create_file_with_force(tmp_path, capsys):
    target = tmp_path / "bogus.tf"
    target.write_text("Existing text")
    assert target.read_text() == "Existing text"

    tfinit.create_file(path=str(target), content="New content", force=True, verbosity=2)
    assert target.read_text() == "New content"
    captured = capsys.readouterr()
    assert captured.out == f"[+] {target}\n"


def test_create_file_with_skip(tmp_path, capsys):
    target = tmp_path / "bogus.tf"
    target.write_text("Existing text")

    tfinit.create_file(
        path=str(target), content="New content", force=False, verbosity=2
    )
    assert target.read_text() == "Existing text"
    captured = capsys.readouterr()
    assert captured.out == f"[s] {target}\n"
