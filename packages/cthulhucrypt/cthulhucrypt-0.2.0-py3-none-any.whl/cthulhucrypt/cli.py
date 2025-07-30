# cthulhucrypt/cli.py
import click
from .core import (
    encrypt,
    decrypt,
    character_pairing,
    bitwise_xor_transform,
    math_chaos,
    dynamic_substitute,
    med_hash,
    high_hash,
    hash2,
    hash2_high,
    final_message,
    remove_spaces,
)

@click.group()
def cli():
    """CthulhuCrypt CLI - An unholy encryption toolkit."""
    pass

@cli.command()
@click.argument("text")
def encrypt_cli(text):
    """Encrypt text (returns hex and table index)."""
    result, table_idx = encrypt(text)
    click.echo(f"Encrypted: {result}\nTable Index: {table_idx}")

@cli.command()
@click.argument("text")
@click.argument("table_idx", type=int)
def decrypt_cli(text, table_idx):
    """Decrypt hex text with table index."""
    try:
        result = decrypt(text, table_idx)
        click.echo(f"Decrypted: {result}")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.argument("text")
def character_pairing_cli(text):
    """Run character_pairing on text."""
    result = character_pairing(text)
    click.echo(f"Paired Digits: {result}")

@cli.command()
@click.argument("text")
def xor_transform_cli(text):
    """Run bitwise_xor_transform on text."""
    result = bitwise_xor_transform(text)
    click.echo(f"XOR Transformed: {result}")

@cli.command()
@click.argument("text")
def math_chaos_cli(text):
    """Run math_chaos on text."""
    result = math_chaos(text)
    click.echo(f"Math Chaos: {result}")

@cli.command()
@click.argument("text")
@click.option("--table-id", default=0, help="Table index for substitution")
def substitute_cli(text, table_id):
    """Run dynamic_substitute on text."""
    from .core import TABLES
    result = dynamic_substitute(text, [TABLES[table_id]])  # Single table for CLI
    click.echo(f"Substituted: {result}")

@cli.command()
@click.argument("text")
def med_hash_cli(text):
    """Run med_hash on text."""
    result = med_hash(text)
    click.echo(f"med_hash: {result}")

@cli.command()
@click.argument("text")
@click.option("--iterations", default=7, help="Number of iterations")
def high_hash_cli(text, iterations):
    """Run high_hash on text."""
    result = high_hash(text, iterations)
    click.echo(f"high_hash: {result}")

@cli.command()
@click.argument("text")
@click.option("--iterations", default=7, help="Number of iterations")
def hash2_cli(text, iterations):
    """Run hash2 on text."""
    result = hash2(text, iterations)
    click.echo(f"hash2: {result}")

@cli.command()
@click.argument("text")
@click.option("--iterations", default=7, help="Number of iterations")
def hash2_high_cli(text, iterations):
    """Run hash2_high on text."""
    result = hash2_high(text, iterations)
    click.echo(f"hash2_high: {result}")

@cli.command()
@click.argument("function")
@click.argument("unencrypted")
@click.option("--iterations", default=1, help="Number of iterations")
@click.option("--hex-output", is_flag=True, help="Output as hex")
@click.option("--output-file", default=None, help="Output file path")
def final_message_cli(function, unencrypted, iterations, hex_output, output_file):
    """Run final_message utility."""
    try:
        result = final_message(function, unencrypted, iterations, hex_output, output_file)
        if result is not None:
            click.echo(result)
        elif output_file:
            click.echo(f"Output written to {output_file}")
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == "__main__":
    cli()