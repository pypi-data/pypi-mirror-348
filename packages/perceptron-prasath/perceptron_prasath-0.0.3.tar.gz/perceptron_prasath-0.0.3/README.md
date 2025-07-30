# Perceptron Python Package

## References - 

* [Official python docs from PYPI](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
# Perceptron from Scratch 🚀

This project is an **end-to-end implementation of the Perceptron algorithm** from scratch using Python and NumPy — without using any high-level ML libraries. It includes training logic, prediction, model serialization, automated testing, CI/CD integration via GitHub Actions, and deployment as a PyPI package.

---

## 📦 PyPI Package

Install it using pip:

```bash
pip install perceptron-scratch

# Project Structure
perceptron-scratch/
│
├── perceptron/               # Core Perceptron implementation
│   ├── __init__.py
│   ├── perceptron.py
│   └── utils.py
│
├── tests/                    # Unit tests
│   └── test_perceptron.py
│
├── .github/workflows/        # GitHub Actions CI/CD pipeline
│   └── python-publish.yml
│
├── setup.py                  # Packaging config
├── pyproject.toml            # Build system
├── README.md
└── LICENSE

What is a Perceptron?
A Perceptron is the simplest form of a neural network used for binary classification. It computes a weighted sum of the inputs and passes it through an activation function (step function in this case).

✨ Features
✅ Trainable Perceptron model from scratch

✅ Supports binary classification

✅ Uses NumPy for matrix operations

✅ CLI-compatible structure

✅ Model saving & loading using joblib

✅ Unit tests included

✅ GitHub Actions for CI/CD

✅ Packaged and deployed to PyPI

# How to Use It
```bash
from perceptron.perceptron import Perceptron
from perceptron.utils import prepare_data
import pandas as pd

# Sample Data - AND Gate
data = {
    "x1": [0, 0, 1, 1],
    "x2": [0, 1, 0, 1],
    "y":  [0, 0, 0, 1]
}
df = pd.DataFrame(data)
X, y = prepare_data(df, target_column="y")

# Train the Model
model = Perceptron(eta=0.1, epochs=10)
model.fit(X, y)
model.total_loss()

# Save and Load
model.save("and.model")
reloaded_model = model.load("model/and.model")
