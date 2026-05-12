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