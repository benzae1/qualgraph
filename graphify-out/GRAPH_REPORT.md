# Graph Report - analytify  (2026-05-01)

## Corpus Check
- 575 files · ~552,910 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 9356 nodes · 32724 edges · 53 communities detected
- Extraction: 38% EXTRACTED · 62% INFERRED · 0% AMBIGUOUS · INFERRED: 20228 edges (avg confidence: 0.65)
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
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]

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
- `Crawler` --uses--> `Return a number of requests in a Downloader for a given slot`  [INFERRED]
  benchmarks\repos\scrapy\scrapy\crawler.py → benchmarks\repos\scrapy\scrapy\pqueues.py
- `Crawler` --uses--> `Returns the next object to be returned by :meth:`pop`,         but without remo`  [INFERRED]
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
Cohesion: 0.01
Nodes (767): Creates an Starlette application., Initializes the application.          Parameters:             debug: Boolean, Starlette, AuthCredentials, AuthenticationBackend, AuthenticationError, AuthenticationMiddleware, BaseUser (+759 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (629): AddonManager, This class facilitates loading and storing :ref:`topics-addons`., AjaxCrawlMiddleware, _has_ajaxcrawlable_meta(), Handle 'AJAX crawlable' pages marked as crawlable via meta tag., Return True if a page without hash fragment could be "AJAX crawlable"., >>> _has_ajaxcrawlable_meta('<html><head><meta name="fragment"  content="!"/></h, AsyncioLoopingCall (+621 more)

### Community 2 - "Community 2"
Cohesion: 0.01
Nodes (313): BaseDownloadHandler, type(), port(), DataURIDownloadHandler, DefaultHeadersMiddleware, _lookup_exception_handler(), wrap_app_handling_exceptions(), from_crawler() (+305 more)

### Community 3 - "Community 3"
Cohesion: 0.01
Nodes (267): ABCMeta, CaselessDict, load_response(), CrawlSpider, CommaSeparatedStrings, CaseInsensitiveDict, CaselessDict, fromkeys() (+259 more)

### Community 4 - "Community 4"
Cohesion: 0.01
Nodes (299): Update early settings that do not require a crawler instance, such as SPIDER_MOD, Call a function in a thread and return its result as a coroutine.      This us, run_in_thread(), identity(), BlockingFeedStorage, is_botocore_available(), Boto/botocore helpers, CsvItemExporter (+291 more)

### Community 5 - "Community 5"
Cohesion: 0.01
Nodes (308): load_pre_crawler_settings(), Load add-ons and configurations from a settings object and apply them., annotate_clusters(), cluster_leiden(), Leiden community detection for code graphs., Return ``node_id -> cluster_id`` using Leiden on an undirected graph., _to_igraph(), build_component_list() (+300 more)

### Community 6 - "Community 6"
Cohesion: 0.01
Nodes (334): BaseRunSpiderCommand, call(), proc(), _load_context_factory_from_settings(), FloatConvertor, IntegerConvertor, PathConvertor, register_url_convertor() (+326 more)

### Community 7 - "Community 7"
Cohesion: 0.02
Nodes (394): AnalysisSummary, analyze_top_n(), _attach_findings(), build_request(), _cache_key(), _finding_payload(), _grammar_version(), LLMAnalyzer (+386 more)

### Community 8 - "Community 8"
Cohesion: 0.01
Nodes (221): from_crawler(), NoRequestsSpider, CallLaterResult, NoRequestsSpider, NoRequestsSpider, NoRequestsSpider, UppercasePipeline, UrlSpider (+213 more)

### Community 9 - "Community 9"
Cohesion: 0.02
Nodes (276): ABC, Agent, BaseDownloadHandler, from_crawler(), Optional base class for download handlers., BaseHttpDownloadHandler, BaseMockServer, CookieJar (+268 more)

### Community 10 - "Community 10"
Cohesion: 0.01
Nodes (199): H2Agent, H2ConnectionPool, Close all the HTTP/2 connections and remove them from pool          Returns:, Arguments:             uri - URI obtained directly from request URL, We use the proxy uri instead of uri obtained from request url, ScrapyProxyH2Agent, ClientFactory, iterate_in_threadpool() (+191 more)

### Community 11 - "Community 11"
Cohesion: 0.01
Nodes (134): as_async_generator(), collect_asyncgen(), Wraps an iterable (sync or async) into an async generator., _embed_bpython_shell(), _embed_ipython_shell(), _embed_ptpython_shell(), _embed_standard_shell(), get_shell_embed_func() (+126 more)

### Community 12 - "Community 12"
Cohesion: 0.02
Nodes (111): BaseScheduler, _add_edge(), _aliased_import_parts(), build_graph(), _call_name(), _class_base_names(), _class_definition_nodes(), _collect_python_files() (+103 more)

### Community 13 - "Community 13"
Cohesion: 0.02
Nodes (67): CookieJar, CookiesMiddleware, _DummyLock, from_crawler(), full_url(), host(), _is_public_domain(), origin_req_host() (+59 more)

### Community 14 - "Community 14"
Cohesion: 0.04
Nodes (65): AssertionError, Command, TextTestResult, Contract, CallbackKeywordArgumentsContract, MetadataContract, Contract to check presence of fields in scraped items     @scrapes page_name pa, Contract to set the url of the request (mandatory)     @url http://scrapy.org (+57 more)

### Community 15 - "Community 15"
Cohesion: 0.03
Nodes (31): from_response(), _get_clickable(), _get_form(), _get_form_url(), _get_inputs(), This module implements the FormRequest class which is a more convenient class (, Find the wanted form element within the given response., Return a list of key-value pairs for the inputs found in the given form. (+23 more)

### Community 16 - "Community 16"
Cohesion: 0.09
Nodes (83): BaseSpiderMiddleware, process_spider_output(), process_spider_output_async(), Return a processed item from the spider output.          This method is called, Optional base class for spider middlewares.      .. versionadded:: 2.13, Return a processed request from the spider output.          This method is cal, BaseSpiderMiddleware, DefaultReferrerPolicy (+75 more)

### Community 17 - "Community 17"
Cohesion: 0.04
Nodes (40): curl_to_request_kwargs(), CurlParser, DataAction, _parse_headers_and_cookies(), Convert a cURL command syntax to Request kwargs.      :param str curl_command:, Inventory, Inventory storage and reservation logic., StockItem (+32 more)

### Community 18 - "Community 18"
Cohesion: 0.03
Nodes (49): ClientTLSOptions, _check_max_size(), _DecompressionMaxSizeExceeded, _inflate(), _unbrotli(), _unzstd(), gunzip(), gzip_magic_number() (+41 more)

### Community 19 - "Community 19"
Cohesion: 0.03
Nodes (38): _BenchServer, _BenchSpider, Command, A spider that follows all links, Command, Command, Command, extract_domain() (+30 more)

### Community 20 - "Community 20"
Cohesion: 0.04
Nodes (33): main(), MockDNSResolver, MockDNSServer, Implements twisted.internet.interfaces.IResolver partially, async_sleep(), get_script_run_env(), Return a OS environment dict suitable to run scripts shipped with tests., twisted_sleep() (+25 more)

### Community 21 - "Community 21"
Cohesion: 0.05
Nodes (23): TestUtilsMisc, from_crawler(), is_generator_with_return_value(), md5sum(), rel_has_nofollow(), walk_callable(), walk_modules(), walk_modules_iter() (+15 more)

### Community 22 - "Community 22"
Cohesion: 0.06
Nodes (17): make_response(), FTPDownloadHandler, An asynchronous FTP file download handler for scrapy which somehow emulates an h, ReceivedDataProtocol, This module implements a class which returns the appropriate Response class bas, Return the most appropriate Response class from a file name, Try to guess the appropriate response based on the body content.         This m, Guess the most appropriate Response class based on         the given arguments. (+9 more)

### Community 23 - "Community 23"
Cohesion: 0.07
Nodes (32): AsyncioSleepSpiderMiddleware, ModernWrapSpider, ModernWrapSpiderMiddleware, ModernWrapSpiderSubclass, NoOpSpiderMiddleware, test_asyncio_sleep_multiple(), test_asyncio_sleep_single(), test_deprecated_mw_deprecated_spider() (+24 more)

### Community 24 - "Community 24"
Cohesion: 0.08
Nodes (33): test_add_http_if_no_scheme(), test_credentials(), test_default_ports(), test_default_ports_creds_off(), test_default_ports_keep(), test_guess_scheme(), test__is_filesystem_path(), test_noop() (+25 more)

### Community 25 - "Community 25"
Cohesion: 0.08
Nodes (15): Debugger, Extensions for debugging Scrapy  See documentation in docs/topics/extensions.r, StackTraceDump, format_engine_status(), get_engine_status(), print_engine_status(), Return a report of the current engine status, listen_tcp() (+7 more)

### Community 26 - "Community 26"
Cohesion: 0.09
Nodes (12): Config, Environ, EnvironError, undefined, Holds a string value that should not be revealed in tracebacks etc.     You sho, Secret, We use `assert_type` to test the types returned by Config via mypy., test_config_types() (+4 more)

### Community 27 - "Community 27"
Cohesion: 0.13
Nodes (12): Like :func:`send_catch_log` but supports :ref:`asynchronous signal handlers, send_catch_log_deferred(), TestSendCatchLog, TestSendCatchLog2, TestSendCatchLogAsync, TestSendCatchLogAsync2, TestSendCatchLogAsyncAsyncDef, TestSendCatchLogAsyncAsyncio (+4 more)

### Community 28 - "Community 28"
Cohesion: 0.11
Nodes (9): Bz2Plugin, GzipPlugin, LZMAPlugin, Extension for processing data before they are exported to feeds., Uses all the declared plugins to process data first, then writes         the pr, Compresses received data using `gzip <https://en.wikipedia.org/wiki/Gzip>`_., Close the target file along with all the plugins., Compresses received data using `bz2 <https://en.wikipedia.org/wiki/Bzip2>`_. (+1 more)

### Community 29 - "Community 29"
Cohesion: 0.18
Nodes (4): _getarg(), Root, Root, Resource

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (3): ProcessWithZeroDivisionErrorPipeline, Some pipelines used for testing, ZeroDivisionErrorPipeline

### Community 32 - "Community 32"
Cohesion: 0.4
Nodes (4): ftp_makedirs_cwd(), ftp_store_file(), Opens a FTP connection with passed credentials,sets current directory     to th, Set the current directory of the FTP connection given in the ``ftp``     argume

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
Nodes (1): Scrapy signals  These signals are documented in docs/topics/signals.rst. Pleas

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (2): CHANGELOG, README

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (1): Create a CallLaterResult from an asyncio TimerHandle.

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (1): Create a CallLaterResult from a Twisted DelayedCall.

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (1): Create a Scrapy project in a temporary directory and return its path.

### Community 54 - "Community 54"
Cohesion: 1.0
Nodes (1): Copy a pre-generated Scrapy project into a temporary directory and return its pa

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (1): Add text to the end of the project settings.py.

### Community 56 - "Community 56"
Cohesion: 1.0
Nodes (1): Replace custom_settings in the given spider file with the given text.

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (1): Mutate ``graph`` with this annotator's signal.

### Community 90 - "Community 90"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 91 - "Community 91"
Cohesion: 1.0
Nodes (1): Write centrality and degree metrics back onto graph nodes.

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (1): Return ``node_id -> cluster_id`` using Leiden on an undirected graph.

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (1): Write structured JSONL events and aggregate per-run counters.

### Community 96 - "Community 96"
Cohesion: 1.0
Nodes (1): Classify each node's role within its cluster using simple topology.

### Community 97 - "Community 97"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

### Community 98 - "Community 98"
Cohesion: 1.0
Nodes (1): Return the stable node id used by graph building and caching.      Convention: `

## Knowledge Gaps
- **260 isolated node(s):** `Extract setting name from directive index node`, `Must be included after 'sphinx.ext.autodoc'. Fixes unwanted 'alias of' behavior.`, `A spider that generate light requests to measure QPS throughput  usage:`, `Scrapy core exceptions  These exceptions are documented in docs/topics/excepti`, `Indicates a missing configuration situation` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 34`** (3 nodes): `exception.py`, `ExceptionSpider`, `.parse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (3 nodes): `normal.py`, `NormalSpider`, `.parse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (2 nodes): `signals.py`, `Scrapy signals  These signals are documented in docs/topics/signals.rst. Pleas`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (2 nodes): `CHANGELOG`, `README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `Create a CallLaterResult from an asyncio TimerHandle.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `Create a CallLaterResult from a Twisted DelayedCall.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `Create a Scrapy project in a temporary directory and return its path.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (1 nodes): `Copy a pre-generated Scrapy project into a temporary directory and return its pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (1 nodes): `Add text to the end of the project settings.py.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (1 nodes): `Replace custom_settings in the given spider file with the given text.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `Mutate ``graph`` with this annotator's signal.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 90`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (1 nodes): `Write centrality and degree metrics back onto graph nodes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (1 nodes): `Return ``node_id -> cluster_id`` using Leiden on an undirected graph.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (1 nodes): `Write structured JSONL events and aggregate per-run counters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (1 nodes): `Classify each node's role within its cluster using simple topology.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 98`** (1 nodes): `Return the stable node id used by graph building and caching.      Convention: ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Crawler` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 8`, `Community 9`, `Community 11`, `Community 12`, `Community 13`, `Community 14`, `Community 16`, `Community 18`, `Community 21`, `Community 22`, `Community 25`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `ScrapyDeprecationWarning` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 21`, `Community 23`, `Community 24`, `Community 27`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `MockServer` connect `Community 9` to `Community 1`, `Community 2`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 10`, `Community 12`, `Community 14`, `Community 20`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 593 inferred relationships involving `Crawler` (e.g. with `AddonManager` and `This class facilitates loading and storing :ref:`topics-addons`.`) actually correct?**
  _`Crawler` has 593 INFERRED edges - model-reasoned connections that need verification._
- **Are the 535 inferred relationships involving `ScrapyDeprecationWarning` (e.g. with `Crawler` and `CrawlerRunnerBase`) actually correct?**
  _`ScrapyDeprecationWarning` has 535 INFERRED edges - model-reasoned connections that need verification._
- **Are the 500 inferred relationships involving `Request` (e.g. with `.start_requests()` and `.fetch()`) actually correct?**
  _`Request` has 500 INFERRED edges - model-reasoned connections that need verification._
- **Are the 391 inferred relationships involving `MockServer` (e.g. with `MockServerSpider` and `MetaSpider`) actually correct?**
  _`MockServer` has 391 INFERRED edges - model-reasoned connections that need verification._