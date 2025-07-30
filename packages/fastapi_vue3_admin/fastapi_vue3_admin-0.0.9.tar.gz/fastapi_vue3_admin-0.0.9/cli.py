import typer
import subprocess
from pathlib import Path
from importlib.metadata import version as pkg_version, PackageNotFoundError

from uvicorn import run
from cookiecutter.main import cookiecutter

cli = typer.Typer(help="fastapi_vue3_admin: 快速建立 FastAPI+Vue3 專案的腳手架")

try:
    __version__ = pkg_version("fastapi_vue3_admin")
except PackageNotFoundError:
    import tomllib, pathlib
    pyproject = pathlib.Path(__file__).with_name("pyproject.toml")
    if pyproject.exists():
        data = tomllib.loads(pyproject.read_text())
        __version__ = data["project"]["version"]
    else:
        __version__ = "0.0.0-dev"


@cli.command()
def dev(host: str = "0.0.0.0", port: int = 8000):
    """啟動開發伺服器"""
    run("app.main:app", host=host, port=port, reload=True)


@cli.command()
def migrate(message: str = "auto", upgrade: bool = True):
    """產生 Alembic 修訂並 (可選) 升級至最新版"""
    cmd_revision = ["alembic", "revision", "--autogenerate", "-m", message]
    subprocess.run(cmd_revision, check=True)
    if upgrade:
        subprocess.run(["alembic", "upgrade", "head"], check=True)


@cli.command()
def create(
    project_name: str,
    template: str | None = None,
    admin_email: str = "admin@example.com",
    admin_password: str = "123456",
):
    """由內建或自訂 Cookiecutter 模板建立新專案。

    範例：
        fva create my_project
        fva create my_project --template https://github.com/xxx/my_template.git
    """
    template_path = Path(template) if template else Path(__file__).with_suffix('').parent / "template"
    if not template_path.exists():
        typer.echo(f"找不到模板路徑: {template_path}")
        raise typer.Exit(code=1)

    typer.echo(f"使用模板 {template_path} 建立專案 {project_name} ...")
    cookiecutter(
        str(template_path),
        no_input=True,
        extra_context={
            "project_slug": project_name,
            "admin_email": admin_email,
            "admin_password": admin_password,
        },
    )


@cli.command()
def version():
    """顯示套件版本"""
    typer.echo(f"fastapi_vue3_admin {__version__}")


if __name__ == "__main__":
    cli() 