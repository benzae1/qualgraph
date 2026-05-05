import os
import sys
import threading
from pathlib import Path

import networkx as nx
import pytest

from qualgraph.graph.serialize import write_json_graph
from qualgraph.viewer.server import create_server

pytestmark = pytest.mark.e2e


def test_viewer_has_no_horizontal_overflow_and_draws_canvas(tmp_path: Path) -> None:
    if sys.platform == "win32" and not os.environ.get("CI"):
        pytest.skip("Local Windows sandbox can block Playwright's subprocess pipes; CI runs this on Linux.")
    playwright = pytest.importorskip("playwright.sync_api")
    graph_path = tmp_path / "viewer.graph.json"
    write_json_graph(_long_label_graph(), graph_path)
    server = create_server(graph_path, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        manager = playwright.sync_playwright()
        try:
            p = manager.start()
        except Exception as exc:
            pytest.skip(f"Playwright could not start in this environment: {exc}")
        try:
            try:
                browser = p.chromium.launch()
            except Exception as exc:
                pytest.skip(f"Playwright Chromium is not installed: {exc}")
            try:
                page = browser.new_page()
                for width, height in [(1440, 900), (820, 900), (390, 844)]:
                    page.set_viewport_size({"width": width, "height": height})
                    page.goto(server.url, wait_until="networkidle")
                    page.screenshot(path=tmp_path / f"viewer-{width}.png", full_page=True)

                    assert page.locator("text=Qualgraph").first.is_visible()
                    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1")
                    assert page.evaluate(
                        """
                        () => {
                          const canvas = document.querySelector('#graphCanvas');
                          const ctx = canvas.getContext('2d');
                          const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
                          for (let index = 0; index < data.length; index += 4) {
                            if (data[index] || data[index + 1] || data[index + 2]) return true;
                          }
                          return false;
                        }
                        """
                    )
            finally:
                browser.close()
        finally:
            p.stop()
    finally:
        server.shutdown()
        server.server_close()


def _long_label_graph() -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_node(
        "pkg/really_long_module_name.py::pkg.really_long_module_name.extremely_verbose_function_name_that_should_wrap::10",
        type="Function",
        name="extremely_verbose_function_name_that_should_wrap",
        qualified_name="pkg.really_long_module_name.extremely_verbose_function_name_that_should_wrap",
        file_path="pkg/really_long_module_name.py",
        line_start=10,
        line_end=20,
        source="def extremely_verbose_function_name_that_should_wrap():\n    return 'ok'\n",
        cluster_id=1,
        risk_score=2.5,
        findings=[
            {
                "source": "llm",
                "code": "maintainability",
                "severity": "MEDIUM",
                "message": "This finding has a deliberately long message that should wrap cleanly inside the inspector.",
            }
        ],
    )
    graph.add_node(
        "tests/test_long.py::tests.test_long.test_wraps::1",
        type="TestFunction",
        name="test_wraps",
        qualified_name="tests.test_long.test_wraps",
        file_path="tests/test_long.py",
        line_start=1,
        line_end=5,
        cluster_id=2,
        risk_score=0.0,
    )
    graph.add_edge(
        "pkg/really_long_module_name.py::pkg.really_long_module_name.extremely_verbose_function_name_that_should_wrap::10",
        "tests/test_long.py::tests.test_long.test_wraps::1",
        type="tested_by",
    )
    return graph
