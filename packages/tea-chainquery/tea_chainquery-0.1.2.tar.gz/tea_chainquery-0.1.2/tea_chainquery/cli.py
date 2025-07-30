import click
from tea_chainquery.blockchain import TeaChainQueryBlockchain

# Create a fresh Click group with explicit name
@click.group(name="cli")
def cli():
    """Sonia: A CLI tool for querying blockchain data."""
    pass


@cli.command(name="balance")
@click.argument("address")
def balance_command(address): 
    """Get the balance of an Ethereum/Base address."""
    query = TeaChainQueryBlockchain()
    try:
        balance = query.get_balance(address)
        click.echo(f"Balance: {balance} ETH")
    except ValueError as e:
        click.echo(f"Error: {e}")
        click.get_current_context().exit(0)  

@cli.command(name="tx_count")
@click.argument("address")
def tx_count_command(address):
    """Get the transaction count of an Ethereum/Base address."""
    query = TeaChainQueryBlockchain()
    try:
        count = query.get_transaction_count(address)
        click.echo(f"Transaction Count: {count}")
    except ValueError as e:
        click.echo(f"Error: {e}")
        click.get_current_context().exit(0) 

if __name__ == "__main__":
    cli()  