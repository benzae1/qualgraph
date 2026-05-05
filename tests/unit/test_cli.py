from pathlib import Path

from typer.testing import CliRunner

from qualgraph.cli import app


runner = CliRunner()


def test_python_module_entrypoint_exports_app() -> None:
    from qualgraph.__main__ import app as module_app

    assert module_app is app


def test_analyze_command_writes_public_artifacts(tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    artifacts_dir = tmp_path / "runs"

    result = runner.invoke(
        app,
        [
            "analyze",
            "benchmarks/repos/tiny_repo",
            "--output-dir",
            str(output_dir),
            "--preset",
            "fast",
            "--coverage-mode",
            "skip",
            "--artifacts-dir",
            str(artifacts_dir),
            "--top-n",
            "5",
        ],
    )

    assert result.exit_code == 0, result.output
    assert (output_dir / "graph.json").exists()
    assert (output_dir / "annotated.graph.json").exists()
    assert (output_dir / "report.md").exists()
    assert (output_dir / "export.json").exists()
    assert "Report:" in result.output
