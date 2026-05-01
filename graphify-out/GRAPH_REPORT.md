# Graph Report - analytify  (2026-04-30)

## Corpus Check
- 130 files · ~189,923 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2063 nodes · 7589 edges · 26 communities detected
- Extraction: 34% EXTRACTED · 66% INFERRED · 0% AMBIGUOUS · INFERRED: 5030 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]

## God Nodes (most connected - your core abstractions)
1. `test_client_factory()` - 310 edges
2. `Starlette` - 168 edges
3. `Route` - 164 edges
4. `Request` - 125 edges
5. `Response` - 116 edges
6. `PlainTextResponse` - 89 edges
7. `RunLogger` - 87 edges
8. `WebSocket` - 85 edges
9. `JSONResponse` - 80 edges
10. `Headers` - 71 edges

## Surprising Connections (you probably didn't know these)
- `register_url_convertor()` --calls--> `app()`  [INFERRED]
  benchmarks\repos\starlette\starlette\convertors.py → benchmarks\repos\starlette\tests\test_convertors.py
- `PlainTextResponse` --calls--> `func_homepage()`  [INFERRED]
  benchmarks\repos\starlette\starlette\responses.py → benchmarks\repos\starlette\tests\test_applications.py
- `PlainTextResponse` --calls--> `async_homepage()`  [INFERRED]
  benchmarks\repos\starlette\starlette\responses.py → benchmarks\repos\starlette\tests\test_applications.py
- `PlainTextResponse` --calls--> `all_users_page()`  [INFERRED]
  benchmarks\repos\starlette\starlette\responses.py → benchmarks\repos\starlette\tests\test_applications.py
- `PlainTextResponse` --calls--> `user_page()`  [INFERRED]
  benchmarks\repos\starlette\starlette\responses.py → benchmarks\repos\starlette\tests\test_applications.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (185): Creates an Starlette application., Initializes the application.          Parameters:             debug: Boolean, AuthCredentials, AuthenticationBackend, AuthenticationError, AuthenticationMiddleware, BaseUser, default_on_error() (+177 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (277): Starlette, test_client_factory(), Middleware, _MiddlewareFactory, Route, StaticFiles, __dir__(), __getattr__() (+269 more)

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (106): _add_edge(), _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files(), _docstring() (+98 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (145): ABC, AnalysisSummary, analyze_top_n(), _attach_findings(), build_request(), _cache_key(), _finding_payload(), _grammar_version() (+137 more)

### Community 4 - "Community 4"
Cohesion: 0.02
Nodes (121): requires(), all_users_page(), async_homepage(), client(), custom_subdomain(), custom_ws_exception_handler(), error_500(), func_homepage() (+113 more)

### Community 5 - "Community 5"
Cohesion: 0.02
Nodes (103): FloatConvertor, IntegerConvertor, PathConvertor, register_url_convertor(), StringConvertor, UUIDConvertor, _is_type_only_path(), Holds a string value that should not be revealed in tracebacks etc.     You sho (+95 more)

### Community 6 - "Community 6"
Cohesion: 0.04
Nodes (117): Definition, Build a NetworkX code graph from Python source files.  The builder intentionally, Git co-change annotator., _calls_from_node(), _calls_matching_package(), detect_complex_hotspots(), detect_cross_signal_findings(), detect_cyclic_dependencies() (+109 more)

### Community 7 - "Community 7"
Cohesion: 0.04
Nodes (72): BackgroundTasks, annotate(), _attach_run_summary(), build(), _default_llm_task_dir(), _default_model(), _echo_verbose_run(), export_json() (+64 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (32): Enum, Tiny order-processing package used as a qualgraph benchmark fixture., Inventory, Inventory storage and reservation logic., StockItem, Customer, CustomerTier, LineItem (+24 more)

### Community 9 - "Community 9"
Cohesion: 0.04
Nodes (57): Response, test_routes(), test_url_path_for(), test_streaming_response_on_client_disconnects(), test_streaming_response_stops_if_receiving_http_disconnect(), assert_middleware_header_route(), async_endpoint(), client() (+49 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (22): ServerErrorMiddleware, HTMLResponse, test_debug_after_response_sent(), test_debug_html(), test_debug_not_http(), test_debug_text(), test_handler(), test_async_func() (+14 more)

### Community 11 - "Community 11"
Cohesion: 0.08
Nodes (28): build_context(), build_node_analysis_prompt(), evidence_corpus(), _node_summary(), Build graph-aware LLM prompts., render_analysis_prompt(), _template_env(), _truncate() (+20 more)

### Community 12 - "Community 12"
Cohesion: 0.1
Nodes (27): _finding_payload(), _relative_to_repo(), _severity_num(), add_finding(), clear_findings_by_source(), finding_key(), Helpers for attaching tool findings to graph nodes., Remove stale findings from a previous run of the same annotator. (+19 more)

### Community 13 - "Community 13"
Cohesion: 0.09
Nodes (12): Protocol, echo_body(), hello_world(), return_exc_info(), test_wsgi_exc_info(), test_wsgi_exception(), test_wsgi_get(), AwaitableOrContextManagerWrapper (+4 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (11): Config, Environ, EnvironError, undefined, We use `assert_type` to test the types returned by Config via mypy., test_config(), test_config_types(), test_config_with_encoding() (+3 more)

### Community 15 - "Community 15"
Cohesion: 0.13
Nodes (17): HTTPException, websocket_raise_http_exception(), client(), no_content(), not_acceptable(), not_modified(), test_force_500_response(), test_handled_exc_after_response() (+9 more)

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (5): iterate_in_threadpool(), run_until_first_complete(), _StopIteration, test_iterate_in_threadpool(), test_run_until_first_complete()

### Community 17 - "Community 17"
Cohesion: 0.83
Nodes (3): main(), showRandomAnnouncement(), shuffle()

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Return ``node_id -> cluster_id`` using Leiden on an undirected graph.

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Write structured JSONL events and aggregate per-run counters.

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **50 isolated node(s):** `undefined`, `A URL path string that may also hold an associated protocol and/or host.     Us`, `Holds a string value that should not be revealed in tracebacks etc.     You sho`, `An immutable multidict.`, `An uploaded file included as part of the request data.` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 18`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Return ``node_id -> cluster_id`` using Leiden on an undirected graph.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `Write structured JSONL events and aggregate per-run counters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `test_client_factory()` connect `Community 1` to `Community 0`, `Community 2`, `Community 4`, `Community 5`, `Community 9`, `Community 10`, `Community 13`, `Community 15`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `Route` connect `Community 1` to `Community 0`, `Community 9`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `Request` connect `Community 0` to `Community 1`, `Community 2`, `Community 5`, `Community 8`, `Community 10`, `Community 11`, `Community 13`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 309 inferred relationships involving `test_client_factory()` (e.g. with `client()` and `test_subdomain_route()`) actually correct?**
  _`test_client_factory()` has 309 INFERRED edges - model-reasoned connections that need verification._
- **Are the 157 inferred relationships involving `Starlette` (e.g. with `State` and `URLPath`) actually correct?**
  _`Starlette` has 157 INFERRED edges - model-reasoned connections that need verification._
- **Are the 155 inferred relationships involving `Route` (e.g. with `Convertor` and `URL`) actually correct?**
  _`Route` has 155 INFERRED edges - model-reasoned connections that need verification._
- **Are the 117 inferred relationships involving `str` (e.g. with `.to_string()` and `.convert()`) actually correct?**
  _`str` has 117 INFERRED edges - model-reasoned connections that need verification._