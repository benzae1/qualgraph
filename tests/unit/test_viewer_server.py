import json
import threading
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

import networkx as nx

from qualgraph.graph.serialize import write_json_graph
from qualgraph.viewer.server import create_server


def test_viewer_server_serves_api_and_assets(tmp_path: Path) -> None:
    graph_path = tmp_path / "graph.json"
    write_json_graph(_server_graph(), graph_path)
    server = create_server(graph_path, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        summary = _json_get(f"{server.url}api/summary")
        graph = _json_get(f"{server.url}api/graph")
        node = _json_get(f"{server.url}api/node?id={quote('pkg/mod.py::pkg.mod.risky::10', safe='')}")
        html = urlopen(server.url, timeout=5).read().decode("utf-8")

        assert summary["nodes"] == 1
        assert graph["mode"] == "clusters"
        assert node["source"] == "def risky():\n    pass\n"
        assert "Qualgraph Viewer" in html
    finally:
        server.shutdown()
        server.server_close()


def _json_get(url: str) -> dict:
    with urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def _server_graph() -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_node(
        "pkg/mod.py::pkg.mod.risky::10",
        type="Function",
        name="risky",
        qualified_name="pkg.mod.risky",
        file_path="pkg/mod.py",
        line_start=10,
        line_end=11,
        source="def risky():\n    pass\n",
        cluster_id=1,
        risk_score=1.0,
    )
    return graph
