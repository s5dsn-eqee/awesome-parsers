# Awesome Parsers [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of maintained parsing libraries, parser generators, and format parsers, organized by technique and tagged by language.

Every entry links to an actively maintained project. Entries that go quiet for more than two years are moved to the Graveyard section rather than deleted, so you can still find them but know what you're getting into. A monthly check flags candidates automatically.

## Contents

- [Parser Combinators](#parser-combinators)
- [PEG Parsers and Generators](#peg-parsers-and-generators)
- [LL and Earley Parsers](#ll-and-earley-parsers)
- [LR / LALR / GLR Generators](#lr--lalr--glr-generators)
- [Incremental and Error-Tolerant Parsers](#incremental-and-error-tolerant-parsers)
- [Lexers and Tokenizers](#lexers-and-tokenizers)
- [Format Parsers](#format-parsers)
  - [JSON](#json)
  - [YAML](#yaml)
  - [TOML](#toml)
  - [XML](#xml)
  - [CSV](#csv)
  - [Markdown](#markdown)
  - [HTML](#html)
  - [CSS](#css)
  - [SQL](#sql)
  - [Dates and Times](#dates-and-times)
  - [URLs and Identifiers](#urls-and-identifiers)
  - [HTTP and Network Protocols](#http-and-network-protocols)
  - [Binary Formats](#binary-formats)
- [Language Parsers](#language-parsers)
- [Learning Resources](#learning-resources)
- [Graveyard](#graveyard)

## Parser Combinators

Build parsers by composing small functions. Best for hand-tuned grammars, good error messages, and when you want to stay in your host language.

- [nom](https://github.com/rust-bakery/nom) `Rust` - Zero-copy, byte-oriented combinators. The default choice for binary and text protocols.
- [winnow](https://github.com/winnow-rs/winnow) `Rust` - A fork of nom focused on ergonomics and debuggability.
- [chumsky](https://codeberg.org/zesterer/chumsky) `Rust` - Combinators with first-class error recovery and pretty diagnostics via ariadne. Development moved from GitHub to Codeberg in 2026.
- [combine](https://github.com/Marwes/combine) `Rust` - Zero-copy combinators with support for partial (streaming) parsing.
- [lexy](https://github.com/foonathan/lexy) `C++` - Compile-time combinators with a grammar DSL and detailed error reporting.
- [Boost.Spirit](https://github.com/boostorg/spirit) `C++` - Long-lived combinator framework (X3 and Qi) where the grammar is written as C++ expression templates.
- [parsec](https://github.com/haskell/parsec) `Haskell` - The original monadic parser combinator library.
- [megaparsec](https://github.com/mrkkrp/megaparsec) `Haskell` - Modern successor to parsec with better error messages and performance.
- [attoparsec](https://github.com/haskell/attoparsec) `Haskell` - Fast combinators for ByteString and Text with incremental input.
- [parsy](https://github.com/python-parsy/parsy) `Python` - Small, readable combinator library with a generator-based syntax.
- [pyparsing](https://github.com/pyparsing/pyparsing) `Python` - Long-lived combinator library with a large ecosystem of examples.
- [parjs](https://github.com/GregRos/parjs) `JavaScript` `TypeScript` - Combinators with detailed failure reasons and soft/hard failure semantics.
- [jparsec](https://github.com/jparsec/jparsec) `Java` - Recursive-descent combinators in the Parsec style.
- [Pidgin](https://github.com/benjamin-hodgson/Pidgin) `C#` - Lightweight, fast combinators with LINQ syntax.
- [fastparse](https://github.com/com-lihaoyi/fastparse) `Scala` - Combinators with macro-generated fast parsers.
- [cats-parse](https://github.com/typelevel/cats-parse) `Scala` - Typelevel combinators that track in the types whether a parser consumes input.
- [better-parse](https://github.com/h0tk3y/better-parse) `Kotlin` - Multiplatform combinators with a grammar DSL and a built-in tokenizer.
- [swift-parsing](https://github.com/pointfreeco/swift-parsing) `Swift` - Combinators from Point-Free that can also print (invert) what they parse.
- [petitparser](https://github.com/petitparser/dart-petitparser) `Dart` - Dynamic combinators that build PEG-style grammars at runtime; also ported to Java, Smalltalk and others.
- [mpc](https://github.com/orangeduck/mpc) `C` - Micro parser combinators for C with a grammar mini-language.
- [mecha](https://github.com/Hejsil/mecha) `Zig` - Parser combinator library for Zig built on comptime.
- [NimbleParsec](https://github.com/dashbitco/nimble_parsec) `Elixir` - Compile-time combinators that generate efficient binary pattern matches.
- [participle](https://github.com/alecthomas/participle) `Go` - Builds parsers from struct tags; closer to a generator than classic combinators.

## PEG Parsers and Generators

Parsing Expression Grammars: ordered choice, unlimited lookahead, no ambiguity. Great for DSLs and config languages. Earley and LL toolkits that are sometimes lumped in with PEG (Lark, nearley, Chevrotain) are in the next section.

- [pest](https://github.com/pest-parser/pest) `Rust` - PEG grammar in a separate file, derive macro generates the parser.
- [rust-peg](https://github.com/kevinmehall/rust-peg) `Rust` - Grammar written inline in Rust via a macro.
- [TatSu](https://github.com/neogeny/TatSu) `Python` - EBNF in, memoizing Packrat PEG parser out.
- [Arpeggio](https://github.com/textX/Arpeggio) `Python` - PEG parser interpreter with Packrat memoization; the engine under textX.
- [parsimonious](https://github.com/erikrose/parsimonious) `Python` - Pure-Python Packrat PEG parser with a concise grammar syntax.
- [pegen](https://github.com/we-like-parsers/pegen) `Python` - The PEG parser generator behind CPython's own parser, available as a standalone package.
- [textX](https://github.com/textX/textX) `Python` - Meta-language for building DSLs with automatic model construction.
- [Peggy](https://github.com/peggyjs/peggy) `JavaScript` - Maintained successor to PEG.js.
- [Ohm](https://github.com/ohmjs/ohm) `JavaScript` - PEG with a separate semantics layer and an interactive grammar editor.
- [pigeon](https://github.com/mna/pigeon) `Go` - PEG grammar to Go code generator.
- [peg](https://github.com/pointlander/peg) `Go` - Generates Go Packrat parsers from PEG grammars.
- [LPeg](https://github.com/roberto-ieru/LPeg) `Lua` - PEGs as first-class pattern values; extremely fast.
- [cpp-peglib](https://github.com/yhirose/cpp-peglib) `C++` - Single-header PEG library with AST generation.
- [PEGTL](https://github.com/taocpp/PEGTL) `C++` - Template-based PEG where the grammar is C++ types.
- [packcc](https://github.com/arithy/packcc) `C` - PEG parser generator producing C code, with Packrat memoization and left-recursion support.
- [Treetop](https://github.com/cjheath/treetop) `Ruby` - PEG grammars compiled to Ruby parsers; the long-standing Ruby choice.

## LL and Earley Parsers

Top-down parsing. LL(k) and ALL(*) generators produce predictable recursive-descent code; Earley parsers accept any context-free grammar, ambiguous ones included, at some cost in speed.

- [ANTLR](https://github.com/antlr/antlr4) `Java` `Python` `JavaScript` `C#` `C++` `Go` - ALL(*) parser generator with runtimes for ten languages and the largest grammar collection in existence.
- [grammars-v4](https://github.com/antlr/grammars-v4) `Grammars` - Community collection of several hundred ANTLR grammars, from SQL dialects to COBOL.
- [JavaCC](https://github.com/javacc/javacc) `Java` - Mature LL(k) generator with a long record in Java tooling; also emits C++ and C# parsers.
- [Chevrotain](https://github.com/Chevrotain/chevrotain) `JavaScript` `TypeScript` - Fast LL(k) parser-building toolkit; no code generation step.
- [Langium](https://github.com/eclipse-langium/langium) `TypeScript` - DSL framework on top of Chevrotain that generates a parser, a language server and VS Code support from one grammar.
- [Xtext](https://github.com/eclipse-xtext/xtext) `Java` - Eclipse framework for DSLs: grammar in, ANTLR-based parser plus editor tooling out.
- [Lark](https://github.com/lark-parser/lark) `Python` - Earley and LALR(1) engines behind an EBNF grammar; handles ambiguous grammars.
- [nearley](https://github.com/kach/nearley) `JavaScript` - Earley parser toolkit for ambiguous grammars.
- [Pyleri](https://github.com/cesbit/pyleri) `Python` - Grammar defined in Python that can export the parser to JavaScript, C, Go and Java.

## LR / LALR / GLR Generators

Classic bottom-up, table-driven parsing. Deterministic, fast, and well understood; GLR handles ambiguity.

- [Bison](https://www.gnu.org/software/bison/) `C` `C++` `Java` - GNU LALR(1)/GLR generator; the yacc successor.
- [byacc](https://github.com/ThomasDickey/byacc-snapshots) `C` - Berkeley Yacc, maintained by Thomas Dickey; a lean, portable yacc without GNU extensions.
- [Lemon](https://sqlite.org/lemon.html) `C` - LALR(1) generator maintained as part of SQLite; thread-safe and re-entrant.
- [LALRPOP](https://github.com/lalrpop/lalrpop) `Rust` - LR(1) generator with readable grammars and good error messages.
- [grmtools](https://github.com/softdevteam/grmtools) `Rust` - Yacc-compatible LR generator with automatic error recovery, plus a lex-compatible lexer.
- [Menhir](https://gitlab.inria.fr/fpottier/menhir) `OCaml` - LR(1) generator with incremental API and error-message tooling.
- [Happy](https://github.com/haskell/happy) `Haskell` - LALR(1) generator used by GHC's own parser.
- [goyacc](https://pkg.go.dev/golang.org/x/tools/cmd/goyacc) `Go` - The yacc port for Go, maintained in the Go tools repository.
- [yecc](https://www.erlang.org/doc/apps/parsetools/yecc.html) `Erlang` - LALR(1) generator from Erlang's parsetools, usually paired with the leex lexer generator; also used from Elixir.

## Incremental and Error-Tolerant Parsers

Designed for editors and tooling, where input changes constantly and is often invalid.

- [tree-sitter](https://github.com/tree-sitter/tree-sitter) `C` - Incremental GLR parser generator with hundreds of community grammars and bindings for most languages. The standard for editor syntax trees.
- [Lezer](https://lezer.codemirror.net/) `JavaScript` - Incremental LR parser system built for CodeMirror 6, with GLR fallback for ambiguity.
- [rowan](https://github.com/rust-analyzer/rowan) `Rust` - Lossless syntax tree library (red/green trees) from rust-analyzer.
- [Roslyn](https://github.com/dotnet/roslyn) `C#` - The .NET compiler platform; full-fidelity, error-tolerant syntax trees for C# and VB.

## Lexers and Tokenizers

- [logos](https://github.com/maciejhirsz/logos) `Rust` - Derive-based lexer generator that compiles to a tight state machine.
- [re2c](https://github.com/skvadrik/re2c) `C` `C++` `Go` `Rust` - Lexer generator producing fast direct-coded scanners.
- [Flex](https://github.com/westes/flex) `C` - The classic fast lexical analyzer generator.
- [RE/flex](https://github.com/Genivia/RE-flex) `C++` - Flex-compatible generator for C++ with Unicode support and indentation anchors.
- [Ragel](https://www.colm.net/open-source/ragel/) `C` `C++` `Go` `Java` - State machine compiler for protocol and lexer code; version 7 is developed at colm.net.
- [JFlex](https://github.com/jflex-de/jflex) `Java` - Lexer generator for Java, used in IntelliJ language plugins and alongside CUP.
- [moo](https://github.com/no-context/moo) `JavaScript` - Optimized tokenizer for use with nearley or standalone.
- [Alex](https://github.com/haskell/alex) `Haskell` - Lexer generator, companion to Happy.
- [sedlex](https://github.com/ocaml-community/sedlex) `OCaml` - Unicode-aware lexer generator implemented as a PPX extension.

## Format Parsers

### JSON

- [simdjson](https://github.com/simdjson/simdjson) `C++` - Parses gigabytes per second using SIMD; bindings for Python, Rust, Go, Node.js and more.
- [yyjson](https://github.com/ibireme/yyjson) `C` - Fast, portable ANSI C library with read, write and mutable-document support.
- [cJSON](https://github.com/DaveGamble/cJSON) `C` - Ultralightweight parser in a single C file, widely used in embedded projects.
- [nlohmann/json](https://github.com/nlohmann/json) `C++` - The most widely used C++ JSON library, designed around STL-like ergonomics rather than raw speed.
- [Glaze](https://github.com/stephenberry/glaze) `C++` - Reflection-based JSON library for C++23 that maps structs directly with no per-type boilerplate.
- [serde_json](https://github.com/serde-rs/json) `Rust` - The de-facto JSON library for Rust, built on serde.
- [simd-json](https://github.com/simd-lite/simd-json) `Rust` - Port of simdjson to Rust with a serde-compatible API.
- [Jackson](https://github.com/FasterXML/jackson-core) `Java` - The standard streaming JSON parser and data-binding stack on the JVM.
- [sonic](https://github.com/bytedance/sonic) `Go` - JIT and SIMD-accelerated JSON for Go.
- [go-json](https://github.com/goccy/go-json) `Go` - Drop-in replacement for encoding/json with much higher throughput.
- [jsonparser](https://github.com/buger/jsonparser) `Go` - Allocation-free JSON access without building a tree.
- [orjson](https://github.com/ijl/orjson) `Python` - Fast JSON library implemented in Rust.
- [msgspec](https://github.com/msgspec/msgspec) `Python` - Fast JSON (and MessagePack) with schema validation through typed structs.

### YAML

- [libyaml](https://github.com/yaml/libyaml) `C` - Reference C parser and emitter, used by many language bindings.
- [PyYAML](https://github.com/yaml/pyyaml) `Python` - The standard Python YAML library; YAML 1.1, with optional libyaml acceleration.
- [ruamel.yaml](https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/) `Python` - YAML 1.2 with round-trip comment preservation.
- [yaml](https://github.com/eemeli/yaml) `JavaScript` - Parses YAML 1.1 and 1.2 into a full document model with comments preserved.
- [js-yaml](https://github.com/nodeca/js-yaml) `JavaScript` - Widely used YAML 1.2 parser and dumper for Node.js and browsers.
- [go-yaml](https://github.com/yaml/go-yaml) `Go` - Community-maintained continuation of the archived go-yaml/yaml package, under the yaml organization.
- [goccy/go-yaml](https://github.com/goccy/go-yaml) `Go` - Independent YAML implementation for Go with better error messages and YAML path queries.
- [SnakeYAML](https://bitbucket.org/snakeyaml/snakeyaml) `Java` - The standard YAML library on the JVM; SnakeYAML Engine covers YAML 1.2.
- [yaml-cpp](https://github.com/jbeder/yaml-cpp) `C++` - YAML 1.2 parser and emitter with a DOM-style API.
- [rapidyaml](https://github.com/biojppm/rapidyaml) `C++` - Very fast YAML parser that works in place on the source buffer.
- [YamlDotNet](https://github.com/aaubry/YamlDotNet) `C#` - YAML parser and serializer for .NET.
- [saphyr](https://github.com/saphyr-rs/saphyr) `Rust` - Maintained continuation of yaml-rust with a YAML 1.2 parser.
- [serde_yaml_ng](https://github.com/acatton/serde-yaml-ng) `Rust` - Conservative fork of the archived serde_yaml for serde users.

### TOML

- [toml++](https://github.com/marzer/tomlplusplus) `C++` - Header-only TOML v1.0 parser and serializer.
- [toml11](https://github.com/ToruNiina/toml11) `C++` - Header-only TOML parser and serializer with detailed error messages and TOML v1.1 support.
- [toml-rs](https://github.com/toml-rs/toml) `Rust` - Used by Cargo itself; toml_edit preserves formatting.
- [tomli](https://github.com/hukkin/tomli) `Python` - The library that became the standard tomllib in Python 3.11; still the backport for older versions.
- [tomlkit](https://github.com/python-poetry/tomlkit) `Python` - Style-preserving TOML parser and editor used by Poetry.
- [BurntSushi/toml](https://github.com/BurntSushi/toml) `Go` - The most widely used TOML library for Go, with struct decoding.
- [go-toml](https://github.com/pelletier/go-toml) `Go` - TOML v1.0 with query and editing support.
- [smol-toml](https://github.com/squirrelchat/smol-toml) `JavaScript` `TypeScript` - Small, fast, spec-compliant TOML 1.0 parser and serializer.
- [Tomlyn](https://github.com/xoofx/Tomlyn) `C#` - TOML parser and writer for .NET with a syntax tree that preserves formatting.
- [tomlj](https://github.com/tomlj/tomlj) `Java` - TOML 1.0 parser for Java with position-aware errors.

### XML

- [libxml2](https://github.com/GNOME/libxml2) `C` - The XML toolkit behind most language bindings (lxml, Nokogiri, PHP, Perl); includes an HTML parser.
- [Expat](https://github.com/libexpat/libexpat) `C` - Stream-oriented (SAX-style) XML parser with a long history in Python, Apache and elsewhere.
- [pugixml](https://github.com/zeux/pugixml) `C++` - Light, fast DOM parser with XPath support.
- [TinyXML-2](https://github.com/leethomason/tinyxml2) `C++` - Small DOM parser aimed at games and embedded use.
- [quick-xml](https://github.com/tafia/quick-xml) `Rust` - Fast pull parser and writer with serde support.
- [roxmltree](https://github.com/RazrFalcon/roxmltree) `Rust` - Read-only DOM built for speed and strictness on untrusted input.
- [lxml](https://github.com/lxml/lxml) `Python` - Bindings to libxml2 and libxslt; fast XML and HTML with XPath and XSLT.
- [fast-xml-parser](https://github.com/NaturalIntelligence/fast-xml-parser) `JavaScript` - Pure JavaScript XML to object parser and builder with validation.
- [Woodstox](https://github.com/FasterXML/woodstox) `Java` - High-performance StAX (pull) parser that underpins Jackson's XML support.

### CSV

- [rust-csv](https://github.com/BurntSushi/rust-csv) `Rust` - Fast, flexible CSV reader and writer with serde integration.
- [PapaParse](https://github.com/mholt/PapaParse) `JavaScript` - Browser and Node.js CSV parser with streaming, workers and header handling.
- [node-csv](https://github.com/adaltas/node-csv) `JavaScript` - Full CSV toolkit for Node.js: parse, stringify, transform and generate, with streaming.
- [CsvHelper](https://github.com/JoshClose/CsvHelper) `C#` - Reads and writes CSV with class mapping; the long-standing .NET choice.
- [Sep](https://github.com/nietras/Sep) `C#` - Modern, SIMD-accelerated CSV parser for .NET.
- [Apache Commons CSV](https://github.com/apache/commons-csv) `Java` - Reads and writes CSV with predefined dialects (Excel, MySQL, RFC 4180).

### Markdown

- [markdown-it](https://github.com/markdown-it/markdown-it) `JavaScript` - CommonMark-compliant, pluggable, fast.
- [marked](https://github.com/markedjs/marked) `JavaScript` - Lightweight compiler with a long history.
- [micromark](https://github.com/micromark/micromark) `JavaScript` - Small, CommonMark-compliant state machine; the engine under remark.
- [remark](https://github.com/remarkjs/remark) `JavaScript` - Markdown as an AST (mdast) with a huge plugin ecosystem.
- [comrak](https://github.com/kivikakk/comrak) `Rust` - CommonMark and GitHub Flavored Markdown; port of cmark-gfm.
- [pulldown-cmark](https://github.com/pulldown-cmark/pulldown-cmark) `Rust` - Pull-parser style, fast and allocation-light.
- [goldmark](https://github.com/yuin/goldmark) `Go` - CommonMark-compliant and extensible; used by Hugo.
- [cmark](https://github.com/commonmark/cmark) `C` - Reference CommonMark implementation.
- [md4c](https://github.com/mity/md4c) `C` - Very fast CommonMark parser used by Qt and many desktop applications.
- [markdown-it-py](https://github.com/executablebooks/markdown-it-py) `Python` - Python port of markdown-it.
- [mistune](https://github.com/lepture/mistune) `Python` - Fast Markdown parser in pure Python with a plugin and renderer API.
- [league/commonmark](https://github.com/thephpleague/commonmark) `PHP` - CommonMark and GFM parser with an extension API; the standard PHP choice.
- [Markdig](https://github.com/xoofx/markdig) `C#` - Fast, extensible CommonMark parser for .NET with a full syntax tree.
- [commonmark-java](https://github.com/commonmark/commonmark-java) `Java` - Java port of the CommonMark reference parser with GFM extensions.
- [flexmark-java](https://github.com/vsch/flexmark-java) `Java` - Highly configurable CommonMark parser that can emulate other Markdown dialects.
- [commonmarker](https://github.com/gjtorikian/commonmarker) `Ruby` - Ruby bindings to comrak, successor to GitHub's cmark-gfm bindings.

### HTML

- [html5ever](https://github.com/servo/html5ever) `Rust` - Spec-compliant HTML5 parser from the Servo project.
- [lol-html](https://github.com/cloudflare/lol-html) `Rust` - Low-latency streaming HTML rewriter from Cloudflare.
- [scraper](https://github.com/rust-scraper/scraper) `Rust` - HTML parsing and CSS selector querying on top of html5ever.
- [parse5](https://github.com/inikulin/parse5) `JavaScript` - Spec-compliant HTML parser used by jsdom and Angular.
- [htmlparser2](https://github.com/fb55/htmlparser2) `JavaScript` - Fast, forgiving streaming HTML and XML parser.
- [cheerio](https://github.com/cheeriojs/cheerio) `JavaScript` - Traversal in the jQuery style over parse5 or htmlparser2.
- [jsoup](https://github.com/jhy/jsoup) `Java` - HTML5 parser with CSS selectors and a cleaner.
- [AngleSharp](https://github.com/AngleSharp/AngleSharp) `C#` - Full W3C DOM implementation for .NET.
- [Html Agility Pack](https://github.com/zzzprojects/html-agility-pack) `C#` - Forgiving HTML parser with XPath and LINQ access.
- [Nokogiri](https://github.com/sparklemotion/nokogiri) `Ruby` - HTML and XML parsing on libxml2 and Gumbo with CSS and XPath queries.
- [selectolax](https://github.com/rushter/selectolax) `Python` - Fast HTML5 parser bound to Modest/Lexbor.
- [x/net/html](https://pkg.go.dev/golang.org/x/net/html) `Go` - Tokenizer and tree builder from the Go team, following the HTML5 spec.
- [Lexbor](https://github.com/lexbor/lexbor) `C` - Fast HTML and CSS engine.

### CSS

- [csstree](https://github.com/csstree/csstree) `JavaScript` - Detailed CSS parser with syntax validation.
- [postcss](https://github.com/postcss/postcss) `JavaScript` - Parses to an AST and drives the largest CSS plugin ecosystem.
- [lightningcss](https://github.com/parcel-bundler/lightningcss) `Rust` `JavaScript` - Extremely fast CSS parser, transformer and minifier.
- [cssparser](https://github.com/servo/rust-cssparser) `Rust` - Servo's CSS tokenizer and parser.
- [tinycss2](https://github.com/Kozea/tinycss2) `Python` - Low-level tokenizer and parser following the CSS Syntax Level 3 spec; used by WeasyPrint.
- [ph-css](https://github.com/phax/ph-css) `Java` - CSS 3 parser and object model for Java.
- [ExCSS](https://github.com/TylerBrinks/ExCSS) `C#` - CSS 3 parser for .NET that produces a stylesheet object model.
- [PHP-CSS-Parser](https://github.com/MyIntervals/PHP-CSS-Parser) `PHP` - Parses CSS into an object model.

### SQL

- [sqlparser-rs](https://github.com/apache/datafusion-sqlparser-rs) `Rust` - Extensible SQL lexer and parser supporting many dialects.
- [sqlglot](https://github.com/tobymao/sqlglot) `Python` - SQL parser, transpiler and optimizer across 20+ dialects.
- [sqlparse](https://github.com/andialbrecht/sqlparse) `Python` - Non-validating SQL parser, formatter and statement splitter.
- [libpg_query](https://github.com/pganalyze/libpg_query) `C` - The real PostgreSQL parser as a library, with bindings for Ruby (pg_query), Python (pglast), Go, Node.js and Rust.
- [JSqlParser](https://github.com/JSQLParser/JSqlParser) `Java` - Parses SQL into a traversable object hierarchy.
- [Apache Calcite](https://github.com/apache/calcite) `Java` - SQL parser and planner framework used by many query engines.
- [node-sql-parser](https://github.com/taozhi8833998/node-sql-parser) `JavaScript` - Parses SQL to AST and back for several dialects.
- [sql-parser-cst](https://github.com/nene/sql-parser-cst) `JavaScript` `TypeScript` - Concrete syntax tree parser that preserves comments and whitespace for several dialects.
- [vitess sqlparser](https://github.com/vitessio/vitess/tree/main/go/vt/sqlparser) `Go` - MySQL-dialect parser from Vitess.
- [TiDB parser](https://github.com/pingcap/tidb/tree/master/pkg/parser) `Go` - MySQL-compatible parser from TiDB, usable on its own.
- [GoogleSQL](https://github.com/google/googlesql) `C++` - Google's SQL parser and analyzer (formerly ZetaSQL) shared by BigQuery and Spanner.

### Dates and Times

- [dateparser](https://github.com/scrapinghub/dateparser) `Python` - Human-readable dates in many languages.
- [dateutil](https://github.com/dateutil/dateutil) `Python` - The standard flexible date parser for Python.
- [chrono](https://github.com/wanasit/chrono) `JavaScript` - Natural language date parser ("next Friday at 3pm").
- [date-fns](https://github.com/date-fns/date-fns) `JavaScript` - Modular date utilities including format-string parsing.
- [when](https://github.com/olebedev/when) `Go` - Natural language date/time parser.
- [go-dateparser](https://github.com/markusmobius/go-dateparser) `Go` - Port of Python's dateparser with its multilingual date formats.
- [Duckling](https://github.com/facebook/duckling) `Haskell` - Rule-based extraction of dates, times, durations and amounts from text in many languages.
- [Recognizers-Text](https://github.com/microsoft/Recognizers-Text) `C#` `JavaScript` `Python` `Java` - Multilingual recognition of dates, numbers, units and more.

### URLs and Identifiers

- [ada](https://github.com/ada-url/ada) `C++` - WHATWG-compliant URL parser used by Node.js; bindings for Rust, Python, Go and more.
- [rust-url](https://github.com/servo/rust-url) `Rust` - WHATWG URL parser from Servo.
- [whatwg-url](https://github.com/jsdom/whatwg-url) `JavaScript` - Reference implementation of the WHATWG URL Standard, used by jsdom.
- [uriparser](https://github.com/uriparser/uriparser) `C` - RFC 3986 URI parser with normalization and reference resolution.
- [libphonenumber](https://github.com/google/libphonenumber) `Java` `C++` `JavaScript` - Phone number parsing and validation.
- [node-semver](https://github.com/npm/node-semver) `JavaScript` - The semantic version parser and range matcher used by npm.

### HTTP and Network Protocols

- [llhttp](https://github.com/nodejs/llhttp) `C` `TypeScript` - HTTP/1.x parser generated from a TypeScript description; the parser inside Node.js.
- [httparse](https://github.com/seanmonstar/httparse) `Rust` - Zero-copy, push-based HTTP/1.x parser used by hyper.
- [picohttpparser](https://github.com/h2o/picohttpparser) `C` - Tiny, fast HTTP/1.x parser from the H2O project.

### Binary Formats

- [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct) `C++` `C#` `Go` `Java` `JavaScript` `Python` `Ruby` - Describe a binary format in YAML and generate parsers for a dozen languages.
- [binrw](https://github.com/jam1garner/binrw) `Rust` - Derive-based binary reading and writing.
- [deku](https://github.com/sharksforarms/deku) `Rust` - Bit-level declarative binary parsing via derive.
- [goblin](https://github.com/m4b/goblin) `Rust` - Cross-platform ELF, PE and Mach-O parser with no_std support.
- [Construct](https://github.com/construct/construct) `Python` - Declarative binary parser and builder.
- [pyelftools](https://github.com/eliben/pyelftools) `Python` - Pure-Python ELF and DWARF parsing.
- [LIEF](https://github.com/lief-project/LIEF) `C++` `Python` - Parse and modify ELF, PE, Mach-O and more.
- [Wuffs](https://github.com/google/wuffs) `C` - Memory-safe language for writing hardened decoders of untrusted file formats.
- [Pattern Language](https://github.com/WerWolv/PatternLanguage) `C++` - The ImHex language for describing binary structures, with a standalone evaluator.
- [Apache Daffodil](https://github.com/apache/daffodil) `Java` `Scala` - Open-source DFDL implementation for describing and parsing fixed text and binary formats.
- [scodec](https://github.com/scodec/scodec) `Scala` - Combinators for binary encoders and decoders with bit-level precision.
- [binary-parser](https://github.com/keichi/binary-parser) `JavaScript` - Declarative binary parser builder for Node.js that generates parsing code at runtime.
- [calamine](https://github.com/tafia/calamine) `Rust` - Pure Rust Excel/OpenDocument spreadsheet reader.

## Language Parsers

Parsers for programming languages, usable as libraries. For editor-grade incremental trees, tree-sitter above has grammars for most of these languages too.

- [SWC](https://github.com/swc-project/swc) `Rust` - Fast JavaScript/TypeScript parser and compiler.
- [oxc](https://github.com/oxc-project/oxc) `Rust` - JavaScript/TypeScript tooling with one of the fastest parsers available.
- [acorn](https://github.com/acornjs/acorn) `JavaScript` - Small, fast ECMAScript parser.
- [espree](https://github.com/eslint/js/tree/main/packages/espree) `JavaScript` - ESLint's parser, built on acorn, now maintained in the eslint/js monorepo.
- [meriyah](https://github.com/meriyah/meriyah) `JavaScript` - Fast, spec-compliant ECMAScript parser with ESTree output.
- [@babel/parser](https://github.com/babel/babel/tree/main/packages/babel-parser) `JavaScript` - Babel's parser with plugin support for proposals.
- [TypeScript](https://github.com/microsoft/TypeScript) `TypeScript` - The TypeScript compiler API, which is also the reference parser for the language.
- [Boa](https://github.com/boa-dev/boa) `Rust` - JavaScript engine with a standalone parser crate.
- [syn](https://github.com/dtolnay/syn) `Rust` - Parses Rust token streams into a syntax tree; the backbone of proc macros.
- [JavaParser](https://github.com/javaparser/javaparser) `Java` - Parse, analyze, transform and generate Java code.
- [Spoon](https://github.com/INRIA/spoon) `Java` - Source code analysis and transformation for Java.
- [scalameta](https://github.com/scalameta/scalameta) `Scala` - Parsers and syntax trees for Scala, used by Scalafmt and Metals.
- [Prism](https://github.com/ruby/prism) `C` `Ruby` - Ruby's official error-tolerant parser, shared by CRuby, JRuby and TruffleRuby.
- [swift-syntax](https://github.com/swiftlang/swift-syntax) `Swift` - Apple's library for parsing, inspecting and rewriting Swift source.
- [libclang](https://clang.llvm.org/docs/LibClang.html) `C` `C++` - Stable C interface to Clang for parsing C, C++ and Objective-C.
- [pycparser](https://github.com/eliben/pycparser) `Python` - Complete C99 parser in pure Python; used by cffi.
- [PHP-Parser](https://github.com/nikic/PHP-Parser) `PHP` - PHP parser written in PHP, used by many static analyzers.
- [go/parser](https://pkg.go.dev/go/parser) `Go` - Go's own parser from the standard library.
- [ast](https://docs.python.org/3/library/ast.html) `Python` - Python's standard-library parser; see also [libcst](https://github.com/Instagram/LibCST) for lossless trees.
- [parso](https://github.com/davidhalter/parso) `Python` - Error-tolerant Python parser with round-trip support; powers Jedi.
- [JuliaSyntax.jl](https://github.com/JuliaLang/JuliaSyntax.jl) `Julia` - Julia's reference parser with precise source locations and error recovery.
- [mvdan/sh](https://github.com/mvdan/sh) `Go` - Shell parser, formatter and interpreter for POSIX shell, Bash and mksh.
- [HCL](https://github.com/hashicorp/hcl) `Go` - HashiCorp Configuration Language parser used by Terraform and friends.
- [wasm-tools](https://github.com/bytecodealliance/wasm-tools) `Rust` - Bytecode Alliance tooling including wasmparser, the standard WebAssembly binary parser.
- [slang](https://github.com/MikePopoloski/slang) `C++` - Fast, complete SystemVerilog parser and analysis library.
- [Verible](https://github.com/chipsalliance/verible) `C++` - SystemVerilog parser, linter and formatter.

## Learning Resources

- [Crafting Interpreters](https://github.com/munificent/craftinginterpreters) - Free book covering scanning, recursive-descent parsing and more, in Java and C.
- [A Compiler Writing Journey](https://github.com/DoctorWkt/acwj) - Incremental, hands-on compiler construction in C.
- [Parsing Techniques: A Practical Guide (Grune & Jacobs)](https://dickgrune.com/Books/PTAPG_2nd_Edition/) - The reference text on parsing algorithms.
- [Parsing Expression Grammars (Ford, 2004)](https://bford.info/pub/lang/peg.pdf) - The original PEG paper.
- [Which Parsing Approach?](https://tratt.net/laurie/blog/2020/which_parsing_approach.html) - Laurence Tratt weighs recursive descent, PEG, LR and generalized parsing, and makes the case for LR.
- [Simple but Powerful Pratt Parsing](https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html) - Operator-precedence parsing explained with a small Rust implementation.
- [Pratt Parsers: Expression Parsing Made Easy](https://journal.stuffwithstuff.com/2011/03/19/pratt-parsers-expression-parsing-made-easy/) - The classic walkthrough of Pratt parsing, in Java.
- [Resilient LL Parsing Tutorial](https://matklad.github.io/2023/05/21/resilient-ll-parsing-tutorial.html) - Error-tolerant hand-written parsing, by the rust-analyzer author.
- [Earley Parsing Explained](https://loup-vaillant.fr/tutorials/earley-parsing/) - Tutorial series that builds an Earley parser step by step.
- [Parsing: a timeline](https://jeffreykegler.github.io/personal/timeline_v3) - History of parsing theory from the 1960s to today, by the Marpa author.
- [Writing a PEG parser for fun and profit](https://www.youtube.com/watch?v=QppWTvh7_sI) - Guido van Rossum on the design of CPython's PEG parser.
- [Tree-sitter: a new parsing system for programming tools](https://www.youtube.com/watch?v=Jes3bD6P0To) - Max Brunsfeld's Strange Loop talk on incremental parsing for editors.
- [Parsing JSON is a Minefield](https://github.com/nst/JSONTestSuite) - Test suite and write-up showing how differently JSON parsers handle edge cases.
- [AST Explorer](https://astexplorer.net/) - Explore the ASTs produced by dozens of parsers in the browser.

## Graveyard

Projects that were once widely used but are archived or have had no activity for more than two years. Listed so you recognize them, not so you adopt them. Quiet is not the same as broken: several of these still work fine, but you will be on your own.

- [PEG.js](https://github.com/pegjs/pegjs) `JavaScript` - Superseded by Peggy.
- [PLY](https://github.com/dabeaz/ply) `Python` - Declared finished by its author; Lark covers the same ground.
- [SLY](https://github.com/dabeaz/sly) `Python` - PLY's successor, archived by its author in 2025.
- [Jison](https://github.com/zaach/jison) `JavaScript` - Bison-style generator with no activity since 2020; Peggy or Chevrotain for new work.
- [parsimmon](https://github.com/jneen/parsimmon) `JavaScript` - Monadic combinators with no activity since 2023; parjs is the maintained alternative.
- [FParsec](https://github.com/stephan-tolksdorf/fparsec) `F#` - The reference F# combinator library; still works, but no activity since 2022.
- [Sprache](https://github.com/sprache/Sprache) `C#` - LINQ-style combinators with no activity since 2021; Pidgin is the maintained alternative.
- [angstrom](https://github.com/inhabitedtype/angstrom) `OCaml` - Fast incremental combinators with no releases or commits since 2024.
- [Parsedown](https://github.com/erusev/parsedown) `PHP` - Largely dormant; consider league/commonmark.
- [Blackfriday](https://github.com/russross/blackfriday) `Go` - Once the default Go Markdown library; goldmark replaced it in Hugo and elsewhere.
- [Babylon](https://github.com/babel/babylon) `JavaScript` - Merged into Babel as @babel/parser.
- [esprima](https://github.com/jquery/esprima) `JavaScript` - The ECMAScript parser many others descend from; no activity since 2021. Use acorn or meriyah.
- [Semantic](https://github.com/github/semantic) `Haskell` - GitHub's multi-language code analysis library on tree-sitter, now archived.
- [serde_yaml](https://github.com/dtolnay/serde-yaml) `Rust` - Archived by its author in 2024, and its serde_yml fork was archived too; use serde_yaml_ng or saphyr.
- [strictyaml](https://github.com/crdoconnor/strictyaml) `Python` - Restricted YAML subset with no activity since 2023.
- [go-yaml/yaml](https://github.com/go-yaml/yaml) `Go` - The original Go YAML package, now archived; the yaml/go-yaml fork continues it.
- [json-iterator](https://github.com/json-iterator/go) `Go` `Java` - Archived; sonic or go-json for Go, Jackson for Java.
- [jsmn](https://github.com/zserge/jsmn) `C` - Minimal JSON tokenizer with no activity since 2021; cJSON or yyjson instead.
- [gumbo-parser](https://github.com/google/gumbo-parser) `C` - Google's HTML5 parser, archived; Lexbor is the C alternative.
- [MyHTML](https://github.com/lexborisov/myhtml) `C` - Deprecated by its author in favor of Lexbor.

## Contributing

Contributions welcome. Read [contributing.md](contributing.md) first; it covers the entry format, the 24-month activity rule, where things go, and how the Graveyard works. In short: one entry per pull request, canonical repository link, language tag, one factual sentence.
