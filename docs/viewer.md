# Local Viewer

The viewer is served locally from packaged static assets:

```bash
qualgraph serve .qualgraph/annotated.graph.json --open
```

Endpoints:

- `/`: viewer HTML
- `/api/health`: server and graph-path health payload
- `/api/summary`: counts, top-risk nodes, warnings, and annotator status
- `/api/clusters`: cluster list
- `/api/graph`: cluster, file, or symbol graph payload
- `/api/findings`: finding list
- `/api/node?id=<node-id>`: node detail

The viewer is designed for offline inspection. It does not send graph data to a
remote service.

## Quality Checks

The e2e viewer test opens the app at desktop, tablet, and mobile widths. It
captures screenshots, checks that the canvas is nonblank, and asserts that the
document has no horizontal overflow.
