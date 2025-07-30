from click.testing import CliRunner
from coragem.cli import cli

def test_balance_invalid_address():
    runner = CliRunner()
    result = runner.invoke(cli, ["balance", "invalid_address"])
    assert result.exit_code == 0
    assert "Error: Invalid address" in result.output

def test_tx_count_invalid_address():
    runner = CliRunner()
    result = runner.invoke(cli, ["tx_count", "invalid_address"])
    assert result.exit_code == 0
    assert "Error: Invalid address" in result.output
    