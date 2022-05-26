from click.testing import CliRunner
from fsa.cli import entrypoint

runner = CliRunner()


def test_cli():
    response = runner.invoke(entrypoint.cli, ["show", "--case", "upper"])
    print()
    print(f"response.output=`{response.output}`")
    print(f"return_value=`{response.return_value}`")
    # print(help(response))
    assert response.exit_code == 0
