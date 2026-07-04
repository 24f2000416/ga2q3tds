from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import yaml
import os

load_dotenv()

app = FastAPI()

# Allow browser requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Defaults ----------------

config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000"
}

# ---------------- YAML ----------------

with open("config.development.yaml") as f:
    config.update(yaml.safe_load(f))

# ---------------- .env ----------------

if os.getenv("APP_PORT"):
    config["port"] = int(os.getenv("APP_PORT"))

if os.getenv("APP_DEBUG"):
    config["debug"] = os.getenv("APP_DEBUG").lower() in [
        "true",
        "1",
        "yes",
        "on"
    ]

if os.getenv("APP_LOG_LEVEL"):
    config["log_level"] = os.getenv("APP_LOG_LEVEL")

if os.getenv("APP_API_KEY"):
    config["api_key"] = os.getenv("APP_API_KEY")

# Alias
if os.getenv("NUM_WORKERS"):
    config["workers"] = int(os.getenv("NUM_WORKERS"))

# ---------------- OS ENV ----------------

for key in ["PORT", "DEBUG", "LOG_LEVEL", "API_KEY"]:

    env = os.getenv("APP_" + key)

    if env is None:
        continue

    if key == "PORT":
        config["port"] = int(env)

    elif key == "DEBUG":
        config["debug"] = env.lower() in [
            "true",
            "1",
            "yes",
            "on"
        ]

    elif key == "LOG_LEVEL":
        config["log_level"] = env

    elif key == "API_KEY":
        config["api_key"] = env


@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):

    final = config.copy()

    for item in set:

        if "=" not in item:
            continue

        key, value = item.split("=", 1)

        if key in ["port", "workers"]:
            final[key] = int(value)

        elif key == "debug":
            final[key] = value.lower() in [
                "true",
                "1",
                "yes",
                "on"
            ]

        else:
            final[key] = value

    final["api_key"] = "****"

    return final