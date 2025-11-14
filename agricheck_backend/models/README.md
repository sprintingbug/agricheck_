# Models Directory

## Current Files

- `agricheckmodel.ipynb` - Jupyter notebook with model training code
- `export_model.py` - Script to export model from Kaggle
- `extract_model_from_notebook.py` - Script to create model architecture from notebook

## Understanding the Notebook vs Model

### The Notebook (`agricheckmodel.ipynb`)
- **What it is**: Training script/code
- **Contains**: Model architecture definition, training code, data preprocessing
- **Purpose**: Used to train the model
- **Output**: Creates trained model files (`.keras` or `.h5`)

### The Trained Model (`.keras` or `.h5` file)
- **What it is**: The actual trained model with weights
- **Contains**: Model architecture + learned weights
- **Purpose**: Used for predictions/inference
- **Required for**: Backend to make predictions

## How to Get the Trained Model

### Option 1: From Kaggle (Recommended)

If you trained the model in Kaggle:

1. **Go to your Kaggle notebook**
2. **Check the "Output" tab** - look for saved model files:
   - `best_finetuned.keras` (best accuracy - recommended)
   - `best.keras`
   - `model_finetuned.tflite`

3. **Download the `.keras` file**

4. **Place it in this directory** (`models/`):
   ```
   models/best_finetuned.keras  # Will be auto-detected
   ```

### Option 2: Export from Kaggle Notebook

Add this cell to your Kaggle notebook and run it:

```python
from tensorflow import keras
import os

# Load your best trained model
model = keras.models.load_model("/kaggle/working/best_finetuned.keras")

# Save to output (downloadable)
model.save("/kaggle/working/plant_disease_model.keras")
print("✅ Model exported! Download from Kaggle outputs.")
```

Then download from Kaggle outputs.

### Option 3: Train Locally

If you want to train the model locally:

1. **Install dependencies**:
   ```bash
   pip install tensorflow jupyter
   ```

2. **Run the notebook**:
   ```bash
   jupyter notebook agricheckmodel.ipynb
   ```

3. **After training**, the model will be saved as:
   - `best.keras`
   - `best_finetuned.keras`

4. **Copy to this directory**

## Model File Naming

The backend will automatically search for model files in this order:

1. `best_finetuned.keras` ⭐ (recommended - best accuracy)
2. `best.keras`
3. `plant_disease_model.keras`
4. `plant_disease_model.h5`
5. `model.keras`
6. `model.h5`

## Current Status

- ✅ Notebook available (`agricheckmodel.ipynb`)
- ⏳ Waiting for trained model file (`.keras` or `.h5`)

## Next Steps

1. **Export/download your trained model** from Kaggle
2. **Place it in this directory** (`models/`)
3. **Name it** `best_finetuned.keras` (or one of the auto-detected names)
4. **Start the backend server** - it will automatically load the model

## Testing

After placing the model file, test it:

```bash
cd ..
python test_model.py
```

This will verify:
- ✅ Model file exists
- ✅ Model loads correctly
- ✅ Dependencies are installed

