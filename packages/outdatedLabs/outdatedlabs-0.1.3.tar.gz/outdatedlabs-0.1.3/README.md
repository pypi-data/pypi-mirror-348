# OutdatedLabs - Secure Machine Learning Training Package

A secure and easy-to-use package for training machine learning models with remote server support.

## Installation

```bash
pip install outdatedLabs
```

## Quick Start

Use the package in your code:
```python
from outdatedLabs import SecureModel

# Create a linear regression model
model = SecureModel.linearRegression()

# Train the model
model.train(
    dataset_hash="your_dataset_hash",
    features=["feature1", "feature2"],
    target="target_column"
)

# Get training metrics
metrics = model.get_metrics()
print(metrics)

# Download and load the trained model
model.download_model()
loaded_model = model.load_model()
```

## Features

- Secure model training with remote server support
- Automatic dataset download and cleanup
- Progress tracking with tqdm
- Comprehensive error handling
- Detailed logging
- Support for multiple algorithms (currently Linear Regression)

## Configuration

The package connects to a local ML training server by default at `http://localhost:3000`. You can change the server URL when creating a model:

```python
model = SecureModel.linearRegression(server_url="http://your-server:3000")
```

## API Reference

### SecureModel

The main class for model training and management.

#### Methods

- `linearRegression(server_url: str = "http://localhost:3000")`: Create a Linear Regression model
- `train(dataset_hash: str, features: List[str], target: str)`: Train the model
- `get_metrics() -> Dict`: Get training metrics
- `download_model() -> str`: Download the trained model
- `load_model() -> Any`: Load the trained model

## License

MIT License 