# Solar Energy Output Predictor

Predict how much sunlight hits a solar panel in Kerala, India, using 5 weather features and a Random Forest model.

**Built as a learning project** to practice the full ML pipeline: data collection → cleaning → modeling → API → Docker → deployment.

---

## What it does

You give it current weather conditions:

```json
{
  "clouds": 20,
  "temperature": 32,
  "humidity": 50,
  "rain": 0,
  "hour": 12
}
```

It returns predicted solar irradiance:

```json
{
  "predicted_sunlight_wm2": 847.3
}
```

---

## Results

| Model | RMSE (W/m²) | MAE (W/m²) | R² |
|-------|-------------|------------|------|
| Linear Regression | — | — | — |
| **Random Forest** | — | — | — |

*(Fill these in after running notebook 02)*

Trained on Jan–Oct 2022, tested on Nov–Dec 2022 (chronological split, no data leakage).

---

## Tech stack

- **Data source:** Open-Meteo API (free, no key needed)
- **Language:** Python 3.10
- **Data handling:** Pandas
- **ML:** Scikit-learn (Linear Regression, Random Forest)
- **API:** FastAPI
- **Containerization:** Docker
- **Deployment:** AWS EC2

---

## Features used (5 inputs)

| Feature | Why it matters |
|---------|---------------|
| Cloud cover (%) | Clouds block sunlight — the #1 predictor |
| Temperature (°C) | Hot clear days correlate with high solar output |
| Humidity (%) | Humid air scatters sunlight, reducing what reaches the panel |
| Rainfall (mm) | Rain = heavy clouds = very low output |
| Hour of day (0–23) | Sun follows a daily arc — zero at night, peak at noon |

---

## How to run

### Option 1: Run locally

```bash
git clone https://github.com/YOUR_USERNAME/solar-predictor.git
cd solar-predictor
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.api:app --port 8000
```

Then open http://localhost:8000/docs to test.

### Option 2: Run with Docker

```bash
docker build -t solar-predictor .
docker run -p 8000:8000 solar-predictor
```

### Option 3: Run the notebooks

```bash
pip install jupyter
jupyter notebook
```

Open notebooks in order: `01_get_data.ipynb` → `02_train_model.ipynb` → `03_build_api.ipynb`

---

## Project structure

```
solar-predictor/
├── data/
│   ├── raw/                  # Downloaded from Open-Meteo
│   └── processed/            # Cleaned + charts
├── notebooks/
│   ├── 01_get_data.ipynb     # Download, clean, visualize
│   ├── 02_train_model.ipynb  # Train and compare models
│   └── 03_build_api.ipynb    # Build API + Dockerfile
├── src/
│   └── api.py                # FastAPI application
├── models/
│   ├── solar_model.pkl       # Trained Random Forest
│   └── feature_columns.json  # Feature names
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Why this project is (mostly) pointless

I want to be upfront about what this project **cannot** do and why.

### The core problem

This model predicts **current** sunlight from **current** weather. That's not useful in the real world because:

1. **If you have current weather data, you already have current sunlight data.** They come from the same sensors and APIs. There is no scenario where you know today's cloud cover but don't know today's solar irradiance — Open-Meteo gives you both in the same API call.

2. **Nobody needs a prediction of the present.** Solar farms need to know what happens **tomorrow** so they can report to the grid. A homeowner needs to know if they should run the washing machine now or wait for sun. Predicting the present answers no real question.

3. **The model is partially circular.** Cloud cover and solar irradiance are physically linked — clouds block sunlight. Teaching a model that "less clouds = more sun" is not discovering a pattern, it's restating physics. The R² score looks impressive, but it's inflated by this circularity.

### What would make it useful

A genuinely useful version would do one of these:

- **24-hour forecast:** Use today's weather to predict tomorrow's sunlight. This requires shifting the target variable by 24 hours (`df["target"] = df["sunlight"].shift(-24)`), which means the model learns patterns like "when it's humid today, it tends to be cloudy tomorrow."

- **Use weather forecasts as input:** Instead of current weather, feed in tomorrow's weather forecast from a service like Open-Meteo's forecast API and predict tomorrow's actual solar output. The value is that forecasts are imperfect, and the model could learn to correct systematic forecast errors.

- **Longer horizon:** Predict sunlight for the next 3–7 days to help with energy grid planning and battery storage decisions.

### So why did I build it this way?

This project exists to **learn and demonstrate the ML pipeline**, not to solve a real prediction problem. The skills it covers are real and transferable:

- Collecting data from an API
- Cleaning and exploring data with Pandas
- Training and comparing ML models
- Building a REST API with FastAPI
- Containerizing with Docker
- Deploying to AWS

The prediction problem is simple on purpose. I chose it so I could focus on learning the **engineering** around ML — the pipeline, the deployment, the infrastructure — rather than getting stuck on complex feature engineering or model tuning.

If I were to make this production-ready, the first thing I'd change is the problem framing: shift to forecasting, add lag features, and validate against a naive baseline (e.g., "tomorrow's sunlight = today's sunlight").

---

## What I learned

- How to pull data from a REST API and parse JSON into a DataFrame
- Why chronological train/test splits matter for time series (random splits leak future data)
- How Random Forest captures non-linear patterns that Linear Regression misses
- How to wrap a model in a FastAPI endpoint with input validation
- How Docker packages code + model + dependencies into a portable container
- Why a simple, honest project is better than a complex one you can't explain

---

## Location

Kochi, Kerala, India (9.93°N, 76.27°E)

Kerala is interesting for solar prediction because of its dramatic monsoon season (June–September), where cloud cover spikes and solar output drops significantly. This creates strong seasonal patterns in the data.

---

## License

MIT
