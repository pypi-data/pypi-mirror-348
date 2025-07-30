import typer
from pathlib import Path
from colorama import Fore
from .compiler import compiler

app = typer.Typer()

@app.command()
def main(
    file: str,
    obfuscate: str = typer.Option(
        None,
        help="Obfuscation method: minify, hex, base64, charcode"
    )
):
    file_path = Path(file).resolve()

    if not file_path.exists():
        typer.echo(Fore.RED + "File Not Found")
        typer.echo(Fore.RESET)
        raise typer.Exit(code=1)

    if not file.endswith(".h.sql"):
        typer.echo(Fore.RED + "File Is Not A .h.sql File")
        typer.echo(Fore.RESET)
        raise typer.Exit(code=1)

    content = file_path.read_text(encoding="utf-8")

    compiled_html = compiler(content, obfuscate=obfuscate)

    output_file = file.replace(".h.sql", ".html")
    with open(output_file, "w", encoding="utf-8") as code:
        code.write(compiled_html)

    typer.echo(Fore.GREEN + f"Compiled! Output written to {output_file}")
    typer.echo(Fore.RESET)


if __name__ == "__main__":
    app()
