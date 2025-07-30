from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased


from trilla_lib.infra.jaeger.config import jaeger_config


def init_tracing():

    tracer_provider = TracerProvider(
        resource=Resource.create({
            "service.name": jaeger_config.service_name
        }),
        sampler=TraceIdRatioBased(jaeger_config.sampling_rate),
    )
    trace.set_tracer_provider(tracer_provider)

    jaeger_exporter = JaegerExporter(
        agent_host_name=jaeger_config.agent_host,
        agent_port=jaeger_config.agent_port,
    )

    span_processor = BatchSpanProcessor(jaeger_exporter)
    tracer_provider.add_span_processor(span_processor)
