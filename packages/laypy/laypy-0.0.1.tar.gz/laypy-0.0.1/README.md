# Laypy (WIP)

Laypy is a Python binding for the [layout](https://github.com/nadavrot/layout), an engine for graphviz, providing efficient graph visualization and layout capabilities.


## Features

- Fast graph layout algorithms implemented in Rust
- Seamless Python integration
- Compatible with common Python graph libraries
- Multiple layout algorithms (force-directed, hierarchical, radial, etc.)
- Customizable node and edge styling
- Export to various formats (SVG, PNG, PDF)
- No need to install Graphviz separately

## Installation

```bash
pip install laypy
```

### Requirements

- Python 3.8+

## Quick Start

```python
import laypy

# Create a simple graph
graph = laypy.Graph()

# Add nodes
graph.add_node("A")
graph.add_node("B")
graph.add_node("C")

# Add edges
graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("C", "A")

# Apply a layout algorithm
layout = laypy.ForceDirected(graph)
layout.compute()

# Export the result
layout.to_svg("my_graph.svg")
```

## Documentation


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

TODO list

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Rust [layout](https://github.com/nadavrot/layout) project
- GraphViz team