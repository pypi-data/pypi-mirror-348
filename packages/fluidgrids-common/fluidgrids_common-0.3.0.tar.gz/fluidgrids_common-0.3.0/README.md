# Fluidgrids Common

A shared package for common utilities used across Fluidgrids backend nodes.

## Features

- NATS client management and messaging utilities
- OpenTelemetry configuration for observability
- Base server implementation
- Credential management utilities
- Adapter utilities

## Installation

```bash
pip install fluidgrids-common
```

## Usage

### Server Setup

```python
from fluidgrids_common.server import create_app
from fluidgrids_common.utils.otel_config import setup_opentelemetry_for_node

# Setup OpenTelemetry
setup_opentelemetry_for_node()

# Create FastAPI app with standard configuration
app = create_app(
    title="My Node",
    description="Node description",
    version="1.0.0"
)

# Add your routes and mount GraphQL
from my_node.gql import graphql_app
app.mount("/graphql/", graphql_app)

if __name__ == "__main__":
    from fluidgrids_common.server import run_server
    run_server(app)
```

### NATS Utilities

```python
from fluidgrids_common.utils.main import init_nats, publish_log_to_nats, publish_event_to_nats

# Initialize NATS
await init_nats()

# Publish logs and events
await publish_log_to_nats(run_id, node_id, "INFO", "Operation started")
await publish_event_to_nats(run_id, node_id, "STATUS_CHANGE", {"status": "RUNNING"})
```

## Development

```bash
# Clone the repository
git clone https://github.com/algoshred/fluidgrids-common.git
cd fluidgrids-common

# Install in development mode
pip install -e .
```

## License

MIT 