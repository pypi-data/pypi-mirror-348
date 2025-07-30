# Solentra - DeSci AI Agent

A powerful Python package for creating science-themed AI agents with advanced research and experimentation capabilities. Solentra enables automated scientific workflows, experiment simulation, research paper analysis, and collaborative research.

## Features

- **Core AI**
  - Specialized agent personas (physicist, biologist, etc.)
  - Context-aware conversation management
  - Multi-agent collaboration capabilities
  - Async processing for complex tasks
  - Model training and evaluation

- **Research Tools**
  - Structured research task planning
  - Experiment design and management
  - Scientific paper analysis
  - Citation handling and formatting
  - Data cleaning and preprocessing

- **Social Integration**
  - Twitter research updates
  - Media sharing capabilities
  - Engagement analytics
  - Impact assessment tools

## Installation

### From PyPI (Recommended)

```bash
pip install solentra
```

### From Source

```bash
git clone https://github.com/solentra/solentra.git
cd solentra
pip install -e .
```

### Development Installation

```bash
pip install solentra[dev]
```

## Quick Start

```python
from solentra import SolentraAgent

# Initialize agent
agent = SolentraAgent(
    agent_name="Research Scientist",
    model_name="solentra-70b",
    tools_enabled=True
)

# Create and run an experiment
protocol = agent.create_experiment(
    steps=["Sample preparation", "Data collection"],
    materials=["Reagent A", "Equipment B"],
    duration="2 hours",
    conditions={"temperature": 25}
)

results = agent.run_experiment(
    protocol=protocol,
    variables={"concentration": 0.5},
    iterations=3
)

# Analyze results
analysis = agent.analyze_data(
    [r['variables']['concentration'] for r in results['results']]
)
```

## Documentation

For detailed documentation, visit our [documentation site](https://solentra.ai/docs).

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Email: contact@solentra.ai
- Twitter: [@Solentra](https://x.com/SolentraAI)
- GitHub: [solentra/solentra](https://github.com/solentra/solentra)
