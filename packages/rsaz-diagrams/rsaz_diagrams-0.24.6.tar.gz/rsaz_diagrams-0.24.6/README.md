# diagrams-xtd
Extended version of diagrams with some PR that never get merged and I want to use.

More details in [CHANGELOG](CHANGELOG.md).

## Resources

This package includes thousands of PNG images in the `resources` directory, organized by cloud provider and service type. These resources are automatically included in the package distribution and are used by the diagrams library to render cloud architecture diagrams.

### Using Custom Icons

If you need to use custom icons, you can use the `Custom` class:

```python
from diagrams import Diagram
from diagrams.custom import Custom

with Diagram("Custom Icons"):
    Custom("My Custom Icon", "./path/to/custom/icon.png")
```

### Accessing Package Resources

The package resources are installed in the Python package distribution. If you need to access them directly:

```python
import os
from pkg_resources import resource_filename

# Get path to a specific icon
azure_icon = resource_filename('diagrams', 'resources/azure/azure.png')

# Or using the direct resource path
from pathlib import Path
site_packages = Path(__file__).parent.parent  # Adjust based on your import location
azure_icon = site_packages / 'resources' / 'azure' / 'azure.png'
```
