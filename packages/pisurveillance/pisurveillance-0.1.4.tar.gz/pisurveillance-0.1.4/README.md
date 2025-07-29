# Surveillance Service

A Python-based surveillance service designed for Raspberry Pi devices. This service captures images from a camera at specified intervals and can be configured for different devices.

## Requirements

- Python 3.9 or higher
- Raspberry Pi with camera module
- Poetry (for installation)

## Installation

1. Install Poetry if you haven't already:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install the package:

```bash
# Install from PyPI
pip install surveillance-service

# Or install from source
git clone <your-repo-url>
cd surveillance-service
poetry install
```

## Usage

The service can be run using the following command:

```bash
surveillance [options]
```

### Command Line Options

- `-f, --frequency`: Image capture frequency in seconds (default: from .env)
- `-d, --device`: Name of your device (default: from .env)
- `-c, --camera`: Camera index (default: from .env)

### Example

```bash
surveillance --frequency 30 --device "raspberry-pi-1" --camera 0
```

## Configuration

Create a `.env` file in your working directory with the following variables:

```
CAPTURE_FREQUENCY=30
DEVICE_NAME=raspberry-pi-1
CAMERA_INDEX=0
```

## License

[Your License]
