'use strict'

/**/

// Dependencies used outside of honeycomb
import bole from '@entropic/bole'
import isDev from 'are-we-dev'

export { bole, isDev }

void ``

import { Writable } from 'stream'
// We continue to support beelines...
import beeline from 'honeycomb-beeline'

// ...but are migrating to OpenTelemetry:
import * as grpc from '@grpc/grpc-js'
import * as otel from '@opentelemetry/api'
import * as otelCore from '@opentelemetry/core'
import * as otlpHttp from '@opentelemetry/exporter-trace-otlp-http'
import * as otlpProto from '@opentelemetry/exporter-trace-otlp-proto'
import * as otlpGrpc from '@opentelemetry/exporter-trace-otlp-grpc'
import * as otelResources from '@opentelemetry/resources'
import { NodeSDK as OtelSDK } from '@opentelemetry/sdk-node'
import * as otelTraceBase from '@opentelemetry/sdk-trace-base'
import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node'
import * as otelSemanticConventions from '@opentelemetry/semantic-conventions'

// We include node core instrumentation, as well as redis
// and postgres instrumentation if those respective features
// are enabled.
//
// Some instrumentation that is NOT included, because boltzmann
// doesn't support the technology:
//
// * @opentelemetry/instrumentation-grpc
// * @opentelemetry/instrumentation-graphql
//
// Some packages which, to our knowledge, don't have available
// instrumentations:
//
// * undici
//
import { Instrumentation as OtelInstrumentation } from '@opentelemetry/instrumentation'
import { DnsInstrumentation as OtelDnsInstrumentation } from '@opentelemetry/instrumentation-dns'
import { HttpInstrumentation as OtelHttpInstrumentation } from '@opentelemetry/instrumentation-http'

void ``;
import { RedisInstrumentation as OtelRedisInstrumentation } from '@opentelemetry/instrumentation-redis'
void ``

void ``
import { PgInstrumentation as OtelPgInstrumentation } from '@opentelemetry/instrumentation-pg'
void ``

class HoneycombError extends Error {
}

// A diagnostic logger for OpenTelemetry. To log at a sensible level,
// call otel.diag.verbose.
class HoneycombDiagLogger implements otel.DiagLogger {
  public logger?: typeof bole
  private _stream: Writable

  // OpenTelemetry's diagnostic logger has one more log level than bole - ie,
  // verbose.
  //
  // For more details on how to treat each log level, see:
  // https://github.com/open-telemetry/opentelemetry-js-api/blob/main/src/diag/consoleLogger.ts#L60

  // Log errors that caused an unexpected failure
  error(message: string, ...args: unknown[]): void {
    this._log('error', message, args)
  }
  // Log warnings that aren't show-stopping but should REALLY be looked at
  warn(message: string, ...args: unknown[]): void {
    this._log('warn', message, args)
  }
  // Log info if you want to be REALLY LOUD for some reason - you probably
  // don't want to use this!
  info(message: string, ...args: unknown[]): void {
    this._log('info', message, args)
  }
  // Log details that could be useful for identifying what went wrong, but
  // aren't the thing that went wrong itself - treat this as you would info
  // logging normally
  debug(message: string, ...args: unknown[]): void {
    this._log('debug', message, args)
  }
  // Log fine-grained details that are mostly going to be useful to those
  // adding new OpenTelemetry related features to boltzmann - treat this like
  // you would debug level logging normally
  verbose(message: string, ...args: unknown[]): void {
    this._log('debug', `VERBOSE: ${message}`, args)
  }

  // Ideally we would log to a bole logger. However, logger setup happens
  // relatively late - in the log middleware - and it's very likely that such
  // a log won't be in-place when we stand up the middleware stack! Therefore,
  // we do log to bole if it's set in the middleware but will fall back to
  // good ol' fashioned JSON.stringify if need be.
  constructor() {
    this._stream = process.stdout

    // So log messages roughly match what's output by the bole in dev mode :^)
    if (isDev()) {
      const pretty = require('bistre')({ time: true })
      this._stream = pretty.pipe(this._stream)
    }
  }

  private _log(level: 'error' | 'warn' | 'info' | 'debug', message: string, args: unknown[]): void {
    let isSelfTest = false
    void ``
    isSelfTest = true
    void ``
    if (isSelfTest) {
      return
    }

    // Log to bole if we have it
    if (this.logger) {
      this.logger[level](message, ...args)
      return
    }

    const line: any = {
      time: (new Date()).toISOString(),
      level,
      name: 'telemetrence:honeycomb',
      message,
      args
    }

    try {
      // are the args JSON-serializable?
      this._writeLine(JSON.stringify(line))
      // SURVEY SAYS...
    } catch (_) {
      // ...ok, make it a string as a fallback
      line.args = require('util').format('%o', line.args)
      this._writeLine(JSON.stringify(line))
    }
  }

  private _writeLine(line: string): void {
      this._stream.write(Buffer.from(line + '\n'))
  }

}

// We only do OpenTelemetry logging if boltzmann's main log level is debug
const _diagLogger = new HoneycombDiagLogger()

if (!process.env.LOG_LEVEL || process.env.LOG_LEVEL === 'debug') {
  otel.diag.setLogger(_diagLogger, otelCore.getEnv().OTEL_LOG_LEVEL)
}

type HoneycombOTLPHeaders = {
  [s: string]: string
}

// Arguments passed to Honeycomb's constructor
interface HoneycombOptions {
  serviceName: string
  // When true, treat Honeycomb instrumentation as
  // disabled
  disable?: boolean

  // When true, Do Otel
  otel?: boolean

  // The Honeycomb write key and dataset
  writeKey?: string | null
  dataset?: string | null

  // Tunables, etc.
  sampleRate?: number
  otlpProtocol?: string
}

// Whether or not otel, beelines and honeycomb are enabled
interface HoneycombFeatures {
  honeycomb: boolean
  beeline: boolean
  otel: boolean
}

// There's a lot of plumbing that happens when setting up
// OpenTelemetry. In order to fully initialize it, we need
// to instantiate all of these object types.
//
// They're exposed on the Honeycomb class but in a nested
// namespace.
interface OtelFactories {
  headers: (writeKey: string | null, dataset: string | null) => HoneycombOTLPHeaders
  resource: (serviceName: string) => otelResources.Resource
  tracerProvider: (
    resource: otelResources.Resource,
  ) => NodeTracerProvider
  spanExporter: (protocol: string, headers: HoneycombOTLPHeaders) => otelTraceBase.SpanExporter
  spanProcessor: (spanExporter: otelTraceBase.SpanExporter) => otelTraceBase.SpanProcessor
  instrumentations: () => OtelInstrumentation[]
  sdk: (
    resource: otelResources.Resource,
    instrumentations: OtelInstrumentation[]
  ) => OtelSDK
}

const defaultOtelFactories: OtelFactories = {
  headers (writeKey: string | null, dataset: string | null): HoneycombOTLPHeaders {
    let headers: HoneycombOTLPHeaders = {}
    if (writeKey) {
      headers['x-honeycomb-team'] = writeKey
    }
    if (dataset) {
      headers['x-honeycomb-dataset'] = dataset
    }
    return headers
  },

  resource (serviceName: string): otelResources.Resource {
    return new otelResources.Resource({
      [otelSemanticConventions.SemanticResourceAttributes.SERVICE_NAME]: serviceName
    })
  },

  // A tracer provider is effectively a Tracer factory and is used to power
  // the otel.getTrace API
  tracerProvider (resource: otelResources.Resource): NodeTracerProvider {
    return new NodeTracerProvider({ resource })
  },

  // There are three different OTLP span exporter classes - one for grpc, one
  // for http/protobuf and one for http/json - this will return the appropriate
  // one for the configured protocol.
  spanExporter (protocol: string, headers: HoneycombOTLPHeaders): otelTraceBase.SpanExporter {
    // Instead of subclassing each implementation, monkey patch the send
    // method on whichever instance we create
    function patchSend(exporter: any) {
      const send = exporter.send

      exporter.send = function(
        objects: otelTraceBase.ReadableSpan[],
        onSuccess: () => void,
        // This error is actually an Error subtype which corresponds 1:1 with
        // the OTLPTraceExporter class being instrumented, but making this a
        // proper generic type is hard - it's fine!
        onError: (error: any) => void
      ) {
        otel.diag.debug(`sending ${objects.length} spans to ${this.url}`)
        send.call(this,
          objects,
          () => {
            otel.diag.debug(`successfully send ${objects.length} spans to ${this.url}`)
            return onSuccess()
          },
          (error: any) => {
            otel.diag.debug(`error while sending ${objects.length} spans: ${error}`)
            return onError(error)
          }
        )
      }
    }

    if (protocol === 'grpc') {
      const metadata = new grpc.Metadata()
      for (let [key, value] of Object.entries(headers)) {
        metadata.set(key, value)
      }
      const credentials = grpc.credentials.createSsl()

      const exporter = new otlpGrpc.OTLPTraceExporter({
        credentials,
        metadata
      })

      patchSend(exporter)

      return exporter
    }

    if (protocol === 'http/json') {
      otel.diag.warn(
        "Honeycomb doesn't support the http/json OTLP protocol - but if you say so"
      )
      const exporter = new otlpHttp.OTLPTraceExporter({
        headers
      })

      patchSend(exporter)

      return exporter
    }

    if (protocol !== 'http/protobuf') {
      otel.diag.warn(
        `Unknown OTLP protocol ${protocol} - using http/protobuf instead`
      )
    }

    const exporter = new otlpProto.OTLPTraceExporter({
      headers
    })

    patchSend(exporter)

    return exporter
  },

  // Process spans, using the supplied trace exporter to
  // do the actual exporting.
  spanProcessor (spanExporter: otelTraceBase.SpanExporter): otelTraceBase.SpanProcessor {
    // There's a bug in the trace base library where the SimpleSpanProcessor doesn't
    // actually conform to the SpanProcessor interface! Luckily this difference
    // comes from not including an optional argument in the type signature and is
    // safe to cast.

    return <otelTraceBase.SpanProcessor>(new otelTraceBase.SimpleSpanProcessor(spanExporter))
  },

  instrumentations () {
    // Any paths we add here will get no traces whatsoever. This is
    // appropriate for the ping route, which should never trace.
    const ignoreIncomingPaths = [
      '/monitor/ping'
    ]

    // OpenTelemetry attempts to auto-collect GCE metadata, causing traces
    // we don't care about. We do our best to ignore them by independently
    // calculating which endpoints it's going to try to call.
    //
    // See: https://github.com/googleapis/gcp-metadata/blob/main/src/index.ts#L26-L44
    const ignoreOutgoingUrls = [
      /^https?:\/\/169\.254\.169\.254/,
      /^https?:\/\/metadata\.google\.internal/,
    ]
    let gceBase: string | null = process.env.GCE_METADATA_IP || process.env.GCE_METADATA_HOST || null
    if (gceBase) {
      if (!/^https?:\/\//.test(gceBase)) {
        gceBase = `http://${gceBase}`;
      }
      ignoreOutgoingUrls.push(new RegExp(`^${gceBase}`))
    }

    let is: OtelInstrumentation[] = [
      new OtelDnsInstrumentation({}),
      // NOTE: This instrumentation creates the default "trace" span and manages
      // header propagation! See the honeycomb trace middleware for more
      // details.
      new OtelHttpInstrumentation({
        // TODO: These fields are expected to become deprecated in the
        // near future...
        ignoreIncomingPaths,
        ignoreOutgoingUrls
      }),
    ]

    void ``
    is.push(new OtelRedisInstrumentation({}))
    void ``

    void ``
    is.push(new OtelPgInstrumentation({}))
    void ``

    return is
  },

  // The SDK will take a service name, instrumentations
  // and a trace exporter and give us a stateful singleton.
  // This is that singleton!
  sdk (
    resource: otelResources.Resource,
    instrumentations: OtelInstrumentation[]
  ): OtelSDK {
    return new OtelSDK({
      resource,
      instrumentations
    })
  }
}

// For testing purposes, it can be beneficial to override how objects in
// OpenTelemetry initialization are created. The Honeycomb class allows for
// passing overrides into its constructor. This is an INTERNAL API - unless
// you're writing honeycomb-related unit tests, it won't be relevant to you.
interface OtelFactoryOverrides {
  headers?: (writeKey: string | null, dataset: string | null) => HoneycombOTLPHeaders
  resource?: (serviceName: string) => otelResources.Resource
  tracerProvider?: (
    resource: otelResources.Resource,
  ) => NodeTracerProvider
  spanExporter?: (protocol: string, headers: HoneycombOTLPHeaders) => otelTraceBase.SpanExporter
  spanProcessor?: (spanExporter: otelTraceBase.SpanExporter) => otelTraceBase.SpanProcessor
  instrumentations?: () => OtelInstrumentation[]
  sdk?: (
    resource: otelResources.Resource,
    instrumentations: OtelInstrumentation[],
  ) => OtelSDK;
}

// Let's GOOOOOOO
class Honeycomb {
  public options: HoneycombOptions
  public features: HoneycombFeatures
  public factories: OtelFactories

  public tracerProvider: NodeTracerProvider | null
  public spanExporter: otelTraceBase.SpanExporter | null
  public spanProcessor: otelTraceBase.SpanProcessor | null
  public instrumentations: OtelInstrumentation[] | null
  public sdk: OtelSDK | null

  public initialized: boolean
  public started: boolean

  private _logger: typeof bole | null

  constructor(
    options: HoneycombOptions,
    overrides: OtelFactoryOverrides = {}
  ) {
    this.options = options
    this.features = {
      honeycomb: !options.disable,
      beeline: !options.disable && !options.otel,
      otel: options.otel || false
    }
    this.initialized = false
    this.started = false

    this.tracerProvider = null
    this.spanExporter = null
    this.spanProcessor = null
    this.instrumentations = null
    this.sdk = null

    this.factories = {
      ...defaultOtelFactories,
      ...(overrides || {})
    }

    this._logger = null
  }

  get tracer (): otel.Tracer {
    return otel.trace.getTracer('telemetrence', '')
  }

  // We (usually) load options from the environment. Unlike with Options,
  // we do a lot of feature detection here.
  public static fromEnv(
    env: typeof process.env = process.env,
    overrides: OtelFactoryOverrides = {}
  ): Honeycomb {
    return new Honeycomb(
      Honeycomb.parseEnv(env),
      overrides
    )
  }

  public static parseEnv(env: typeof process.env = process.env): HoneycombOptions {
    // For beelines, if we don't have HONEYCOMB_WRITEKEY there isn't much we
    // can do...
    let disable = !env.HONEYCOMB_WRITEKEY

    // Beelines should pick these up automatically, but we'll need them to
    // configure default OTLP headers
    const writeKey = env.HONEYCOMB_WRITEKEY || null
    const dataset = env.HONEYCOMB_DATASET || null

    // OpenTelemetry is configured with a huge pile of `OTEL_*` environment
    // variables. If any of them are defined, we'll use OpenTelemetry instead
    // of beelines. Typically one would configure OTEL_EXPORTER_OTLP_ENDPOINT
    // to point to either api.honeycomb.io or your local refinery, but this
    // will flag on OTEL_ENABLED=1 as well if you want to use all the
    // defaults.
    //
    // For a broad overview of common variables, see:
    // https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/sdk-environment-variables.md
    //
    // For a list of variables the OTLP exporter respects, see:
    // https://opentelemetry.io/docs/reference/specification/protocol/exporter/
    const isOtel: boolean = Object.entries(env).some(([name, value]) => {
      return name.startsWith('OTEL_') && value && value.length;
    });

    // OpenTelemetry can optionally load the honeycomb headers from the
    // OTEL_EXPORTER_OTLP_HEADERS and/or OTEL_EXPORTER_OTLP_TRACE_HEADERS
    // environment variables, so having HONEYCOMB_WRITEKEY be falsey is
    // potentially OK. This strategy also allows people to use the
    // honeycomb tracing for non-honeycomb use cases.
    if (isOtel) {
      disable = false
    }

    // This sample rate is for beeline only - to set the OpenTelemetry sample
    // rate, set OTEL_TRACES_SAMPLER=parentbased_traceidratio and
    // OTEL_TRACES_SAMPLER_ARG=${SOME_NUMBER}. Note that beeline defines
    // sample rate as total/sampled, but OpenTelemetry defines it as
    // sampled/total!
    let sampleRate: number = Number(env.HONEYCOMB_SAMPLE_RATE || 1)

    if (isNaN(sampleRate)) {
      sampleRate = 1
    }

    // OTLP is supposed to be configured with this environment variable, but
    // the OpenTelemetry SDKs leave this as a some-assembly-required job.
    // We default to 'http/protobuf' because it's well-supported by both
    // Honeycomb and AWS load balancers and because it's relatively snappy.
    //
    // For more information on how this is configured, see:
    // https://opentelemetry.io/docs/reference/specification/protocol/exporter/#specify-protocol
    const otlpProtocol = env.OTEL_EXPORTER_OTLP_PROTOCOL || env.OTEL_EXPORTER_OTLP_TRACES_PROTOCOL || 'http/protobuf'

    // The service name logic is VERY similar to what's in prelude.ts,
    // except that OTEL_SERVICE_NAME takes precedence if defined
    const serviceName: string = ((): string => {
      try {
        return env.OTEL_SERVICE_NAME || env.SERVICE_NAME || require('./package.json').name.split('/').pop()
      } catch (err) {
        return 'telemetrence'
      }
    })()

    return {
      serviceName,
      disable,
      otel: isOtel,
      writeKey,
      dataset,
      sampleRate,
      otlpProtocol
    }
  }

  // Initialize Honeycomb! Stands up the otel node SDK if enabled,
  // otherwise sets up the beeline library.
  // This needs to occur before any imports you want instrumentation
  // to be aware of. This step is separated from the constructor if only because
  // there are irreversible side effects galore.
  public init(): void {
    if (!this.features.honeycomb) {
      this.initialized = true
      return
    }

    try {
      const writeKey: string | null = this.writeKey
      const dataset: string | null = this.dataset
      const sampleRate: number = this.sampleRate
      const serviceName: string = this.serviceName

      if (this.features.beeline && writeKey) {
        beeline({ writeKey, dataset, sampleRate, serviceName })
        this.initialized = true
        return
      }

      const f = this.factories

      const headers: HoneycombOTLPHeaders = f.headers(writeKey, dataset)
      const resource: otelResources.Resource = f.resource(serviceName)

      const exporter = f.spanExporter(this.options.otlpProtocol || 'http/protobuf', headers)
      const processor = f.spanProcessor(exporter)
      const instrumentations = f.instrumentations()

      const provider: NodeTracerProvider = f.tracerProvider(resource)
      provider.addSpanProcessor(processor)
      provider.register()

      const sdk = f.sdk(
        resource,
        instrumentations,
      )

      this.spanExporter = exporter
      this.spanProcessor = processor
      this.instrumentations = instrumentations
      this.tracerProvider = provider

      this.sdk = sdk

      this.initialized = true
    } catch (err) {
      if (err instanceof HoneycombError) {
        otel.diag.error((err as any).stack || String(err));
        return;
      }
      throw err;
    }
  }

  // Start the OpenTelemetry SDK. If using beelines, this is
  // a no-op. This needs to happen before anything happens in
  // the entrypoint and is an async operation.
  public async start(): Promise<void> {
    const sdk = this.sdk

    const shutdown = async () => {
      await this.stop()
    }

    if (sdk) {
      process.once('beforeExit', shutdown)

      await sdk.start()
    }
    this.started = true
  }

  public async stop(): Promise<void> {
    const sdk = this.sdk
    if (!sdk) return
    try {
      await sdk.shutdown()
    } catch (err) {
      otel.diag.error((err as any).stack || String(err))
    }
  }

  public get writeKey (): string | null {
    return this.options.writeKey || null
  }

  public get dataset (): string | null {
    return this.options.dataset || null
  }

  public get sampleRate (): number {
    return this.options.sampleRate || 1
  }

  public get serviceName (): string {
    return this.options.serviceName || 'telemetrence'
  }

  public get logger (): typeof bole | null {
    return this._logger
  }

  public set logger (logger: typeof bole | null) {
    this._logger = logger
    _diagLogger.logger = logger ? logger : undefined
  }
}

export {
  beeline,
  otel,
  otelCore,
  otelResources,
  OtelSDK,
  otelTraceBase,
  NodeTracerProvider,
  otelSemanticConventions,
  OtelInstrumentation,
  OtelDnsInstrumentation,
  OtelHttpInstrumentation,
  // 
  OtelRedisInstrumentation,
  // 
  // 
  OtelPgInstrumentation
  // 
}

export {
  defaultOtelFactories,
  Honeycomb,
  HoneycombError,
  HoneycombFeatures,
  HoneycombOptions,
  HoneycombOTLPHeaders,
  OtelFactories,
  OtelFactoryOverrides,
}

void ``

class OtelMockSpanProcessor extends otelTraceBase.SimpleSpanProcessor {
  public _exporterCreatedSpans: otelTraceBase.ReadableSpan[] = []

  constructor(_exporter: otelTraceBase.SpanExporter) {
    super(_exporter)
    this._exporterCreatedSpans = []
  }

  onEnd(span: otelTraceBase.ReadableSpan): void {
    // note that this collects spans as they *close*, meaning a parent span
    // will be *behind* its children
    this._exporterCreatedSpans.push(span)
  }
}

function getOtelMockSpans(spanProcessor: otelTraceBase.SpanProcessor | null): otelTraceBase.ReadableSpan[] {
  const processor: any = spanProcessor

  if (!processor) {
    throw new Error(
      'Span processor is not defined - did you initialize honeycomb?'
    )
  }

  if (!processor._exporterCreatedSpans) {
    throw new Error(
      'Span processor is not an OtelMockSpanProcessor'
    )
  }

  return <otelTraceBase.ReadableSpan[]>(processor._exporterCreatedSpans)
}

function resetOtelMockSpans(spanProcessor: otelTraceBase.SpanProcessor | null): void {
  const processor: any = spanProcessor

  if (!processor) {
    throw new Error(
      'Span processor is not defined - did you initialize honeycomb?'
    )
  }

  if (!processor._exporterCreatedSpans) {
    throw new Error(
      'Span processor is not an OtelMockSpanProcessor'
    )
  }

  processor._exporterCreatedSpans = []
}

function createMockHoneycomb(): Honeycomb {
  process.env.OTEL_LOG_LEVEL = 'error'
  return new Honeycomb(
    {
      serviceName: 'test-app',
      disable: false,
      otel: true,
      writeKey: 'SOME_WRITEKEY',
      dataset: 'SOME_DATASET',
      sampleRate: 1
    },
    {
      spanProcessor(spanExporter) {
        return new OtelMockSpanProcessor(spanExporter)
      }
    }
  )
}

export {
  createMockHoneycomb,
  getOtelMockSpans,
  OtelMockSpanProcessor,
  resetOtelMockSpans
}

void ``;

if (!process.env.HONEYCOMB_DATASET && process.env.HONEYCOMBIO_DATASET) {
  process.env.HONEYCOMB_DATASET = process.env.HONEYCOMBIO_DATASET
}

if (!process.env.HONEYCOMB_WRITEKEY && process.env.HONEYCOMBIO_WRITEKEY) {
  process.env.HONEYCOMB_WRITEKEY = process.env.HONEYCOMBIO_WRITEKEY
}

if (!process.env.HONEYCOMB_SAMPLE_RATE && process.env.HONEYCOMBIO_SAMPLE_RATE) {
  process.env.HONEYCOMB_SAMPLE_RATE = process.env.HONEYCOMBIO_SAMPLE_RATE
}

if (!process.env.HONEYCOMB_TEAM && process.env.HONEYCOMBIO_TEAM) {
  process.env.HONEYCOMB_TEAM = process.env.HONEYCOMBIO_TEAM
}

let honeycomb: Honeycomb = Honeycomb.fromEnv(process.env);

void ``;
honeycomb = createMockHoneycomb()
void ``;

honeycomb.init()

export { honeycomb }

void ``;

import tap from 'tap'
type Test = (typeof tap.Test)["prototype"]

/* c8 ignore next */
if (require.main === module) {
  const { test } = tap

  test('Honeycomb.parseEnv', async (t: Test) => {
    t.test('options.disable', async (assert: Test) => {
      assert.equal(
        Honeycomb.parseEnv({}).disable,
        true,
        'should be disabled when no env vars'
      )
      assert.equal(
        Honeycomb.parseEnv({HONEYCOMB_WRITEKEY: ''}).disable,
        true,
        'should be disabled when env vars are blank'
      )
      assert.equal(
        Honeycomb.parseEnv({HONEYCOMB_WRITEKEY: 'some write key'}).disable,
        false,
        'should be enabled when write key is defined'
      )
      assert.equal(
        Honeycomb.parseEnv({OTEL_ENABLED: '1'}).disable,
        false,
        'should be enabled if any otel env var is set'
      )
    })

    t.test('options.otel', async (assert: Test) => {
      assert.equal(
        Honeycomb.parseEnv({}).otel,
        false,
        'should not use otel when no env vars'
      )
      assert.equal(
        Honeycomb.parseEnv(
          {
            HONEYCOMB_WRITEKEY: '',
            HONEYCOMB_API_HOST: 'https://refinery.tech'
          }
        ).otel,
        false,
        'should not use otel when only beeline variables are set'
      )
      assert.equal(
        Honeycomb.parseEnv(
          {
            HONEYCOMB_WRITEKEY: 'some write key',
            OTEL_EXPORTER_OTLP_ENDPOINT: 'https://refinery.website'
          }
        ).otel,
        true,
        'should use otel when OTEL_EXPORTER_OTLP_ENDPOINT is defined'
      )
      assert.equal(
        Honeycomb.parseEnv(
          {
            OTEL_ENABLED: '1'
          }
        ).otel,
        true,
        'should use otel when any OTEL_* variable is defined, even if HONEYCOMB_WRITEKEY is missing'
      )
      assert.equal(
        Honeycomb.parseEnv(
          {
            OTEL_ENABLED: ''
          }
        ).otel,
        false,
        'should NOT use otel when all OTEL_* variables are defined as empty strings'
      )
    })

    t.test('options.sampleRate', async (assert: Test) => {
      assert.equal(
        Honeycomb.parseEnv({}).sampleRate,
        1,
        'should be 1 by default'
      )
      assert.equal(
        Honeycomb.parseEnv(
          { HONEYCOMB_SAMPLE_RATE: '1' }
        ).sampleRate,
        1,
        'should be 1 if defined as 1'
      )
      assert.equal(
        Honeycomb.parseEnv(
          {
            HONEYCOMB_SAMPLE_RATE: '0.5'
          }
        ).sampleRate,
        0.5,
        'should be 0.5 if defined as 0.5'
      )
      assert.equal(
        Honeycomb.parseEnv(
          { HONEYCOMB_SAMPLE_RATE: 'pony' }
        ).sampleRate,
        1,
        'should be 1 if not parseable'
      )
    })

    t.test('options.serviceName', async (assert: Test) => {
      assert.equal(
        Honeycomb.parseEnv({}).serviceName,
        'telemetrence',
        'should fall back to "telemetrence" when no env vars (nor package.json)'
      )
      assert.equal(
        Honeycomb.parseEnv({ SERVICE_NAME: 'test-app' }).serviceName,
        'test-app',
        'should use SERVICE_NAME when defined'
      )
      assert.equal(
        Honeycomb.parseEnv({ OTEL_SERVICE_NAME: 'test-app' }).serviceName,
        'test-app',
        'should use OTEL_SERVICE_NAME when defined'
      )
      assert.equal(
        Honeycomb.parseEnv({
          SERVICE_NAME: 'test-app',
          OTEL_SERVICE_NAME: 'otel-test-app'
        }).serviceName,
        'otel-test-app',
        'OTEL_SERVICE_NAME should take precedence over SERVICE_NAME'
      )
      assert.equal(
        Honeycomb.parseEnv({
          SERVICE_NAME: 'test-app',
          OTEL_SERVICE_NAME: ''
        }).serviceName,
        'test-app',
        "OTEL_SERVICE_NAME should be ignored when it's a blank string"
      )
    })
  })
  test('factories', async (t: Test) => {
    t.test('headers', async (assert: Test) => {
      const headers = defaultOtelFactories.headers(
        'some write key',
        'some dataset'
      )

      assert.same(
        headers,
        {
          'x-honeycomb-team': 'some write key',
          'x-honeycomb-dataset': 'some dataset'
        },
        'should have the expected headers'
      )
    })

    t.test('resource', async (assert: Test) => {
      assert.doesNotThrow(() => defaultOtelFactories.resource('test-service'))
    })

    test('tracerProvider', async (assert: Test) => {
      const resource = defaultOtelFactories.resource('test-service')
      assert.doesNotThrow(
        () => defaultOtelFactories.tracerProvider(resource),
        'should create a tracer provider'
      )
    })

    test('spanExporter', async (assert: Test) => {
      const headers = defaultOtelFactories.headers(
        'some write key',
        'some dataset'
      )

      process.env.OTEL_LOG_LEVEL = 'error'

      for (let protocol of ['grpc', 'http/protobuf', 'http/json']) {
        assert.doesNotThrow(() => {
          defaultOtelFactories.spanExporter(protocol, headers)
        })
      }
    })

    test('spanProcessor', async (assert: Test) => {
      assert.doesNotThrow(() => {
        const exporter = defaultOtelFactories.spanExporter(
          'http/protobuf',
          defaultOtelFactories.headers(
            'some write key',
            'some dataset'
          )
        )

        defaultOtelFactories.spanProcessor(exporter)
      }, 'should create a span processor')
    })

    test('instrumentations', async (assert: Test) => {
      // expected instrumentations: dns, node core, postgres, redis
      assert.equal(
        defaultOtelFactories.instrumentations().length,
        4,
        'should create 4 instrumentations (dns, http, postgres, redis)'
      )
    })

    test('sdk', async (assert: Test) => {
      // run the init function
      assert.doesNotThrow(() => {
        const resource = defaultOtelFactories.resource('test-service')
        const instrumentations = defaultOtelFactories.instrumentations()

        defaultOtelFactories.sdk(
          resource, 
          instrumentations,
        )
      }, 'should create an sdk')
    })
  })

  test('init and start', async (assert: Test) => {
    const honeycomb = createMockHoneycomb()

    honeycomb.init()

    assert.doesNotThrow(async () => {
      await honeycomb.start()
      await honeycomb.stop()
    })
  })
}

void ``
void ``

