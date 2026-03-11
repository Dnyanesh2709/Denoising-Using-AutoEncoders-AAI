# 🧠 Denoise Studio — Convolutional Autoencoder

> Neural image reconstruction powered by a Convolutional Autoencoder.

Built with Python, Streamlit, Keras 3 and TensorFlow.

---

## 👥 Team

Made with ♥ by **Charmi Jani**, **Tejashree Karekar** and **Dnyanesh Panchal**

---

## 📌 What is Denoise Studio?

Denoise Studio is a deep learning web app that takes a noisy or corrupted image as input and reconstructs a clean version using a trained Convolutional Autoencoder. The model compresses the image into a compact latent representation and then decodes it back — removing noise in the process.

---

## 🚀 Features

- Upload any noisy image (PNG / JPG)
- Automatically resizes to 28×28 grayscale for model input
- Runs inference using a trained Keras autoencoder
- Side-by-side comparison of noisy input vs denoised output
- Displays PSNR, MSE and Peak Activation metrics
- Download the denoised image as PNG
- Sleek dark-themed editorial UI

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Deep Learning | Keras 3 / TensorFlow |
| Model Type | Convolutional Autoencoder |
| Image Processing | Pillow, NumPy |
| Deployment | Streamlit Cloud |

---

## 🧬 Model Architecture

The autoencoder is a Sequential Keras model trained on 28×28 grayscale images.

**Encoder:**
- Conv2D — 16 filters, 3×3 kernel, stride 2, same padding
- Conv2D — 8 filters, 3×3 kernel, stride 2, same padding
- Conv2D — 8 filters, 3×3 kernel, stride 1, same padding

**Decoder:**
- Conv2DTranspose — 16 filters, 3×3 kernel, stride 2, same padding
- Conv2DTranspose — 1 filter, 3×3 kernel, stride 2, sigmoid activation

**Training:**
- Loss: Binary Crossentropy
- Input shape: 28 × 28 × 1
- Saved with Keras 3.10.0

---

## 📁 Project Structure

```
denoise-studio/
├── app2.py                 # Streamlit frontend
├── denoise_model.keras     # Trained autoencoder model
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version for Streamlit Cloud
├── .python-version         # Python version pin
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/denoise-studio.git
cd denoise-studio
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app2.py
```

Open your browser at `http://localhost:8501`

---

## 📊 Metrics Explained

| Metric | Description |
|---|---|
| PSNR (dB) | Peak Signal-to-Noise Ratio — higher is better |
| MSE Loss | Mean Squared Error between input and output — lower is better |
| Peak Activation | Maximum pixel activation value in the decoded output |

---

## 🌐 Deployment

This app is deployed on **Streamlit Cloud** using Python 3.11.

To deploy your own:
1. Push all files including `denoise_model.keras` to a public GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app2.py` as the main file
5. Set Python version to **3.11** in Advanced Settings
6. Deploy!

---

## 📦 Requirements

```
streamlit
numpy
pillow
keras==3.10.0
tensorflow
```

---

## 📄 License

This project is for educational purposes only.
