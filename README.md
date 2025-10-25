# Customer Churn Prediction (ANNproject)

Predict whether a bank customer will churn using an Artificial Neural Network (ANN). This repository contains a trained Keras model, preprocessing artifacts, example notebooks, and a small Streamlit app to try predictions locally.

## Contents

- `app.py` — Streamlit app to run the model and interactively predict customer churn.
- `model.h5` — Trained Keras/TensorFlow model (saved weights + architecture).
- `Churn_Modelling.csv` — Original dataset used for training / experimentation.
- `requirements.txt` — Python dependencies used by the project.
- `venv/` — (local) Python virtual environment (not always present in other clones).
- `run_streamlit.ps1` — PowerShell helper that activates `venv` (if present) and runs Streamlit.
- `label_encoder_gender.pkl`, `onehot_encoder_geo.pkl`, `scaler.pkl` — preprocessing artifacts used by `app.py` and notebooks.
- `exp.ipynb`, `prediction.ipynb` — Jupyter notebooks for experiments and prediction examples.
- `logs/` — TensorBoard logs (training/validation) created during model training.

## Goal

Build and expose a lightweight web UI for predicting customer churn from a set of features using a pre-trained ANN. The app demonstrates preprocessing, loading the model, and serving predictions.

## Quick start (Windows / PowerShell)

Recommended: use the included `venv` if it's present, or create one and install dependencies.

1) From project root open PowerShell.

2) If you already have a `venv` folder in the repo (this project shows `venv/`), run the helper script which attempts to activate the venv and run Streamlit:

```powershell
& 'C:\Users\ptani\OneDrive\Desktop\ANNproject\run_streamlit.ps1'
```

3) If you prefer to explicitly use the venv python (works even if activation fails):

```powershell
& 'C:\Users\ptani\OneDrive\Desktop\ANNproject\venv\python.exe' -m pip install -r requirements.txt
& 'C:\Users\ptani\OneDrive\Desktop\ANNproject\venv\python.exe' -m streamlit run 'C:\Users\ptani\OneDrive\Desktop\ANNproject\app.py'
```

4) If you don't have a `venv` and want to create one now:

```powershell
# create and activate a new venv (PowerShell)
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
& .\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Notes:
- If you see `The term 'streamlit' is not recognized...`, either activate the venv first or run Streamlit via `python -m streamlit`. On Windows PowerShell, activation is done with `& .\venv\Scripts\Activate.ps1`.
- If you installed Streamlit into a different Python than the one your terminal uses, re-install into the project venv or run Streamlit via the venv's python.
- If the app fails during preprocessing, verify that the encoder/scaler `.pkl` files exist and were created with the same feature ordering used by `app.py`.

## How the app works (high level)

1. `app.py` loads preprocessing artifacts (`scaler.pkl`, label/onehot encoders) and `model.h5`.
2. User inputs (via the Streamlit UI) are preprocessed to match training-time features (encoding, scaling).
3. The processed vector is fed to the Keras model and a predicted probability of churn is shown.

## Using the model in Python

Example snippet to run predictions (from project root):

```python
import pickle
from tensorflow.keras.models import load_model
import numpy as np

# load artifacts
scaler = pickle.load(open('scaler.pkl', 'rb'))
gender_le = pickle.load(open('label_encoder_gender.pkl', 'rb'))
geo_ohe = pickle.load(open('onehot_encoder_geo.pkl', 'rb'))
model = load_model('model.h5')

# Example: build an input array (match features used by training)
X_raw = [/* raw values in the same order your app uses */]
X_pre = ... # apply encoders and scaler
pred = model.predict(np.array([X_pre]))
print('churn probability =', pred[0,0])
```

See `app.py` and `prediction.ipynb` for the exact preprocessing order and code.

## Dataset

`Churn_Modelling.csv` contains the customer records used for experiments. Typical fields include customer demographics, balance, tenure, number of products, whether the customer has a credit card, active membership status, estimated salary, geography, gender, and whether they left (churn). Use the notebooks to explore column names and preprocessing steps.

## Notebooks

- `exp.ipynb` — training/experiment notebook (feature engineering, training loops, TensorBoard logging).
- `prediction.ipynb` — demonstrates loading the model + artifacts and running example predictions.

## Troubleshooting

- Streamlit command not found: either activate the venv or run `python -m streamlit`. On Windows PowerShell, activation is done with `& .\venv\Scripts\Activate.ps1`.
- If you installed Streamlit into a different Python than the one your terminal uses, re-install into the project venv or run Streamlit via the venv's python.
- If the app fails during preprocessing, verify that the encoder/scaler `.pkl` files exist and were created with the same feature ordering used by `app.py`.

## Re-training the model

If you want to re-train from the raw CSV:

1. Open `exp.ipynb` and follow the cells for preprocessing and training.
2. Save the new model to `model.h5` and export updated encoders/scalers using `pickle`.
3. Update `requirements.txt` if you add/change libraries.

## Development notes

- The repo contains `logs/` for TensorBoard. To view training metrics locally:

```powershell
# example
tensorboard --logdir logs/train
```

## License & contact

This repository is provided as-is for learning and demonstration. If you have questions or want help running the app, open an issue or contact the maintainer in the repository.

---

If anything in this README is unclear or you want me to add step-by-step screenshots, CI instructions, or a `run_streamlit.bat` for Windows cmd, tell me which and I'll add it.
