# Changelog

## [0.1.0] - Initial Release

The first official release of `UniLVQ` includes:

### 📦 Project Infrastructure
- Add standard project files: `CODE_OF_CONDUCT.md`, `MANIFEST.in`, `LICENSE`, `CITATION.cff`, `requirements.txt`
- Add core utility modules: `verifier`, `scorer`, `early_stopper`, `data_scaler`, `data_handler`
- Add common base model: `BaseModel` (in `base_model.py`)

### 🧠 Rule-based LVQ Models (in `classic_lvq.py`)
- `BaseLVQ`: Inherits `BaseModel`
- `Lvq1Classifier`: Implements LVQ1, inherits `BaseLVQ`, `ClassifierMixin`
- `Lvq21Classifier`: Implements LVQ2.1, inherits `BaseLVQ`, `ClassifierMixin`
- `Lvq3Classifier`: Implements LVQ3, inherits `BaseLVQ`, `ClassifierMixin`
- `OptimizedLvq1Classifier`: Optimized LVQ1, inherits `BaseLVQ`, `ClassifierMixin`

### 🔁 Generalized LVQ Models (in `glvq.py`)
- `CustomGLVQ`: PyTorch-based model (`nn.Module`)
- `GlvqClassifier`: Wraps `CustomGLVQ`, inherits `BaseModel`, `ClassifierMixin`
- `GlvqRegressor`: Wraps `CustomGLVQ`, inherits `BaseModel`, `RegressorMixin`

### 🔁 Generalized Relevance LVQ Models (in `grlvq.py`)
- `CustomGRLVQ`: PyTorch-based model (`nn.Module`)
- `GrlvqClassifier`: Wraps `CustomGRLVQ`, inherits `BaseModel`, `ClassifierMixin`
- `GrlvqRegressor`: Wraps `CustomGRLVQ`, inherits `BaseModel`, `RegressorMixin`

### 🧭 Local Generalized Matrix LVQ Models (in `lgmlvq.py`)
- `CustomLGMLVQ`: PyTorch-based model (`nn.Module`)
- `LgmlvqClassifier`: Wraps `CustomLGMLVQ`, inherits `BaseModel`, `ClassifierMixin`

### 🛠 DevOps & Docs
- Add publishing workflow (CI/CD)
- Add example notebooks
- Add unit tests
- Add documentation website
