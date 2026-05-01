# Graph Report - analytify  (2026-05-01)

## Corpus Check
- 575 files · ~553,982 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 9380 nodes · 32798 edges · 57 communities detected
- Extraction: 38% EXTRACTED · 62% INFERRED · 0% AMBIGUOUS · INFERRED: 20275 edges (avg confidence: 0.65)
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
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]
- [[_COMMUNITY_Community 99|Community 99]]
- [[_COMMUNITY_Community 100|Community 100]]
- [[_COMMUNITY_Community 101|Community 101]]
- [[_COMMUNITY_Community 102|Community 102]]

## God Nodes (most connected - your core abstractions)
1. `Crawler` - 610 edges
2. `ScrapyDeprecationWarning` - 538 edges
3. `MockServer` - 393 edges
4. `get_crawler()` - 353 edges
5. `test_client_factory()` - 311 edges
6. `NotConfigured` - 308 edges
7. `Item` - 285 edges
8. `Field` - 233 edges
9. `DefaultSpider` - 222 edges
10. `from_crawler()` - 168 edges

## Surprising Connections (you probably didn't know these)
- `Update early settings that do not require a crawler instance, such as SPIDER_MOD` --uses--> `Crawler`  [INFERRED]
  benchmarks\repos\scrapy\scrapy\addons.py → benchmarks\repos\scrapy\scrapy\crawler.py
- `Crawler` --uses--> `Logs a download error message from a spider (typically coming from         the`  [INFERRED]
  benchmarks\repos\scrapy\scrapy\crawler.py → benchmarks\repos\scrapy\scrapy\logformatter.py
- `Crawler` --uses--> `Return a filesystem-safe version of a string ``text``      >>> _path_safe('sim`  [INFERRED]
  benchmarks\repos\scrapy\scrapy\crawler.py → benchmarks\repos\scrapy\scrapy\pqueues.py
- `Crawler` --uses--> `Protocol for downstream queues of ``ScrapyPriorityQueue``.`  [INFERRED]
  benchmarks\repos\scrapy\scrapy\crawler.py → benchmarks\repos\scrapy\scrapy\pqueues.py
- `Crawler` --uses--> `Return a number of requests in a Downloader for a given slot`  [INFERRED]
  benchmarks\repos\scrapy\scrapy\crawler.py → benchmarks\repos\scrapy\scrapy\pqueues.py

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
Nodes (803): AddonManager, This class facilitates loading and storing :ref:`topics-addons`., Load add-ons and configurations from a settings object and apply them., AjaxCrawlMiddleware, _has_ajaxcrawlable_meta(), Handle 'AJAX crawlable' pages marked as crawlable via meta tag., Return True if a page without hash fragment could be "AJAX crawlable"., >>> _has_ajaxcrawlable_meta('<html><head><meta name="fragment"  content="!"/></h (+795 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (745): Creates an Starlette application., Initializes the application.          Parameters:             debug: Boolean, Starlette, AuthCredentials, AuthenticationBackend, AuthenticationError, AuthenticationMiddleware, BaseUser (+737 more)

### Community 2 - "Community 2"
Cohesion: 0.01
Nodes (432): BaseRunSpiderCommand, call(), proc(), closest_scrapy_cfg(), get_config(), get_sources(), init_env(), Get Scrapy config file as a ConfigParser (+424 more)

### Community 3 - "Community 3"
Cohesion: 0.01
Nodes (490): AnalysisSummary, analyze_top_n(), _attach_findings(), build_request(), _cache_key(), _finding_payload(), _grammar_version(), LLMAnalyzer (+482 more)

### Community 4 - "Community 4"
Cohesion: 0.01
Nodes (232): BaseDownloadHandler, CachingHostnameResolverSpider, type(), port(), DataURIDownloadHandler, _lookup_exception_handler(), wrap_app_handling_exceptions(), from_crawler() (+224 more)

### Community 5 - "Community 5"
Cohesion: 0.01
Nodes (223): load_response(), CrawlSpider, CommaSeparatedStrings, iter_errback(), Wrap an iterable calling an errback if an error is caught while     iterating i, NotSupported, Indicates a feature or method is not supported, CSVFeedSpider (+215 more)

### Community 6 - "Community 6"
Cohesion: 0.02
Nodes (267): Agent, BaseDownloadHandler, Optional base class for download handlers., BaseHttpDownloadHandler, BaseMockServer, ClientTLSOptions, CookieJar, CrawlSpider (+259 more)

### Community 7 - "Community 7"
Cohesion: 0.01
Nodes (192): load_pre_crawler_settings(), from_crawler(), NoRequestsSpider, build_component_list(), feed_complete_default_values_from_settings(), feed_process_params_from_cli(), Receives feed export params (from the 'crawl' or 'runspider' commands),     che, Compose a component list from a :ref:`component priority dictionary     <compon (+184 more)

### Community 8 - "Community 8"
Cohesion: 0.02
Nodes (184): ABC, BlockingFeedStorage, CsvItemExporter, from_crawler(), process_request(), DefaultHeaders downloader middleware  See documentation in docs/topics/downloa, BaseItemExporter, CsvItemExporter (+176 more)

### Community 9 - "Community 9"
Cohesion: 0.01
Nodes (210): H2Agent, H2ConnectionPool, Close all the HTTP/2 connections and remove them from pool          Returns:, Arguments:             uri - URI obtained directly from request URL, We use the proxy uri instead of uri obtained from request url, ScrapyProxyH2Agent, ClientFactory, iterate_in_threadpool() (+202 more)

### Community 10 - "Community 10"
Cohesion: 0.01
Nodes (139): CaselessDict, ImmutableMultiDict, MultiDict, CaselessDict, fromkeys(), LocalCache, This module contains data types used by Scrapy which are not included in the Py, Dictionary with a finite number of keys.      Older items expires first. (+131 more)

### Community 11 - "Community 11"
Cohesion: 0.02
Nodes (135): Update early settings that do not require a crawler instance, such as SPIDER_MOD, Call a function in a thread and return its result as a coroutine.      This us, run_in_thread(), is_botocore_available(), Boto/botocore helpers, CaseInsensitiveDict, A dict-like structure that accepts strings or bytes     as keys and allows case, NotConfigured (+127 more)

### Community 12 - "Community 12"
Cohesion: 0.01
Nodes (100): BaseScheduler, _pop_command_name(), CookieJar, _DummyLock, from_crawler(), full_url(), host(), _is_public_domain() (+92 more)

### Community 13 - "Community 13"
Cohesion: 0.03
Nodes (106): ABCMeta, AssertionError, identity(), Contract, CallbackKeywordArgumentsContract, MetadataContract, Contract to check presence of fields in scraped items     @scrapes page_name pa, Contract to set the url of the request (mandatory)     @url http://scrapy.org (+98 more)

### Community 14 - "Community 14"
Cohesion: 0.02
Nodes (74): NoRequestsSpider, coroutine_test(), inline_callbacks_test(), Mark a test function written in a :func:`twisted.internet.defer.inlineCallbacks`, Mark a test function that returns a coroutine.      * with ``pytest-twisted``, NoRequestsSpider, NoRequestsSpider, PeriodicLog (+66 more)

### Community 15 - "Community 15"
Cohesion: 0.02
Nodes (106): as_async_generator(), collect_asyncgen(), Wraps an iterable (sync or async) into an async generator., _embed_bpython_shell(), _embed_ipython_shell(), _embed_ptpython_shell(), _embed_standard_shell(), get_shell_embed_func() (+98 more)

### Community 16 - "Community 16"
Cohesion: 0.08
Nodes (84): BaseSpiderMiddleware, from_crawler(), process_spider_output(), process_spider_output_async(), Return a processed item from the spider output.          This method is called, Optional base class for spider middlewares.      .. versionadded:: 2.13, Return a processed request from the spider output.          This method is cal, BaseSpiderMiddleware (+76 more)

### Community 17 - "Community 17"
Cohesion: 0.03
Nodes (61): _check_max_size(), _DecompressionMaxSizeExceeded, _inflate(), _unbrotli(), _unzstd(), make_response(), gunzip(), gzip_magic_number() (+53 more)

### Community 18 - "Community 18"
Cohesion: 0.03
Nodes (42): _BenchServer, _BenchSpider, Command, A spider that follows all links, Command, TextTestResult, Command, Command (+34 more)

### Community 19 - "Community 19"
Cohesion: 0.04
Nodes (33): main(), MockDNSResolver, MockDNSServer, Implements twisted.internet.interfaces.IResolver partially, async_sleep(), get_script_run_env(), Return a OS environment dict suitable to run scripts shipped with tests., twisted_sleep() (+25 more)

### Community 20 - "Community 20"
Cohesion: 0.07
Nodes (17): from_response(), _get_clickable(), _get_form(), _get_form_url(), _get_inputs(), This module implements the FormRequest class which is a more convenient class (, Find the wanted form element within the given response., Return a list of key-value pairs for the inputs found in the given form. (+9 more)

### Community 21 - "Community 21"
Cohesion: 0.07
Nodes (30): Inventory, Inventory storage and reservation logic., StockItem, Customer, CustomerTier, LineItem, Order, OrderStatus (+22 more)

### Community 22 - "Community 22"
Cohesion: 0.06
Nodes (33): Debugger, Extensions for debugging Scrapy  See documentation in docs/topics/extensions.r, StackTraceDump, format_engine_status(), get_engine_status(), print_engine_status(), Return a report of the current engine status, listen_tcp() (+25 more)

### Community 23 - "Community 23"
Cohesion: 0.08
Nodes (33): test_add_http_if_no_scheme(), test_credentials(), test_default_ports(), test_default_ports_creds_off(), test_default_ports_keep(), test_guess_scheme(), test__is_filesystem_path(), test_noop() (+25 more)

### Community 24 - "Community 24"
Cohesion: 0.11
Nodes (13): decode_robotstxt(), ProtegoRobotParser, PythonRobotParser, RerpRobotParser, RobotParser, BaseRobotParserTest, empty response should equal 'allow all, garbage response should be discarded, equal 'allow all (+5 more)

### Community 25 - "Community 25"
Cohesion: 0.11
Nodes (8): _AsyncBackend, _is_asgi3(), Provide an ASGI3 interface onto an ASGI2 app., _TestClientTransport, _Upgrade, WebSocketTestSession, _WrapASGI2, WebSocketDisconnect

### Community 26 - "Community 26"
Cohesion: 0.12
Nodes (5): test_absolute_path(), test_custom_asyncio_loop_enabled_true(), test_runspider_log_short_names(), TestRunSpiderCommand, TestWindowsRunSpiderCommand

### Community 27 - "Community 27"
Cohesion: 0.09
Nodes (12): Config, Environ, EnvironError, undefined, Holds a string value that should not be revealed in tracebacks etc.     You sho, Secret, We use `assert_type` to test the types returned by Config via mypy., test_config_types() (+4 more)

### Community 28 - "Community 28"
Cohesion: 0.14
Nodes (7): curl_to_request_kwargs(), CurlParser, DataAction, _parse_headers_and_cookies(), Convert a cURL command syntax to Request kwargs.      :param str curl_command:, _test_command(), TestCurlToRequestKwargs

### Community 29 - "Community 29"
Cohesion: 0.11
Nodes (9): Bz2Plugin, GzipPlugin, LZMAPlugin, Extension for processing data before they are exported to feeds., Uses all the declared plugins to process data first, then writes         the pr, Compresses received data using `gzip <https://en.wikipedia.org/wiki/Gzip>`_., Close the target file along with all the plugins., Compresses received data using `bz2 <https://en.wikipedia.org/wiki/Bzip2>`_. (+1 more)

### Community 30 - "Community 30"
Cohesion: 0.18
Nodes (4): _getarg(), Root, Root, Resource

### Community 31 - "Community 31"
Cohesion: 0.23
Nodes (7): Update a deprecated path from an object with its new location, update_classpath(), MyWarning, NewName, SomeBaseClass, TestUpdateClassPath, UserWarning

### Community 32 - "Community 32"
Cohesion: 0.29
Nodes (3): ProcessWithZeroDivisionErrorPipeline, Some pipelines used for testing, ZeroDivisionErrorPipeline

### Community 34 - "Community 34"
Cohesion: 0.4
Nodes (5): MetaPathFinder, install_reactor_import_hook(), Hook that prevents importing :mod:`twisted.internet.reactor`., Prevent importing :mod:`twisted.internet.reactor`., ReactorImportHook

### Community 35 - "Community 35"
Cohesion: 0.5
Nodes (3): Tests that make sure parts needed for the scrapy-poet stack work., Making sure annotations on all non-abstract callbacks can be resolved., test_callbacks()

### Community 36 - "Community 36"
Cohesion: 0.67
Nodes (1): ExceptionSpider

### Community 37 - "Community 37"
Cohesion: 0.67
Nodes (1): NormalSpider

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Scrapy signals  These signals are documented in docs/topics/signals.rst. Pleas

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (1): Create a CallLaterResult from an asyncio TimerHandle.

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (1): Create a CallLaterResult from a Twisted DelayedCall.

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (1): Create a Scrapy project in a temporary directory and return its path.

### Community 56 - "Community 56"
Cohesion: 1.0
Nodes (1): Copy a pre-generated Scrapy project into a temporary directory and return its pa

### Community 57 - "Community 57"
Cohesion: 1.0
Nodes (1): Add text to the end of the project settings.py.

### Community 58 - "Community 58"
Cohesion: 1.0
Nodes (1): Replace custom_settings in the given spider file with the given text.

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (1): Check that the underlying tool is installed and runnable.

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (1): Write centrality and degree metrics back onto graph nodes.

### Community 96 - "Community 96"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 97 - "Community 97"
Cohesion: 1.0
Nodes (1): Return ``node_id -> cluster_id`` using Leiden on an undirected graph.

### Community 98 - "Community 98"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 99 - "Community 99"
Cohesion: 1.0
Nodes (1): Write structured JSONL events and aggregate per-run counters.

### Community 100 - "Community 100"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 101 - "Community 101"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 102 - "Community 102"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **263 isolated node(s):** `Extract setting name from directive index node`, `Must be included after 'sphinx.ext.autodoc'. Fixes unwanted 'alias of' behavior.`, `A spider that generate light requests to measure QPS throughput  usage:`, `Scrapy core exceptions  These exceptions are documented in docs/topics/excepti`, `Indicates a missing configuration situation` (+258 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 36`** (3 nodes): `exception.py`, `ExceptionSpider`, `.parse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (3 nodes): `normal.py`, `NormalSpider`, `.parse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (2 nodes): `signals.py`, `Scrapy signals  These signals are documented in docs/topics/signals.rst. Pleas`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `Create a CallLaterResult from an asyncio TimerHandle.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `Create a CallLaterResult from a Twisted DelayedCall.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (1 nodes): `Create a Scrapy project in a temporary directory and return its path.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (1 nodes): `Copy a pre-generated Scrapy project into a temporary directory and return its pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (1 nodes): `Add text to the end of the project settings.py.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (1 nodes): `Replace custom_settings in the given spider file with the given text.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (1 nodes): `Check that the underlying tool is installed and runnable.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (1 nodes): `Write centrality and degree metrics back onto graph nodes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (1 nodes): `Return ``node_id -> cluster_id`` using Leiden on an undirected graph.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 98`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 99`** (1 nodes): `Write structured JSONL events and aggregate per-run counters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 100`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 101`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 102`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Crawler` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 10`, `Community 11`, `Community 12`, `Community 13`, `Community 15`, `Community 16`, `Community 17`, `Community 22`, `Community 24`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `ScrapyDeprecationWarning` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 12`, `Community 14`, `Community 15`, `Community 23`, `Community 31`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `MockServer` connect `Community 6` to `Community 0`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 8`, `Community 9`, `Community 12`, `Community 13`, `Community 14`, `Community 19`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 593 inferred relationships involving `Crawler` (e.g. with `AddonManager` and `This class facilitates loading and storing :ref:`topics-addons`.`) actually correct?**
  _`Crawler` has 593 INFERRED edges - model-reasoned connections that need verification._
- **Are the 535 inferred relationships involving `ScrapyDeprecationWarning` (e.g. with `Crawler` and `CrawlerRunnerBase`) actually correct?**
  _`ScrapyDeprecationWarning` has 535 INFERRED edges - model-reasoned connections that need verification._
- **Are the 500 inferred relationships involving `Request` (e.g. with `.start_requests()` and `.fetch()`) actually correct?**
  _`Request` has 500 INFERRED edges - model-reasoned connections that need verification._
- **Are the 391 inferred relationships involving `MockServer` (e.g. with `MockServerSpider` and `MetaSpider`) actually correct?**
  _`MockServer` has 391 INFERRED edges - model-reasoned connections that need verification._