"""Local HTTP server for the bundled Qualgraph viewer."""

from __future__ import annotations

import json
import mimetypes
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from qualgraph.viewer.model import ViewerData


class ViewerServer(ThreadingHTTPServer):
    """ThreadingHTTPServer carrying immutable viewer data."""

    def __init__(self, server_address: tuple[str, int], viewer: ViewerData) -> None:
        super().__init__(server_address, ViewerRequestHandler)
        self.viewer = viewer

    @property
    def url(self) -> str:
        host, port = self.server_address
        display_host = "127.0.0.1" if host in {"", "0.0.0.0"} else host
        return f"http://{display_host}:{port}/"


class ViewerRequestHandler(BaseHTTPRequestHandler):
    server: ViewerServer

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path == "/":
            self._send_asset("index.html")
            return
        if parsed.path.startswith("/assets/"):
            self._send_asset(parsed.path.removeprefix("/assets/"))
            return
        if parsed.path == "/api/summary":
            self._send_json(self.server.viewer.summary())
            return
        if parsed.path == "/api/clusters":
            self._send_json({"clusters": self.server.viewer.clusters()})
            return
        if parsed.path == "/api/graph":
            cluster_id = _first(query.get("cluster"))
            self._send_json(self.server.viewer.graph_payload(cluster_id=cluster_id))
            return
        if parsed.path == "/api/findings":
            source = _first(query.get("source"))
            self._send_json({"findings": self.server.viewer.findings(source=source)})
            return
        if parsed.path == "/api/node":
            node_id = _first(query.get("id"))
            if not node_id:
                self._send_json({"error": "missing node id"}, status=HTTPStatus.BAD_REQUEST)
                return
            detail = self.server.viewer.node_detail(node_id)
            if detail is None:
                self._send_json({"error": "node not found"}, status=HTTPStatus.NOT_FOUND)
                return
            self._send_json(detail)
            return
        self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, _format: str, *args: Any) -> None:
        return

    def _send_json(self, payload: Any, *, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_asset(self, asset_name: str) -> None:
        clean_name = asset_name.strip("/").replace("\\", "/")
        if not clean_name or ".." in clean_name.split("/"):
            self._send_json({"error": "invalid asset"}, status=HTTPStatus.BAD_REQUEST)
            return
        try:
            asset = resources.files("qualgraph.viewer.assets").joinpath(clean_name)
            body = asset.read_bytes()
        except (FileNotFoundError, ModuleNotFoundError, IsADirectoryError):
            self._send_json({"error": "asset not found"}, status=HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(clean_name)[0] or "application/octet-stream"
        if clean_name.endswith(".js"):
            content_type = "text/javascript"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8" if content_type.startswith("text/") else content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)


def create_server(graph_path: str | Path, *, host: str = "127.0.0.1", port: int = 0, top_n: int = 50) -> ViewerServer:
    viewer = ViewerData.from_path(graph_path, top_n=top_n)
    return ViewerServer((host, port), viewer)


def serve_graph(
    graph_path: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 0,
    top_n: int = 50,
    open_browser: bool = False,
) -> str:
    server = create_server(graph_path, host=host, port=port, top_n=top_n)
    url = server.url
    if open_browser:
        threading.Timer(0.25, lambda: webbrowser.open(url)).start()
    try:
        print(f"Qualgraph viewer running at {url}")
        print("Press Ctrl+C to stop.")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return url


def _first(values: list[str] | None) -> str | None:
    if not values:
        return None
    return values[0]
