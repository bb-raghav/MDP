# AI/ML Based Air Quality Downscaling System

## Project Overview

This project focuses on improving the spatial resolution of satellite-based air quality maps using Artificial Intelligence and Machine Learning techniques.

The system combines:
- Satellite air quality data
- Meteorological data
- Machine learning models

to generate more detailed and accurate air pollution predictions.

---

## Objectives

- Collect satellite and meteorological datasets
- Preprocess and clean environmental data
- Train ML/DL models for PM2.5 prediction
- Perform spatial downscaling of AQI maps
- Visualize predictions using plots and heatmaps

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Jupyter Notebook

Future tools:
- XGBoost
- Streamlit
- GeoPandas
- TensorFlow/PyTorch

---

## Project Structure

```bash
air-quality-downscaling/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── notebooks/
│
├── src/
│   ├── preprocessing/
│   ├── models/
│   ├── visualization/
│   └── utils/
│
├── outputs/
│   ├── plots/
│   └── predictions/
│
├── reports/
│
├── app/
│
├── requirements.txt
├── README.md
└── main.py
```

---

## Current Progress

- [x] GitHub repository initialized
- [x] Project structure created
- [ ] Dataset collection
- [ ] Data preprocessing
- [ ] Baseline ML model
- [ ] Visualization dashboard
- [ ] Model evaluation

---

## Team Responsibilities

### Core Development
- Data preprocessing
- Model training
- System integration

### Documentation & Presentation
- PPT preparation
- Final report
- Research paper drafting
- Demo preparation

---

## Setup Instructions

### Clone Repository

```bash
git clone <your_repo_url>
cd air-quality-downscaling
```

### Create Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Future Scope

- Real-time AQI prediction
- Deep learning-based super resolution
- Interactive pollution dashboard
- Multi-city deployment
- Web-based visualization platform

---

## License

Academic Project – For Educational Purposes