# Graph Report - analytify  (2026-05-04)

## Corpus Check
- 748 files · ~943,384 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 16193 nodes · 66109 edges · 66 communities detected
- Extraction: 32% EXTRACTED · 68% INFERRED · 0% AMBIGUOUS · INFERRED: 44761 edges (avg confidence: 0.66)
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
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 102|Community 102]]
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
Nodes (1128): AddonManager, This class facilitates loading and storing :ref:`topics-addons`., Load add-ons and configurations from a settings object and apply them., Update early settings that do not require a crawler instance, such as SPIDER_MOD, AjaxCrawlMiddleware, _has_ajaxcrawlable_meta(), Handle 'AJAX crawlable' pages marked as crawlable via meta tag., Return True if a page without hash fragment could be "AJAX crawlable". (+1120 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (828): AbstractCookieJar, AbstractResolver, ResolveResult, AbstractCookieJar, AbstractResolver, BaseProtocol, _BaseRequestContextManager, delete() (+820 more)

### Community 2 - "Community 2"
Cohesion: 0.01
Nodes (772): Creates an Starlette application., Initializes the application.          Parameters:             debug: Boolean, Starlette, AuthCredentials, AuthenticationBackend, AuthenticationError, AuthenticationMiddleware, BaseUser (+764 more)

### Community 3 - "Community 3"
Cohesion: 0.01
Nodes (582): AbstractAccessLogger, AbstractAsyncAccessLogger, AbstractMatchInfo, AbstractRouter, AbstractStreamWriter, AbstractView, Execute the view handler., Resolve result.      This is the result returned from an AbstractResolver's (+574 more)

### Community 4 - "Community 4"
Cohesion: 0.01
Nodes (941): init(), main(), init(), main(), fetch(), go(), client(), ClientSession (+933 more)

### Community 5 - "Community 5"
Cohesion: 0.01
Nodes (761): time(), ClientTimeout, SSRFConnector, links(), url(), proc(), make_client_request(), BaseConnector (+753 more)

### Community 6 - "Community 6"
Cohesion: 0.01
Nodes (604): Return True if the connection is open., BaseProtocol, BrotliDecompressor, CompressObjArgs, DecompressionBaseHandler, encoding_to_mode(), Base class for decompression handlers., Decompress the given data. (+596 more)

### Community 7 - "Community 7"
Cohesion: 0.01
Nodes (391): BaseDownloadHandler, ClientTLSOptions, CookiesMiddleware, This middleware enables working with sites that need cookies, type(), CoreStats, from_crawler(), Extension for collecting core stats like items scraped and start/finish times (+383 more)

### Community 8 - "Community 8"
Cohesion: 0.01
Nodes (535): Agent, H2Agent, H2ConnectionPool, Close all the HTTP/2 connections and remove them from pool          Returns:, Arguments:             uri - URI obtained directly from request URL, We use the proxy uri instead of uri obtained from request url, ScrapyProxyH2Agent, BaseDownloadHandler (+527 more)

### Community 9 - "Community 9"
Cohesion: 0.01
Nodes (342): ABC, ABCMeta, AssertionError, identity(), BlockingFeedStorage, main(), Contract, CsvItemExporter (+334 more)

### Community 10 - "Community 10"
Cohesion: 0.01
Nodes (416): AbstractStreamWriter, boot(), draw(), drillCluster(), escapeAttr(), escapeHtml(), fetchJson(), findingCard() (+408 more)

### Community 11 - "Community 11"
Cohesion: 0.01
Nodes (285): load_response(), _embed_bpython_shell(), _embed_ipython_shell(), _embed_ptpython_shell(), _embed_standard_shell(), get_shell_embed_func(), Return the first acceptable shell-embed function     from a given list of shell, Start an IPython Shell (+277 more)

### Community 12 - "Community 12"
Cohesion: 0.01
Nodes (334): load_pre_crawler_settings(), BaseHTTPRequestHandler, annotate_clusters(), cluster_leiden(), _cluster_partition(), _coarsen_clusters(), _compact_cluster_ids(), _is_test_node() (+326 more)

### Community 13 - "Community 13"
Cohesion: 0.01
Nodes (465): AnalysisSummary, analyze_top_n(), _attach_findings(), build_request(), _cache_key(), _finding_payload(), _grammar_version(), LLMAnalyzer (+457 more)

### Community 14 - "Community 14"
Cohesion: 0.01
Nodes (385): get_root(), main(), api_logging_middleware(), This is a collection of semi-complete examples that get included into the cookbo, retry_middleware(), ssrf_middleware(), TokenRefresh401Middleware, TokenRefreshExpiryMiddleware (+377 more)

### Community 15 - "Community 15"
Cohesion: 0.02
Nodes (264): background_tasks(), listen_to_valkey(), on_shutdown(), websocket_handler(), display_message(), ConnectionResetError, calculate_timeout_when(), call_later() (+256 more)

### Community 16 - "Community 16"
Cohesion: 0.01
Nodes (172): AioHTTPTestCase, _parallel_asyncio(), Execute a callable over the objects in the given iterable, in parallel,     usi, BasicAuthMiddleware, main(), A protected resource that requires any valid auth., Run a simple test server with basic auth endpoints., Run all basic auth middleware tests. (+164 more)

### Community 17 - "Community 17"
Cohesion: 0.02
Nodes (171): cookies(), parse_cookie_header(), parse_set_cookie_headers(), preserve_morsel_with_coded_value(), Unquote a cookie value.      Vendored from http.cookies._unquote to ensure com, Parse a Cookie header according to RFC 6265 Section 5.4.      Cookie headers c, Parse cookie headers using a vendored version of SimpleCookie parsing.      Th, Preserve a Morsel's coded_value exactly as received from the server.      This (+163 more)

### Community 18 - "Community 18"
Cohesion: 0.03
Nodes (28): curl_to_request_kwargs(), CurlParser, DataAction, _parse_headers_and_cookies(), Convert a cURL command syntax to Request kwargs.      :param str curl_command:, from_response(), from_curl(), _buildresponse() (+20 more)

### Community 19 - "Community 19"
Cohesion: 0.07
Nodes (91): BaseSpiderMiddleware, from_crawler(), process_spider_output(), process_spider_output_async(), Return a processed item from the spider output.          This method is called, Optional base class for spider middlewares.      .. versionadded:: 2.13, Return a processed request from the spider output.          This method is cal, BaseSpiderMiddleware (+83 more)

### Community 20 - "Community 20"
Cohesion: 0.04
Nodes (10): content_disposition(), content_disposition_filename(), parse_content_disposition(), test_attwithfn2231iso_bad(), test_attwithfn2231nbadpct1(), test_attwithfn2231nbadpct2(), test_attwithfn2231utf8_bad(), test_attwithquotedsemicolon() (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.04
Nodes (31): main(), MockDNSResolver, MockDNSServer, Implements twisted.internet.interfaces.IResolver partially, get_script_run_env(), Return a OS environment dict suitable to run scripts shipped with tests., get_script_dir(), Setting TWISTED_REACTOR_ENABLED=False in spider settings is not         current (+23 more)

### Community 22 - "Community 22"
Cohesion: 0.06
Nodes (36): coroutine_test(), inline_callbacks_test(), Mark a test function written in a :func:`twisted.internet.defer.inlineCallbacks`, Mark a test function that returns a coroutine.      * with ``pytest-twisted``, AsyncioSleepSpiderMiddleware, ModernWrapSpider, ModernWrapSpiderMiddleware, ModernWrapSpiderSubclass (+28 more)

### Community 23 - "Community 23"
Cohesion: 0.08
Nodes (23): _pop_command_name(), _append_settings(), create_files(), _proj_path_cached(), The command uses the expected *CrawlerProcess, the spider works., The command uses the expected *CrawlerProcess, the spider fails to use asyncio., The reactor is set via the project default settings (to the asyncio value)., The reactor is set via the command line to the asyncio value.         AsyncCraw (+15 more)

### Community 24 - "Community 24"
Cohesion: 0.06
Nodes (9): _BenchServer, _BenchSpider, Command, A spider that follows all links, Command, Command, Command, ScrapyCommand (+1 more)

### Community 25 - "Community 25"
Cohesion: 0.12
Nodes (5): test_absolute_path(), test_custom_asyncio_loop_enabled_true(), test_runspider_log_short_names(), TestRunSpiderCommand, TestWindowsRunSpiderCommand

### Community 26 - "Community 26"
Cohesion: 0.11
Nodes (15): Directive, Element, General, collect_scrapy_settings_refs(), get_setting_name_and_refid(), _iter_sorted_settings(), make_setting_element(), make_setting_markdown_item() (+7 more)

### Community 27 - "Community 27"
Cohesion: 0.11
Nodes (9): Bz2Plugin, GzipPlugin, LZMAPlugin, Extension for processing data before they are exported to feeds., Uses all the declared plugins to process data first, then writes         the pr, Compresses received data using `gzip <https://en.wikipedia.org/wiki/Gzip>`_., Close the target file along with all the plugins., Compresses received data using `bz2 <https://en.wikipedia.org/wiki/Bzip2>`_. (+1 more)

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
Cohesion: 0.5
Nodes (3): codspeed benchmarks for http writer., Benchmark 100 calls to _serialize_headers., test_serialize_headers()

### Community 33 - "Community 33"
Cohesion: 0.5
Nodes (3): Tests that make sure parts needed for the scrapy-poet stack work., Making sure annotations on all non-abstract callbacks can be resolved., test_callbacks()

### Community 34 - "Community 34"
Cohesion: 0.67
Nodes (1): ExceptionSpider

### Community 35 - "Community 35"
Cohesion: 0.67
Nodes (1): NormalSpider

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): # NOTE: makefile cythonizes all Cython modules

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Scrapy signals  These signals are documented in docs/topics/signals.rst. Pleas

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): Decompress the given data.

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (1): Return True if more output is available by passing b"".

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (1): Create a BasicAuth object from an Authorization HTTP header.

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): Create BasicAuth from url.

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): The value of content part for Content-Type HTTP header.

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (1): The value of charset part for Content-Type HTTP header.

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): The value of Content-Length HTTP header.

### Community 61 - "Community 61"
Cohesion: 1.0
Nodes (1): Create a CallLaterResult from an asyncio TimerHandle.

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (1): Create a CallLaterResult from a Twisted DelayedCall.

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (1): Create a Scrapy project in a temporary directory and return its path.

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (1): Copy a pre-generated Scrapy project into a temporary directory and return its pa

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (1): Add text to the end of the project settings.py.

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (1): Replace custom_settings in the given spider file with the given text.

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 102 - "Community 102"
Cohesion: 1.0
Nodes (1): Precomputed graph summaries used by the local HTTP viewer.

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
- **512 isolated node(s):** `# NOTE: makefile cythonizes all Cython modules`, `Base class for decompression handlers.`, `Decompress the given data.`, `Decompress the given data.`, `Return True if more output is available by passing b"".` (+507 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 29`** (7 nodes): `test_pytest_plugin.py`, `test_aiohttp_client_cls_fixture_custom_client_used()`, `test_aiohttp_client_cls_fixture_factory()`, `test_aiohttp_plugin()`, `test_aiohttp_plugin_async_fixture()`, `test_aiohttp_plugin_async_gen_fixture()`, `test_warning_checks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (3 nodes): `exception.py`, `ExceptionSpider`, `.parse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (3 nodes): `normal.py`, `NormalSpider`, `.parse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (2 nodes): `setup.py`, `# NOTE: makefile cythonizes all Cython modules`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (2 nodes): `signals.py`, `Scrapy signals  These signals are documented in docs/topics/signals.rst. Pleas`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `Decompress the given data.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `Return True if more output is available by passing b"".`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `Create a BasicAuth object from an Authorization HTTP header.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `Create BasicAuth from url.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `The value of content part for Content-Type HTTP header.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `The value of charset part for Content-Type HTTP header.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `The value of Content-Length HTTP header.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (1 nodes): `Create a CallLaterResult from an asyncio TimerHandle.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (1 nodes): `Create a CallLaterResult from a Twisted DelayedCall.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `Create a Scrapy project in a temporary directory and return its path.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `Copy a pre-generated Scrapy project into a temporary directory and return its pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (1 nodes): `Add text to the end of the project settings.py.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `Replace custom_settings in the given spider file with the given text.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 102`** (1 nodes): `Precomputed graph summaries used by the local HTTP viewer.`
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

- **Why does `Crawler` connect `Community 0` to `Community 2`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 12`, `Community 19`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `Application` connect `Community 4` to `Community 1`, `Community 2`, `Community 3`, `Community 11`, `Community 14`, `Community 16`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `ScrapyDeprecationWarning` connect `Community 0` to `Community 2`, `Community 4`, `Community 5`, `Community 7`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 12`, `Community 16`, `Community 22`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 876 inferred relationships involving `Application` (e.g. with `AbstractRouter` and `AbstractMatchInfo`) actually correct?**
  _`Application` has 876 INFERRED edges - model-reasoned connections that need verification._
- **Are the 593 inferred relationships involving `Crawler` (e.g. with `AddonManager` and `This class facilitates loading and storing :ref:`topics-addons`.`) actually correct?**
  _`Crawler` has 593 INFERRED edges - model-reasoned connections that need verification._
- **Are the 569 inferred relationships involving `str` (e.g. with `.__str__()` and `.__str__()`) actually correct?**
  _`str` has 569 INFERRED edges - model-reasoned connections that need verification._
- **Are the 566 inferred relationships involving `url()` (e.g. with `.__init__()` and `._build_url()`) actually correct?**
  _`url()` has 566 INFERRED edges - model-reasoned connections that need verification._