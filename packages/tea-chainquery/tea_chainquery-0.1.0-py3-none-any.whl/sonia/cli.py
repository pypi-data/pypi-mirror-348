import click
from sonia.blockchain import SoniaBlockchain

# Create a fresh Click group with explicit name
@click.group(name="cli")
def cli():
    """Sonia: A CLI tool for querying blockchain data."""
    pass

# Explicitly name the commands
@cli.command(name="balance")
@click.argument("address")
def balance_command(address):  # Changed function name to avoid potential conflicts
    """Get the balance of an Ethereum/Base address."""
    query = SoniaBlockchain()
    try:
        balance = query.get_balance(address)
        click.echo(f"Balance: {balance} ETH")
    except ValueError as e:
        click.echo(f"Error: {e}")
        click.get_current_context().exit(0)  # Force exit code 0

@cli.command(name="tx_count")
@click.argument("address")
def tx_count_command(address):  # Changed function name to avoid potential conflicts
    """Get the transaction count of an Ethereum/Base address."""
    query = SoniaBlockchain()
    try:
        count = query.get_transaction_count(address)
        click.echo(f"Transaction Count: {count}")
    except ValueError as e:
        click.echo(f"Error: {e}")
        click.get_current_context().exit(0)  # Force exit code 0

if __name__ == "__main__":
    cli()  # pragma: no cover