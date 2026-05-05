# Graph Report - qualgraph  (2026-05-04)

## Corpus Check
- 748 files Â· ~944,165 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 16203 nodes Â· 66157 edges Â· 66 communities detected
- Extraction: 32% EXTRACTED Â· 68% INFERRED Â· 0% AMBIGUOUS Â· INFERRED: 44779 edges (avg confidence: 0.66)
- Token cost: 0 input Â· 0 output

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
  benchmarks\repos\aiohttp\aiohttp\abc.py â†’ benchmarks\repos\aiohttp\aiohttp\cookiejar.py
- `AbstractCookieJar` --uses--> `Remove expired cookies.`  [INFERRED]
  benchmarks\repos\aiohttp\aiohttp\abc.py â†’ benchmarks\repos\aiohttp\aiohttp\cookiejar.py
- `AbstractCookieJar` --uses--> `Returns this jar's cookies filtered by their attributes.`  [INFERRED]
  benchmarks\repos\aiohttp\aiohttp\abc.py â†’ benchmarks\repos\aiohttp\aiohttp\cookiejar.py
- `AbstractCookieJar` --uses--> `Implements a dummy cookie storage.      It can be used with the ClientSession`  [INFERRED]
  benchmarks\repos\aiohttp\aiohttp\abc.py â†’ benchmarks\repos\aiohttp\aiohttp\cookiejar.py
- `AbstractStreamWriter` --uses--> `Test writer that captures written bytes in a buffer.`  [INFERRED]
  benchmarks\repos\aiohttp\aiohttp\abc.py â†’ benchmarks\repos\aiohttp\tests\test_payload.py

## Hyperedges (group relationships)
- **Annotator Plugin Architecture** â€” annotator_base, annotator_pipeline, annotator_bandit, annotator_ruff, annotator_radon [INFERRED 0.80]
- **Quality Signal Aggregation Flow** â€” annotator_pipeline, findings_cross_signal, findings_model, cache_sqlite [INFERRED 0.75]
- **CLI Entry Flow** â€” cli_module, config_module, logging_module, annotator_pipeline [INFERRED 0.80]
- **LLM provider implementations** â€” anthropic_provider, openai_provider, ollama_provider [INFERRED 0.85]
- **Graph construction pipeline** â€” parser_graph_module, resolver_module, builder_module [INFERRED 0.80]
- **Graph analysis output stack** â€” metrics_module, clustering_module, risk_module [INFERRED 0.75]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.0
Nodes (1256): ABCMeta, AddonManager, This class facilitates loading and storing :ref:`topics-addons`., Load add-ons and configurations from a settings object and apply them., Update early settings that do not require a crawler instance, such as SPIDER_MOD, AjaxCrawlMiddleware, _has_ajaxcrawlable_meta(), Handle 'AJAX crawlable' pages marked as crawlable via meta tag. (+1248 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (1230): init(), get_root(), main(), init(), main(), fetch(), go(), client() (+1222 more)

### Community 2 - "Community 2"
Cohesion: 0.01
Nodes (665): ABC, AbstractAccessLogger, AbstractAsyncAccessLogger, AbstractMatchInfo, AbstractRouter, AbstractStreamWriter, AbstractView, Execute the view handler. (+657 more)

### Community 3 - "Community 3"
Cohesion: 0.01
Nodes (821): Creates an Starlette application., Initializes the application.          Parameters:             debug: Boolean, Starlette, AssertionError, AuthCredentials, AuthenticationBackend, AuthenticationError, AuthenticationMiddleware (+813 more)

### Community 4 - "Community 4"
Cohesion: 0.0
Nodes (597): Agent, BaseDownloadHandler, BaseRunSpiderCommand, CachingHostnameResolverSpider, set_zlib_backend(), cleanup_payload_pending_file_closes(), enable_cleanup_closed(), netrc_contents() (+589 more)

### Community 5 - "Community 5"
Cohesion: 0.01
Nodes (778): AbstractCookieJar, AbstractResolver, ResolveResult, AbstractResolver, _BaseRequestContextManager, delete(), ClientConnectionError, ClientConnectionResetError (+770 more)

### Community 6 - "Community 6"
Cohesion: 0.01
Nodes (656): AbstractCookieJar, background_tasks(), listen_to_valkey(), on_shutdown(), time(), ClientTimeout, SSRFConnector, proc() (+648 more)

### Community 7 - "Community 7"
Cohesion: 0.01
Nodes (612): AbstractStreamWriter, boot(), draw(), drillCluster(), drillFile(), escapeAttr(), escapeHtml(), fetchJson() (+604 more)

### Community 8 - "Community 8"
Cohesion: 0.01
Nodes (372): H2Agent, H2ConnectionPool, Close all the HTTP/2 connections and remove them from pool          Returns:, Arguments:             uri - URI obtained directly from request URL, We use the proxy uri instead of uri obtained from request url, ScrapyProxyH2Agent, BaseDownloadHandler, Optional base class for download handlers. (+364 more)

### Community 9 - "Community 9"
Cohesion: 0.01
Nodes (347): BrowserLikePolicyForHTTPS, ClientTLSOptions, BrowserLikeContextFactory, _filter_method_warning(), from_crawler(), _ScrapyClientContextFactory, If the header `key` does not exist, then set it to `value`.         Returns the, make_response() (+339 more)

### Community 10 - "Community 10"
Cohesion: 0.02
Nodes (458): AnalysisSummary, analyze_top_n(), _attach_findings(), build_request(), _cache_key(), _finding_payload(), _grammar_version(), LLMAnalyzer (+450 more)

### Community 11 - "Community 11"
Cohesion: 0.01
Nodes (217): load_response(), NotSupported, Indicates a feature or method is not supported, CSVFeedSpider, This module implements the XMLFeedSpider which is the recommended spider to use, Spider for parsing CSV feeds.     It receives a CSV file in a response; iterate, This method has the same purpose as the one in XMLFeedSpider, This method has the same purpose as the one in XMLFeedSpider (+209 more)

### Community 12 - "Community 12"
Cohesion: 0.01
Nodes (232): BlockingFeedStorage, main(), CsvItemExporter, Debugger, Extensions for debugging Scrapy  See documentation in docs/topics/extensions.r, StackTraceDump, from_crawler(), process_request() (+224 more)

### Community 13 - "Community 13"
Cohesion: 0.01
Nodes (204): load_pre_crawler_settings(), _BenchServer, _BenchSpider, Command, A spider that follows all links, _getarg(), Root, build_component_list() (+196 more)

### Community 14 - "Community 14"
Cohesion: 0.01
Nodes (242): AioHTTPTestCase, from_crawler(), NoRequestsSpider, create_looping_call(), _parallel_asyncio(), Execute a callable over the objects in the given iterable, in parallel,     usi, Create an instance of a looping call class.      This creates an instance of, BaseProtocol (+234 more)

### Community 15 - "Community 15"
Cohesion: 0.01
Nodes (208): BaseHTTPRequestHandler, _gen_default_accept_encoding(), annotate_clusters(), cluster_leiden(), _cluster_partition(), _coarsen_clusters(), _compact_cluster_ids(), _is_test_node() (+200 more)

### Community 16 - "Community 16"
Cohesion: 0.02
Nodes (71): _DummyLock, from_crawler(), full_url(), host(), _is_public_domain(), origin_req_host(), process_request(), process_response() (+63 more)

### Community 17 - "Community 17"
Cohesion: 0.02
Nodes (144): Compress the data and returned the compressed bytes.          Note that flush(, ZLibBackendWrapper, Helpers for WebSocket protocol versions 13 and 8., Websocket masking function.      `mask` is a `bytes` object of length 4; `data, _websocket_mask_python(), ws_ext_gen(), ws_ext_parse(), _xor_table() (+136 more)

### Community 18 - "Community 18"
Cohesion: 0.02
Nodes (48): curl_to_request_kwargs(), CurlParser, DataAction, _parse_headers_and_cookies(), Convert a cURL command syntax to Request kwargs.      :param str curl_command:, FormRequest, from_response(), _get_form() (+40 more)

### Community 19 - "Community 19"
Cohesion: 0.02
Nodes (171): cookies(), parse_cookie_header(), parse_set_cookie_headers(), preserve_morsel_with_coded_value(), Unquote a cookie value.      Vendored from http.cookies._unquote to ensure com, Parse a Cookie header according to RFC 6265 Section 5.4.      Cookie headers c, Parse cookie headers using a vendored version of SimpleCookie parsing.      Th, Preserve a Morsel's coded_value exactly as received from the server.      This (+163 more)

### Community 20 - "Community 20"
Cohesion: 0.07
Nodes (89): BaseSpiderMiddleware, from_crawler(), process_spider_output(), process_spider_output_async(), Return a processed item from the spider output.          This method is called, Optional base class for spider middlewares.      .. versionadded:: 2.13, Return a processed request from the spider output.          This method is cal, BaseSpiderMiddleware (+81 more)

### Community 21 - "Community 21"
Cohesion: 0.04
Nodes (38): DownloadHandlerProtocol, ItemLoader, Tiny order-processing package used as a qualgraph benchmark fixture., A user-friendly abstraction to populate an :ref:`item <topics-items>` with data, Inventory, Inventory storage and reservation logic., StockItem, MailSender (+30 more)

### Community 22 - "Community 22"
Cohesion: 0.03
Nodes (53): Command, TextTestResult, call(), _pop_command_name(), main(), showRandomAnnouncement(), shuffle(), DummyTestCase (+45 more)

### Community 23 - "Community 23"
Cohesion: 0.04
Nodes (11): content_disposition_filename(), filename(), name(), parse_content_disposition(), test_attwithfn2231iso_bad(), test_attwithfn2231nbadpct1(), test_attwithfn2231nbadpct2(), test_attwithfn2231utf8_bad() (+3 more)

### Community 24 - "Community 24"
Cohesion: 0.04
Nodes (33): main(), MockDNSResolver, MockDNSServer, Implements twisted.internet.interfaces.IResolver partially, async_sleep(), get_script_run_env(), Return a OS environment dict suitable to run scripts shipped with tests., twisted_sleep() (+25 more)

### Community 25 - "Community 25"
Cohesion: 0.05
Nodes (35): _get_handler(), get_scrapy_root_handler(), install_scrapy_root_handler(), LogCounterHandler, Return a log handler object according to settings, Fake file-like stream object that redirects writes to a logger instance      T, Record log levels count into a crawler stats, # NOTE: This also handles 'args' being an empty dict, that case doesn't (+27 more)

### Community 26 - "Community 26"
Cohesion: 0.05
Nodes (47): coroutine_test(), inline_callbacks_test(), Mark a test function written in a :func:`twisted.internet.defer.inlineCallbacks`, Mark a test function that returns a coroutine.      * with ``pytest-twisted``, test_asyncio_delayed(), test_deprecated(), test_deprecated_non_generator_exception(), test_deprecated_subclass() (+39 more)

### Community 27 - "Community 27"
Cohesion: 0.12
Nodes (5): test_absolute_path(), test_custom_asyncio_loop_enabled_true(), test_runspider_log_short_names(), TestRunSpiderCommand, TestWindowsRunSpiderCommand

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
  These have â‰¤1 connection - possible missing edges or undocumented components.
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

- **Why does `Crawler` connect `Community 0` to `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 8`, `Community 9`, `Community 11`, `Community 12`, `Community 13`, `Community 14`, `Community 15`, `Community 16`, `Community 20`, `Community 21`, `Community 25`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `Application` connect `Community 1` to `Community 2`, `Community 5`, `Community 11`, `Community 14`, `Community 21`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `ScrapyDeprecationWarning` connect `Community 0` to `Community 1`, `Community 4`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 11`, `Community 12`, `Community 13`, `Community 14`, `Community 15`, `Community 21`, `Community 26`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 876 inferred relationships involving `Application` (e.g. with `AbstractRouter` and `AbstractMatchInfo`) actually correct?**
  _`Application` has 876 INFERRED edges - model-reasoned connections that need verification._
- **Are the 593 inferred relationships involving `Crawler` (e.g. with `AddonManager` and `This class facilitates loading and storing :ref:`topics-addons`.`) actually correct?**
  _`Crawler` has 593 INFERRED edges - model-reasoned connections that need verification._
- **Are the 572 inferred relationships involving `str` (e.g. with `.__str__()` and `.__str__()`) actually correct?**
  _`str` has 572 INFERRED edges - model-reasoned connections that need verification._
- **Are the 566 inferred relationships involving `url()` (e.g. with `.__init__()` and `._build_url()`) actually correct?**
  _`url()` has 566 INFERRED edges - model-reasoned connections that need verification._