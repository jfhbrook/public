'use strict';
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.honeycomb = exports.HoneycombError = exports.Honeycomb = exports.defaultOtelFactories = exports.OtelPgInstrumentation = exports.OtelRedisInstrumentation = exports.OtelHttpInstrumentation = exports.OtelDnsInstrumentation = exports.OtelInstrumentation = exports.otelSemanticConventions = exports.NodeTracerProvider = exports.otelTraceBase = exports.OtelSDK = exports.otelResources = exports.otelCore = exports.otel = exports.beeline = exports.isDev = exports.bole = void 0;
/**/
// Dependencies used outside of honeycomb
const bole_1 = __importDefault(require("@entropic/bole"));
exports.bole = bole_1.default;
const are_we_dev_1 = __importDefault(require("are-we-dev"));
exports.isDev = are_we_dev_1.default;
void ``;
// We continue to support beelines...
const honeycomb_beeline_1 = __importDefault(require("honeycomb-beeline"));
exports.beeline = honeycomb_beeline_1.default;
// ...but are migrating to OpenTelemetry:
const grpc = __importStar(require("@grpc/grpc-js"));
const otel = __importStar(require("@opentelemetry/api"));
exports.otel = otel;
const otelCore = __importStar(require("@opentelemetry/core"));
exports.otelCore = otelCore;
const otlpHttp = __importStar(require("@opentelemetry/exporter-trace-otlp-http"));
const otlpProto = __importStar(require("@opentelemetry/exporter-trace-otlp-proto"));
const otlpGrpc = __importStar(require("@opentelemetry/exporter-trace-otlp-grpc"));
const otelResources = __importStar(require("@opentelemetry/resources"));
exports.otelResources = otelResources;
const sdk_node_1 = require("@opentelemetry/sdk-node");
Object.defineProperty(exports, "OtelSDK", { enumerable: true, get: function () { return sdk_node_1.NodeSDK; } });
const otelTraceBase = __importStar(require("@opentelemetry/sdk-trace-base"));
exports.otelTraceBase = otelTraceBase;
const sdk_trace_node_1 = require("@opentelemetry/sdk-trace-node");
Object.defineProperty(exports, "NodeTracerProvider", { enumerable: true, get: function () { return sdk_trace_node_1.NodeTracerProvider; } });
const otelSemanticConventions = __importStar(require("@opentelemetry/semantic-conventions"));
exports.otelSemanticConventions = otelSemanticConventions;
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
const instrumentation_1 = require("@opentelemetry/instrumentation");
Object.defineProperty(exports, "OtelInstrumentation", { enumerable: true, get: function () { return instrumentation_1.Instrumentation; } });
const instrumentation_dns_1 = require("@opentelemetry/instrumentation-dns");
Object.defineProperty(exports, "OtelDnsInstrumentation", { enumerable: true, get: function () { return instrumentation_dns_1.DnsInstrumentation; } });
const instrumentation_http_1 = require("@opentelemetry/instrumentation-http");
Object.defineProperty(exports, "OtelHttpInstrumentation", { enumerable: true, get: function () { return instrumentation_http_1.HttpInstrumentation; } });
void ``;
const instrumentation_redis_1 = require("@opentelemetry/instrumentation-redis");
Object.defineProperty(exports, "OtelRedisInstrumentation", { enumerable: true, get: function () { return instrumentation_redis_1.RedisInstrumentation; } });
void ``;
void ``;
const instrumentation_pg_1 = require("@opentelemetry/instrumentation-pg");
Object.defineProperty(exports, "OtelPgInstrumentation", { enumerable: true, get: function () { return instrumentation_pg_1.PgInstrumentation; } });
void ``;
class HoneycombError extends Error {
}
exports.HoneycombError = HoneycombError;
// A diagnostic logger for OpenTelemetry. To log at a sensible level,
// call otel.diag.verbose.
class HoneycombDiagLogger {
    // Ideally we would log to a bole logger. However, logger setup happens
    // relatively late - in the log middleware - and it's very likely that such
    // a log won't be in-place when we stand up the middleware stack! Therefore,
    // we do log to bole if it's set in the middleware but will fall back to
    // good ol' fashioned JSON.stringify if need be.
    constructor() {
        this._stream = process.stdout;
        // So log messages roughly match what's output by the bole in dev mode :^)
        if ((0, are_we_dev_1.default)()) {
            const pretty = require('bistre')({ time: true });
            this._stream = pretty.pipe(this._stream);
        }
    }
    // OpenTelemetry's diagnostic logger has one more log level than bole - ie,
    // verbose.
    //
    // For more details on how to treat each log level, see:
    // https://github.com/open-telemetry/opentelemetry-js-api/blob/main/src/diag/consoleLogger.ts#L60
    // Log errors that caused an unexpected failure
    error(message, ...args) {
        this._log('error', message, args);
    }
    // Log warnings that aren't show-stopping but should REALLY be looked at
    warn(message, ...args) {
        this._log('warn', message, args);
    }
    // Log info if you want to be REALLY LOUD for some reason - you probably
    // don't want to use this!
    info(message, ...args) {
        this._log('info', message, args);
    }
    // Log details that could be useful for identifying what went wrong, but
    // aren't the thing that went wrong itself - treat this as you would info
    // logging normally
    debug(message, ...args) {
        this._log('debug', message, args);
    }
    // Log fine-grained details that are mostly going to be useful to those
    // adding new OpenTelemetry related features to boltzmann - treat this like
    // you would debug level logging normally
    verbose(message, ...args) {
        this._log('debug', `VERBOSE: ${message}`, args);
    }
    _log(level, message, args) {
        let isSelfTest = false;
        void ``;
        if (isSelfTest) {
            return;
        }
        // Log to bole if we have it
        if (this.logger) {
            this.logger[level](message, ...args);
            return;
        }
        const line = {
            time: (new Date()).toISOString(),
            level,
            name: 'telemetrence:honeycomb',
            message,
            args
        };
        try {
            // are the args JSON-serializable?
            this._writeLine(JSON.stringify(line));
            // SURVEY SAYS...
        }
        catch (_) {
            // ...ok, make it a string as a fallback
            line.args = require('util').format('%o', line.args);
            this._writeLine(JSON.stringify(line));
        }
    }
    _writeLine(line) {
        this._stream.write(Buffer.from(line + '\n'));
    }
}
// We only do OpenTelemetry logging if boltzmann's main log level is debug
const _diagLogger = new HoneycombDiagLogger();
if (!process.env.LOG_LEVEL || process.env.LOG_LEVEL === 'debug') {
    otel.diag.setLogger(_diagLogger, otelCore.getEnv().OTEL_LOG_LEVEL);
}
const defaultOtelFactories = {
    headers(writeKey, dataset) {
        let headers = {};
        if (writeKey) {
            headers['x-honeycomb-team'] = writeKey;
        }
        if (dataset) {
            headers['x-honeycomb-dataset'] = dataset;
        }
        return headers;
    },
    resource(serviceName) {
        return new otelResources.Resource({
            [otelSemanticConventions.SemanticResourceAttributes.SERVICE_NAME]: serviceName
        });
    },
    // A tracer provider is effectively a Tracer factory and is used to power
    // the otel.getTrace API
    tracerProvider(resource) {
        return new sdk_trace_node_1.NodeTracerProvider({ resource });
    },
    // There are three different OTLP span exporter classes - one for grpc, one
    // for http/protobuf and one for http/json - this will return the appropriate
    // one for the configured protocol.
    spanExporter(protocol, headers) {
        // Instead of subclassing each implementation, monkey patch the send
        // method on whichever instance we create
        function patchSend(exporter) {
            const send = exporter.send;
            exporter.send = function (objects, onSuccess, 
            // This error is actually an Error subtype which corresponds 1:1 with
            // the OTLPTraceExporter class being instrumented, but making this a
            // proper generic type is hard - it's fine!
            onError) {
                otel.diag.debug(`sending ${objects.length} spans to ${this.url}`);
                send.call(this, objects, () => {
                    otel.diag.debug(`successfully send ${objects.length} spans to ${this.url}`);
                    return onSuccess();
                }, (error) => {
                    otel.diag.debug(`error while sending ${objects.length} spans: ${error}`);
                    return onError(error);
                });
            };
        }
        if (protocol === 'grpc') {
            const metadata = new grpc.Metadata();
            for (let [key, value] of Object.entries(headers)) {
                metadata.set(key, value);
            }
            const credentials = grpc.credentials.createSsl();
            const exporter = new otlpGrpc.OTLPTraceExporter({
                credentials,
                metadata
            });
            patchSend(exporter);
            return exporter;
        }
        if (protocol === 'http/json') {
            otel.diag.warn("Honeycomb doesn't support the http/json OTLP protocol - but if you say so");
            const exporter = new otlpHttp.OTLPTraceExporter({
                headers
            });
            patchSend(exporter);
            return exporter;
        }
        if (protocol !== 'http/protobuf') {
            otel.diag.warn(`Unknown OTLP protocol ${protocol} - using http/protobuf instead`);
        }
        const exporter = new otlpProto.OTLPTraceExporter({
            headers
        });
        patchSend(exporter);
        return exporter;
    },
    // Process spans, using the supplied trace exporter to
    // do the actual exporting.
    spanProcessor(spanExporter) {
        // There's a bug in the trace base library where the SimpleSpanProcessor doesn't
        // actually conform to the SpanProcessor interface! Luckily this difference
        // comes from not including an optional argument in the type signature and is
        // safe to cast.
        return (new otelTraceBase.SimpleSpanProcessor(spanExporter));
    },
    instrumentations() {
        // Any paths we add here will get no traces whatsoever. This is
        // appropriate for the ping route, which should never trace.
        const ignoreIncomingPaths = [
            '/monitor/ping'
        ];
        // OpenTelemetry attempts to auto-collect GCE metadata, causing traces
        // we don't care about. We do our best to ignore them by independently
        // calculating which endpoints it's going to try to call.
        //
        // See: https://github.com/googleapis/gcp-metadata/blob/main/src/index.ts#L26-L44
        const ignoreOutgoingUrls = [
            /^https?:\/\/169\.254\.169\.254/,
            /^https?:\/\/metadata\.google\.internal/,
        ];
        let gceBase = process.env.GCE_METADATA_IP || process.env.GCE_METADATA_HOST || null;
        if (gceBase) {
            if (!/^https?:\/\//.test(gceBase)) {
                gceBase = `http://${gceBase}`;
            }
            ignoreOutgoingUrls.push(new RegExp(`^${gceBase}`));
        }
        let is = [
            new instrumentation_dns_1.DnsInstrumentation({}),
            // NOTE: This instrumentation creates the default "trace" span and manages
            // header propagation! See the honeycomb trace middleware for more
            // details.
            new instrumentation_http_1.HttpInstrumentation({
                // TODO: These fields are expected to become deprecated in the
                // near future...
                ignoreIncomingPaths,
                ignoreOutgoingUrls
            }),
        ];
        void ``;
        is.push(new instrumentation_redis_1.RedisInstrumentation({}));
        void ``;
        void ``;
        is.push(new instrumentation_pg_1.PgInstrumentation({}));
        void ``;
        return is;
    },
    // The SDK will take a service name, instrumentations
    // and a trace exporter and give us a stateful singleton.
    // This is that singleton!
    sdk(resource, instrumentations) {
        return new sdk_node_1.NodeSDK({
            resource,
            instrumentations
        });
    }
};
exports.defaultOtelFactories = defaultOtelFactories;
// Let's GOOOOOOO
class Honeycomb {
    constructor(options, overrides = {}) {
        this.options = options;
        this.features = {
            honeycomb: !options.disable,
            beeline: !options.disable && !options.otel,
            otel: options.otel || false
        };
        this.initialized = false;
        this.started = false;
        this.tracerProvider = null;
        this.spanExporter = null;
        this.spanProcessor = null;
        this.instrumentations = null;
        this.sdk = null;
        this.factories = Object.assign(Object.assign({}, defaultOtelFactories), (overrides || {}));
        this._logger = null;
    }
    get tracer() {
        return otel.trace.getTracer('telemetrence', '');
    }
    // We (usually) load options from the environment. Unlike with Options,
    // we do a lot of feature detection here.
    static fromEnv(env = process.env, overrides = {}) {
        return new Honeycomb(Honeycomb.parseEnv(env), overrides);
    }
    static parseEnv(env = process.env) {
        // For beelines, if we don't have HONEYCOMB_WRITEKEY there isn't much we
        // can do...
        let disable = !env.HONEYCOMB_WRITEKEY;
        // Beelines should pick these up automatically, but we'll need them to
        // configure default OTLP headers
        const writeKey = env.HONEYCOMB_WRITEKEY || null;
        const dataset = env.HONEYCOMB_DATASET || null;
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
        const isOtel = Object.entries(env).some(([name, value]) => {
            return name.startsWith('OTEL_') && value && value.length;
        });
        // OpenTelemetry can optionally load the honeycomb headers from the
        // OTEL_EXPORTER_OTLP_HEADERS and/or OTEL_EXPORTER_OTLP_TRACE_HEADERS
        // environment variables, so having HONEYCOMB_WRITEKEY be falsey is
        // potentially OK. This strategy also allows people to use the
        // honeycomb tracing for non-honeycomb use cases.
        if (isOtel) {
            disable = false;
        }
        // This sample rate is for beeline only - to set the OpenTelemetry sample
        // rate, set OTEL_TRACES_SAMPLER=parentbased_traceidratio and
        // OTEL_TRACES_SAMPLER_ARG=${SOME_NUMBER}. Note that beeline defines
        // sample rate as total/sampled, but OpenTelemetry defines it as
        // sampled/total!
        let sampleRate = Number(env.HONEYCOMB_SAMPLE_RATE || 1);
        if (isNaN(sampleRate)) {
            sampleRate = 1;
        }
        // OTLP is supposed to be configured with this environment variable, but
        // the OpenTelemetry SDKs leave this as a some-assembly-required job.
        // We default to 'http/protobuf' because it's well-supported by both
        // Honeycomb and AWS load balancers and because it's relatively snappy.
        //
        // For more information on how this is configured, see:
        // https://opentelemetry.io/docs/reference/specification/protocol/exporter/#specify-protocol
        const otlpProtocol = env.OTEL_EXPORTER_OTLP_PROTOCOL || env.OTEL_EXPORTER_OTLP_TRACES_PROTOCOL || 'http/protobuf';
        // The service name logic is VERY similar to what's in prelude.ts,
        // except that OTEL_SERVICE_NAME takes precedence if defined
        const serviceName = (() => {
            try {
                return env.OTEL_SERVICE_NAME || env.SERVICE_NAME || require('./package.json').name.split('/').pop();
            }
            catch (err) {
                return 'telemetrence';
            }
        })();
        return {
            serviceName,
            disable,
            otel: isOtel,
            writeKey,
            dataset,
            sampleRate,
            otlpProtocol
        };
    }
    // Initialize Honeycomb! Stands up the otel node SDK if enabled,
    // otherwise sets up the beeline library.
    // This needs to occur before any imports you want instrumentation
    // to be aware of. This step is separated from the constructor if only because
    // there are irreversible side effects galore.
    init() {
        if (!this.features.honeycomb) {
            this.initialized = true;
            return;
        }
        try {
            const writeKey = this.writeKey;
            const dataset = this.dataset;
            const sampleRate = this.sampleRate;
            const serviceName = this.serviceName;
            if (this.features.beeline && writeKey) {
                (0, honeycomb_beeline_1.default)({ writeKey, dataset, sampleRate, serviceName });
                this.initialized = true;
                return;
            }
            const f = this.factories;
            const headers = f.headers(writeKey, dataset);
            const resource = f.resource(serviceName);
            const exporter = f.spanExporter(this.options.otlpProtocol || 'http/protobuf', headers);
            const processor = f.spanProcessor(exporter);
            const instrumentations = f.instrumentations();
            const provider = f.tracerProvider(resource);
            provider.addSpanProcessor(processor);
            provider.register();
            const sdk = f.sdk(resource, instrumentations);
            this.spanExporter = exporter;
            this.spanProcessor = processor;
            this.instrumentations = instrumentations;
            this.tracerProvider = provider;
            this.sdk = sdk;
            this.initialized = true;
        }
        catch (err) {
            if (err instanceof HoneycombError) {
                otel.diag.error(err.stack || String(err));
                return;
            }
            throw err;
        }
    }
    // Start the OpenTelemetry SDK. If using beelines, this is
    // a no-op. This needs to happen before anything happens in
    // the entrypoint and is an async operation.
    start() {
        return __awaiter(this, void 0, void 0, function* () {
            const sdk = this.sdk;
            const shutdown = () => __awaiter(this, void 0, void 0, function* () {
                yield this.stop();
            });
            if (sdk) {
                process.once('beforeExit', shutdown);
                yield sdk.start();
            }
            this.started = true;
        });
    }
    stop() {
        return __awaiter(this, void 0, void 0, function* () {
            const sdk = this.sdk;
            if (!sdk)
                return;
            try {
                yield sdk.shutdown();
            }
            catch (err) {
                otel.diag.error(err.stack || String(err));
            }
        });
    }
    get writeKey() {
        return this.options.writeKey || null;
    }
    get dataset() {
        return this.options.dataset || null;
    }
    get sampleRate() {
        return this.options.sampleRate || 1;
    }
    get serviceName() {
        return this.options.serviceName || 'telemetrence';
    }
    get logger() {
        return this._logger;
    }
    set logger(logger) {
        this._logger = logger;
        _diagLogger.logger = logger ? logger : undefined;
    }
}
exports.Honeycomb = Honeycomb;
void ``;
if (!process.env.HONEYCOMB_DATASET && process.env.HONEYCOMBIO_DATASET) {
    process.env.HONEYCOMB_DATASET = process.env.HONEYCOMBIO_DATASET;
}
if (!process.env.HONEYCOMB_WRITEKEY && process.env.HONEYCOMBIO_WRITEKEY) {
    process.env.HONEYCOMB_WRITEKEY = process.env.HONEYCOMBIO_WRITEKEY;
}
if (!process.env.HONEYCOMB_SAMPLE_RATE && process.env.HONEYCOMBIO_SAMPLE_RATE) {
    process.env.HONEYCOMB_SAMPLE_RATE = process.env.HONEYCOMBIO_SAMPLE_RATE;
}
if (!process.env.HONEYCOMB_TEAM && process.env.HONEYCOMBIO_TEAM) {
    process.env.HONEYCOMB_TEAM = process.env.HONEYCOMBIO_TEAM;
}
let honeycomb = Honeycomb.fromEnv(process.env);
exports.honeycomb = honeycomb;
void ``;
honeycomb.init();
void ``;
void ``;
