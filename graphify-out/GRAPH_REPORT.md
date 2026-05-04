# Graph Report - analytify  (2026-05-04)

## Corpus Check
- 748 files · ~942,824 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 16185 nodes · 66093 edges · 66 communities detected
- Extraction: 32% EXTRACTED · 68% INFERRED · 0% AMBIGUOUS · INFERRED: 44757 edges (avg confidence: 0.66)
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
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 103|Community 103]]
- [[_COMMUNITY_Community 104|Community 104]]
- [[_COMMUNITY_Community 105|Community 105]]
- [[_COMMUNITY_Community 106|Community 106]]
- [[_COMMUNITY_Community 107|Community 107]]
- [[_COMMUNITY_Community 108|Community 108]]
- [[_COMMUNITY_Community 109|Community 109]]
- [[_COMMUNITY_Community 110|Community 110]]
- [[_COMMUNITY_Community 111|Community 111]]
- [[_COMMUNITY_Community 112|Community 112]]
- [[_COMMUNITY_Community 113|Community 113]]
- [[_COMMUNITY_Community 114|Community 114]]
- [[_COMMUNITY_Community 115|Community 115]]

## God Nodes (most connected - your core abstractions)
1. `Application` - 903 edges
2. `Crawler` - 610 edges
3. `url()` - 568 edges
4. `url()` - 567 edges
5. `ScrapyDeprecationWarning` - 538 edges
6. `aiohttp_client()` - 521 edges
7. `ClientResponse` - 431 edges
8. `AbstractStreamWriter` - 411 edges
9. `MockServer` - 393 edges
10. `get_crawler()` - 353 edges

## Surprising Connections (you probably didn't know these)
- `AbstractCookieJar` --uses--> `Save cookies to a file using JSON format.          :param file_path: Path to f`  [INFERRED]
  benchmarks\repos\aiohttp\aiohttp\abc.py → benchmarks\repos\aiohttp\aiohttp\cookiejar.py
- `AbstractCookieJar` --uses--> `Remove expired cookies.`  [INFERRED]
  benchmarks\repos\aiohttp\aiohttp\abc.py → benchmarks\repos\aiohttp\aiohttp\cookiejar.py
- `AbstractCookieJar` --uses--> `Returns this jar's cookies filtered by their attributes.`  [INFERRED]
  benchmarks\repos\aiohttp\aiohttp\abc.py → benchmarks\repos\aiohttp\aiohttp\cookiejar.py
- `AbstractCookieJar` --uses--> `Implements a dummy cookie storage.      It can be used with the ClientSession`  [INFERRED]
  benchmarks\repos\aiohttp\aiohttp\abc.py → benchmarks\repos\aiohttp\aiohttp\cookiejar.py
- `AbstractStreamWriter` --uses--> `Test writer that captures written bytes in a buffer.`  [INFERRED]
  benchmarks\repos\aiohttp\aiohttp\abc.py → benchmarks\repos\aiohttp\tests\test_payload.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** — annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** — annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** — cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** — anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** — parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** — metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.0
Nodes (1365): ABC, ABCMeta, AddonManager, This class facilitates loading and storing :ref:`topics-addons`., Load add-ons and configurations from a settings object and apply them., Update early settings that do not require a crawler instance, such as SPIDER_MOD, AjaxCrawlMiddleware, _has_ajaxcrawlable_meta() (+1357 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (1224): _parallel_asyncio(), Execute a callable over the objects in the given iterable, in parallel,     usi, init(), main(), Run a simple test server with basic auth endpoints., Run all basic auth middleware tests., Test server for basic auth endpoints., run_test_server() (+1216 more)

### Community 2 - "Community 2"
Cohesion: 0.01
Nodes (632): AbstractAccessLogger, AbstractAsyncAccessLogger, AbstractMatchInfo, AbstractRouter, AbstractStreamWriter, AbstractView, Execute the view handler., Resolve result.      This is the result returned from an AbstractResolver's (+624 more)

### Community 3 - "Community 3"
Cohesion: 0.01
Nodes (822): AbstractCookieJar, AbstractResolver, ResolveResult, AbstractResolver, BaseProtocol, _BaseRequestContextManager, ClientTimeout, delete() (+814 more)

### Community 4 - "Community 4"
Cohesion: 0.01
Nodes (802): AbstractCookieJar, time(), escape_quotes(), parse_header_pairs(), unescape_quotes(), links(), url(), call() (+794 more)

### Community 5 - "Community 5"
Cohesion: 0.01
Nodes (718): Creates an Starlette application., Initializes the application.          Parameters:             debug: Boolean, Starlette, AssertionError, AuthCredentials, AuthenticationBackend, AuthenticationError, AuthenticationMiddleware (+710 more)

### Community 6 - "Community 6"
Cohesion: 0.01
Nodes (414): CachingHostnameResolverSpider, type(), CoreStats, from_crawler(), Extension for collecting core stats like items scraped and start/finish times, port(), _lookup_exception_handler(), wrap_app_handling_exceptions() (+406 more)

### Community 7 - "Community 7"
Cohesion: 0.01
Nodes (704): AbstractStreamWriter, background_tasks(), listen_to_valkey(), on_shutdown(), websocket_handler(), A protected resource that requires any valid auth., Handle basic auth validation., fm_size() (+696 more)

### Community 8 - "Community 8"
Cohesion: 0.01
Nodes (389): Agent, H2Agent, H2ConnectionPool, Close all the HTTP/2 connections and remove them from pool          Returns:, Arguments:             uri - URI obtained directly from request URL, We use the proxy uri instead of uri obtained from request url, ScrapyProxyH2Agent, BaseDownloadHandler (+381 more)

### Community 9 - "Community 9"
Cohesion: 0.01
Nodes (350): load_pre_crawler_settings(), main(), ClientFactory, annotate_clusters(), cluster_leiden(), _cluster_partition(), _coarsen_clusters(), _compact_cluster_ids() (+342 more)

### Community 10 - "Community 10"
Cohesion: 0.01
Nodes (400): boot(), draw(), drillCluster(), escapeAttr(), escapeHtml(), fetchJson(), findingCard(), fmt() (+392 more)

### Community 11 - "Community 11"
Cohesion: 0.01
Nodes (238): load_response(), NotSupported, Indicates a feature or method is not supported, CSVFeedSpider, This module implements the XMLFeedSpider which is the recommended spider to use, Spider for parsing CSV feeds.     It receives a CSV file in a response; iterate, This method has the same purpose as the one in XMLFeedSpider, This method has the same purpose as the one in XMLFeedSpider (+230 more)

### Community 12 - "Community 12"
Cohesion: 0.02
Nodes (439): AnalysisSummary, analyze_top_n(), _attach_findings(), build_request(), _cache_key(), _finding_payload(), _grammar_version(), LLMAnalyzer (+431 more)

### Community 13 - "Community 13"
Cohesion: 0.01
Nodes (192): BaseHTTPRequestHandler, _gen_default_accept_encoding(), unused_port_socket(), _DummyLock, full_url(), host(), origin_req_host(), potential_domain_matches() (+184 more)

### Community 14 - "Community 14"
Cohesion: 0.02
Nodes (201): AioHTTPTestCase, BaseProtocol, Compress the data and returned the compressed bytes.          Note that flush(, ZLibBackendWrapper, Helpers for WebSocket protocol versions 13 and 8., Websocket masking function.      `mask` is a `bytes` object of length 4; `data, _websocket_mask_python(), ws_ext_gen() (+193 more)

### Community 15 - "Community 15"
Cohesion: 0.01
Nodes (120): as_async_generator(), collect_asyncgen(), Wraps an iterable (sync or async) into an async generator., _embed_bpython_shell(), _embed_ipython_shell(), _embed_ptpython_shell(), _embed_standard_shell(), get_shell_embed_func() (+112 more)

### Community 16 - "Community 16"
Cohesion: 0.02
Nodes (112): BaseRunSpiderCommand, Command, _colorize(), _enable_windows_terminal_processing(), pformat(), pprint(), pprint and pformat wrappers with colorization support, _tty_supports_color() (+104 more)

### Community 17 - "Community 17"
Cohesion: 0.02
Nodes (171): cookies(), parse_cookie_header(), parse_set_cookie_headers(), preserve_morsel_with_coded_value(), Unquote a cookie value.      Vendored from http.cookies._unquote to ensure com, Parse a Cookie header according to RFC 6265 Section 5.4.      Cookie headers c, Parse cookie headers using a vendored version of SimpleCookie parsing.      Th, Preserve a Morsel's coded_value exactly as received from the server.      This (+163 more)

### Community 18 - "Community 18"
Cohesion: 0.03
Nodes (38): curl_to_request_kwargs(), CurlParser, DataAction, _parse_headers_and_cookies(), Convert a cURL command syntax to Request kwargs.      :param str curl_command:, from_response(), _get_clickable(), _get_form() (+30 more)

### Community 19 - "Community 19"
Cohesion: 0.02
Nodes (61): _BenchServer, _BenchSpider, Command, A spider that follows all links, Command, TextTestResult, _pop_command_name(), Command (+53 more)

### Community 20 - "Community 20"
Cohesion: 0.02
Nodes (82): coroutine_test(), inline_callbacks_test(), Mark a test function written in a :func:`twisted.internet.defer.inlineCallbacks`, Mark a test function that returns a coroutine.      * with ``pytest-twisted``, main(), MockDNSResolver, MockDNSServer, Implements twisted.internet.interfaces.IResolver partially (+74 more)

### Community 21 - "Community 21"
Cohesion: 0.07
Nodes (89): BaseSpiderMiddleware, from_crawler(), process_spider_output(), process_spider_output_async(), Return a processed item from the spider output.          This method is called, Optional base class for spider middlewares.      .. versionadded:: 2.13, Return a processed request from the spider output.          This method is cal, BaseSpiderMiddleware (+81 more)

### Community 22 - "Community 22"
Cohesion: 0.04
Nodes (11): content_disposition_filename(), filename(), name(), parse_content_disposition(), test_attwithfn2231iso_bad(), test_attwithfn2231nbadpct1(), test_attwithfn2231nbadpct2(), test_attwithfn2231utf8_bad() (+3 more)

### Community 23 - "Community 23"
Cohesion: 0.08
Nodes (24): started(), AsyncioWorker, BaseTestWorker, test__create_ssl_context_with_ca_certs(), test__create_ssl_context_with_ciphers(), test__create_ssl_context_without_certs_and_ciphers(), test__get_valid_log_format_exc(), test__get_valid_log_format_ok() (+16 more)

### Community 24 - "Community 24"
Cohesion: 0.12
Nodes (5): test_absolute_path(), test_custom_asyncio_loop_enabled_true(), test_runspider_log_short_names(), TestRunSpiderCommand, TestWindowsRunSpiderCommand

### Community 25 - "Community 25"
Cohesion: 0.12
Nodes (11): Config, Environ, EnvironError, undefined, We use `assert_type` to test the types returned by Config via mypy., test_config(), test_config_types(), test_config_with_encoding() (+3 more)

### Community 26 - "Community 26"
Cohesion: 0.11
Nodes (9): Bz2Plugin, GzipPlugin, LZMAPlugin, Extension for processing data before they are exported to feeds., Uses all the declared plugins to process data first, then writes         the pr, Compresses received data using `gzip <https://en.wikipedia.org/wiki/Gzip>`_., Close the target file along with all the plugins., Compresses received data using `bz2 <https://en.wikipedia.org/wiki/Bzip2>`_. (+1 more)

### Community 27 - "Community 27"
Cohesion: 0.21
Nodes (4): is_generator_with_return_value(), warn_on_generator_with_return_value(), test_indentation_error(), TestUtilsMisc

### Community 28 - "Community 28"
Cohesion: 0.17
Nodes (11): codspeed benchmarks for the web responses., Benchmark creating 100 web.Response with headers., Benchmark creating 100 web.Response with bytes., Benchmark creating 100 web.Response with text., Benchmark creating 100 simple web.StreamResponse., Benchmark creating 100 simple web.Response., test_simple_web_response(), test_simple_web_stream_response() (+3 more)

### Community 29 - "Community 29"
Cohesion: 0.29
Nodes (1): test_warning_checks()

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (3): ProcessWithZeroDivisionErrorPipeline, Some pipelines used for testing, ZeroDivisionErrorPipeline

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (1): _py_files()

### Community 33 - "Community 33"
Cohesion: 0.5
Nodes (3): codspeed benchmarks for http writer., Benchmark 100 calls to _serialize_headers., test_serialize_headers()

### Community 34 - "Community 34"
Cohesion: 0.5
Nodes (3): Tests that make sure parts needed for the scrapy-poet stack work., Making sure annotations on all non-abstract callbacks can be resolved., test_callbacks()

### Community 35 - "Community 35"
Cohesion: 0.67
Nodes (1): ExceptionSpider

### Community 36 - "Community 36"
Cohesion: 0.67
Nodes (1): NormalSpider

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): # NOTE: makefile cythonizes all Cython modules

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Scrapy signals  These signals are documented in docs/topics/signals.rst. Pleas

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (1): Decompress the given data.

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (1): Return True if more output is available by passing b"".

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): Create a BasicAuth object from an Authorization HTTP header.

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): Create BasicAuth from url.

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (1): The value of content part for Content-Type HTTP header.

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): The value of charset part for Content-Type HTTP header.

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (1): The value of Content-Length HTTP header.

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (1): Create a CallLaterResult from an asyncio TimerHandle.

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (1): Create a CallLaterResult from a Twisted DelayedCall.

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (1): Create a Scrapy project in a temporary directory and return its path.

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (1): Copy a pre-generated Scrapy project into a temporary directory and return its pa

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (1): Add text to the end of the project settings.py.

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (1): Replace custom_settings in the given spider file with the given text.

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 103 - "Community 103"
Cohesion: 1.0
Nodes (1): Return ``node_id -> cluster_id`` using Leiden on an undirected graph.

### Community 104 - "Community 104"
Cohesion: 1.0
Nodes (1): Return ``node_id -> cluster_id`` using Leiden on an undirected graph.

### Community 105 - "Community 105"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 106 - "Community 106"
Cohesion: 1.0
Nodes (1): Check that the underlying tool is installed and runnable.

### Community 107 - "Community 107"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 108 - "Community 108"
Cohesion: 1.0
Nodes (1): Write centrality and degree metrics back onto graph nodes.

### Community 109 - "Community 109"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 110 - "Community 110"
Cohesion: 1.0
Nodes (1): Return ``node_id -> cluster_id`` using Leiden on an undirected graph.

### Community 111 - "Community 111"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 112 - "Community 112"
Cohesion: 1.0
Nodes (1): Write structured JSONL events and aggregate per-run counters.

### Community 113 - "Community 113"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 114 - "Community 114"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 115 - "Community 115"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **511 isolated node(s):** `# NOTE: makefile cythonizes all Cython modules`, `Base class for decompression handlers.`, `Decompress the given data.`, `Decompress the given data.`, `Return True if more output is available by passing b"".` (+506 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 29`** (7 nodes): `test_pytest_plugin.py`, `test_aiohttp_client_cls_fixture_custom_client_used()`, `test_aiohttp_client_cls_fixture_factory()`, `test_aiohttp_plugin()`, `test_aiohttp_plugin_async_fixture()`, `test_aiohttp_plugin_async_gen_fixture()`, `test_warning_checks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (6 nodes): `conftest.py`, `mockserver()`, `_py_files()`, `pytest_addoption()`, `pytest_runtest_setup()`, `reactor_pytest()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (3 nodes): `exception.py`, `ExceptionSpider`, `.parse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (3 nodes): `normal.py`, `NormalSpider`, `.parse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (2 nodes): `setup.py`, `# NOTE: makefile cythonizes all Cython modules`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (2 nodes): `signals.py`, `Scrapy signals  These signals are documented in docs/topics/signals.rst. Pleas`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `Decompress the given data.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `Return True if more output is available by passing b"".`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `Create a BasicAuth object from an Authorization HTTP header.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `Create BasicAuth from url.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `The value of content part for Content-Type HTTP header.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `The value of charset part for Content-Type HTTP header.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `The value of Content-Length HTTP header.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (1 nodes): `Create a CallLaterResult from an asyncio TimerHandle.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (1 nodes): `Create a CallLaterResult from a Twisted DelayedCall.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `Create a Scrapy project in a temporary directory and return its path.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (1 nodes): `Copy a pre-generated Scrapy project into a temporary directory and return its pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `Add text to the end of the project settings.py.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (1 nodes): `Replace custom_settings in the given spider file with the given text.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 103`** (1 nodes): `Return ``node_id -> cluster_id`` using Leiden on an undirected graph.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 104`** (1 nodes): `Return ``node_id -> cluster_id`` using Leiden on an undirected graph.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 105`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 106`** (1 nodes): `Check that the underlying tool is installed and runnable.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 107`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 108`** (1 nodes): `Write centrality and degree metrics back onto graph nodes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 109`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 110`** (1 nodes): `Return ``node_id -> cluster_id`` using Leiden on an undirected graph.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 111`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 112`** (1 nodes): `Write structured JSONL events and aggregate per-run counters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 113`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 114`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 115`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Crawler` connect `Community 0` to `Community 3`, `Community 4`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 13`, `Community 16`, `Community 21`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `Application` connect `Community 1` to `Community 2`, `Community 3`, `Community 7`, `Community 14`, `Community 15`, `Community 23`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `ScrapyDeprecationWarning` connect `Community 0` to `Community 1`, `Community 4`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 13`, `Community 15`, `Community 20`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 876 inferred relationships involving `Application` (e.g. with `AbstractRouter` and `AbstractMatchInfo`) actually correct?**
  _`Application` has 876 INFERRED edges - model-reasoned connections that need verification._
- **Are the 593 inferred relationships involving `Crawler` (e.g. with `AddonManager` and `This class facilitates loading and storing :ref:`topics-addons`.`) actually correct?**
  _`Crawler` has 593 INFERRED edges - model-reasoned connections that need verification._
- **Are the 569 inferred relationships involving `str` (e.g. with `.__str__()` and `.__str__()`) actually correct?**
  _`str` has 569 INFERRED edges - model-reasoned connections that need verification._
- **Are the 566 inferred relationships involving `url()` (e.g. with `.__init__()` and `._build_url()`) actually correct?**
  _`url()` has 566 INFERRED edges - model-reasoned connections that need verification._