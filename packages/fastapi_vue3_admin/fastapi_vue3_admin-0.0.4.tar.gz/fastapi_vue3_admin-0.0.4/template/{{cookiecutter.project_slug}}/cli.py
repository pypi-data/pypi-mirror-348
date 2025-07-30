import subprocess
import typer
from uvicorn import run

cli = typer.Typer(help="{{ cookiecutter.project_slug }} CLI 工具")

@cli.command()
def dev(host: str = "0.0.0.0", port: int = 8000):
    """啟動開發伺服器"""
    run("app.main:app", host=host, port=port, reload=True)

@cli.command()
def migrate(message: str = "auto", upgrade: bool = True):
    """產生 Alembic 修訂並 (可選) 升級至最新版"""
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message], check=True)
    if upgrade:
        subprocess.run(["alembic", "upgrade", "head"], check=True)

if __name__ == "__main__":
    cli() 