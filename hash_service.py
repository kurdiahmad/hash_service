import logging
from flask import Flask, request, jsonify
import hashlib
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry import trace
import os

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Set OpenTelemetry service name
resource = Resource.create({"service.name": "hash-service"})

# Initialize OpenTelemetry tracing
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

# Configure Jaeger Exporter (Thrift over HTTP)
jaeger_exporter = JaegerExporter(
    collector_endpoint="http://jaeger-collector.jaeger.svc.cluster.local:14268/api/traces"
)

# Add span processor
span_processor = BatchSpanProcessor(jaeger_exporter)
tracer_provider.add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

@app.route('/hash', methods=['POST'])
def hash_string():
    with tracer.start_as_current_span("hash_request") as span:
        input_data = request.get_data(as_text=True).strip()
        if not input_data:
            span.set_attribute("error", True)
            return jsonify({"error": "No input provided"}), 400

        sha256_hash = hashlib.sha256(input_data.encode()).hexdigest()

        # Add trace attributes
        span.set_attribute("input_length", len(input_data))
        span.set_attribute("hash", sha256_hash)

        return sha256_hash

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
