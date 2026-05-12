# AI/ML-Based Air Quality Downscaling System

## Overview

This project focuses on improving the spatial resolution and accuracy of air quality prediction using Machine Learning and geospatial environmental data.

The system combines:

- Ground station AQI measurements
- Satellite-derived environmental features
- Meteorological parameters
- Geospatial raster datasets

to build predictive models for Air Quality Index (AQI) classification and pollution analysis across Indian cities.

---

# Problem Statement

Satellite pollution maps provide broad regional coverage but often lack fine spatial resolution and local accuracy.

This project aims to:

- Combine satellite and ground-station data
- Extract meaningful environmental features
- Train ML models for AQI prediction
- Build a scalable air-quality intelligence pipeline
- Visualize pollution patterns interactively

---

# Current Dataset Features

The training dataset currently includes:

## Ground Station Features

- AQI
- PM2.5
- PM10
- Temperature
- Humidity
- Pressure
- Wind Speed
- Latitude
- Longitude

## Satellite / Raster Features

- AER (Aerosol Optical Depth)
- CO
- NO2
- SO2
- NDVI
- NightLights
- DEM
- LULC
- Population Density

---

# Project Architecture

```text
Raw Satellite Rasters
        ↓
Raster Feature Extraction
        ↓
Ground Station AQI Merge
        ↓
Training Dataset Preparation
        ↓
ML Model Training
        ↓
Prediction & Evaluation
        ↓
Visualization Dashboard
```

---

# Tech Stack

## Backend / ML

- Python
- Pandas
- NumPy
- Scikit-learn
- Rasterio
- GeoPandas
- SQLAlchemy
- Psycopg2
- Joblib

## Frontend

- React
- Vite
- Leaflet.js
- Tailwind CSS

## Database

- Neon PostgreSQL

---

# Project Structure

```bash
MDP/
│
├── app/                            # Frontend Dashboard
│   ├── public/
│   └── src/
│       ├── assets/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── styles/
│
├── backend/
│   ├── api/
│   ├── models/
│   │   └── train/
│   ├── preprocessing/
│   │   └── pipeline/
│   ├── utils/
│   └── visualization/
│
├── data/
│   ├── external/                  # Raw received datasets
│   ├── processed/                 # Cleaned training datasets
│   └── raw/
│       └── india/                 # Raster TIFF files
│
├── notebooks/
│
├── outputs/
│   ├── datasets/
│   ├── logs/
│   ├── models/
│   ├── plots/
│   └── predictions/
│
├── reports/
│
├── requirements.txt
├── .gitignore
├── README.md
└── main.py
```

---

# Current Progress

## Completed

- [x] Project architecture setup
- [x] Frontend AQI dashboard
- [x] Raster ingestion pipeline
- [x] Dataset cleaning pipeline
- [x] Ground + satellite data integration
- [x] AQI category generation
- [x] Feature engineering pipeline
- [x] Training dataset preparation
- [x] Neon PostgreSQL integration

## In Progress

- [ ] Baseline Random Forest model
- [ ] AQI prediction pipeline
- [ ] Feature importance analysis
- [ ] Model evaluation metrics

## Planned

- [ ] Real-time AQI prediction
- [ ] XGBoost implementation
- [ ] Spatial downscaling models
- [ ] Interactive GIS dashboard
- [ ] Multi-city deployment

---

# Machine Learning Pipeline

## Input Features

```text
temperature
humidity
pressure
wind_speed
AER
CO
DEM
LULC
NDVI
NightLights
NO2
POP
SO2
latitude
longitude
month
day
```

## Target Variable

```text
AQI Category
```

AQI categories include:

- Good
- Moderate
- Poor
- Severe

---

# Setup Instructions

## Clone Repository

```bash
git clone <your_repo_url>
cd MDP
```

---

## Create Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Frontend

```bash
cd app
npm install
npm run dev
```

---

# Run Backend Scripts

Example:

```bash
python backend/preprocessing/pipeline/prepare_training_data.py
```

---

# Research & Academic Scope

This system can be extended into:

- High-resolution AQI forecasting
- Satellite-based pollution downscaling
- AI-driven urban environmental intelligence
- Smart-city monitoring systems
- Public health analytics platforms

---

# Team Contributions

- Data preprocessing
- Raster handling
- ML pipeline development
- Frontend dashboard development
- Database integration
- Documentation & reporting

---

# License

Academic Project — Educational & Research Use Only