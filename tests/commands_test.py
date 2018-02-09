import betamax
import pytest


from yum import cli
from conftest import invoker
from click.testing import CliRunner


def test_cli_wrong():
    """Test the list_repos output and exit code"""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert 'Options:' in result.output.split("\n")
    assert 'Commands:' in result.output.split("\n")

def test_cli_bad_creddentials():
    """Test the gain output and exit code"""
    runner = CliRunner()
    result = runner.invoke(cli, ['-u', 'ihopenoonehasthisusername','gain'], obj={})
    print(result.output)
    assert result.exit_code == 1

def test_cli_gain():
    """Test the gain output and exit code"""
    runner = CliRunner()
    result = runner.invoke(cli, [ '-u', invoker.testingUsername(),
                                '-p', invoker.testingPassword(),
                                'gain'], obj={})
    assert 'Level:' in result.output
    assert 'Likes:' in result.output
    assert result.exit_code == 0

def test_cli_share():
    """
    Test sharing pictures on instagram
    """
    runner = CliRunner()
    result = runner.invoke(cli,[ '-u', invoker.testingUsername(),
                                '-p', invoker.testingPassword(),
                                'share',
                                 '-c',invoker.caption(),
                                 invoker.getDataPath('ramen.jpg')], obj={})
    assert result.exit_code == 0


def test_cli_food():
    """
    Test food list
    """
    runner = CliRunner()
    result = runner.invoke(cli, ['-u', invoker.testingUsername(),
                                '-p', invoker.testingPassword(),
                                 'food'], obj={ } )
    assert result.exit_code == 0
    assert len(result.output.split(" ")) > 2

def test_cli_bad_config():
    """
    Test food list
    """
    runner = CliRunner()
    result = runner.invoke(cli, ['-c', 'configthatdoesnt.exists', 'food'], obj={ } )
    assert result.exit_code == 1
    assert  result.output == invoker.errMsgConfig()
