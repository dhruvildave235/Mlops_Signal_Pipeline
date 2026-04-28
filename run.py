
import argparse
import yaml
import pandas as pd
import numpy as np
import logging
import time
import json
import sys
import os

def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def load_config(path):
    if not os.path.exists(path):
        raise Exception("Config file not found")
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise Exception("Invalid config structure")

    for key in ["seed", "window", "version"]:
        if key not in config:
            raise Exception(f"Missing config field: {key}")

    return config

def load_data(path):
    if not os.path.exists(path):
        raise Exception("Input file not found")

    try:
        df = pd.read_csv(path)
    except Exception:
        raise Exception("Invalid CSV format")

    if df.empty:
        raise Exception("Empty dataset")

    df.columns = [c.strip().lower() for c in df.columns]

    if "close" not in df.columns:
        raise Exception("Missing required column: close")

    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    setup_logger(args.log_file)
    start_time = time.time()

    try:
        logging.info("Job started")

        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)
        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        df = load_data(args.input)
        logging.info(f"Rows loaded: {len(df)}")

        # Rolling mean
        logging.info("Computing rolling mean")
        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        # Signal generation
        logging.info("Generating signal")
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

        valid_df = df.dropna()
        signal_rate = valid_df["signal"].mean()

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": int(len(df)),
            "metric": "signal_rate",
            "value": float(round(signal_rate, 4)),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        logging.info(f"Metrics summary: {metrics}")

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)

        print(json.dumps(metrics))

        logging.info("Job completed successfully")
        sys.exit(0)

    except Exception as e:
        logging.error(str(e))

        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=2)

        print(json.dumps(error_output))
        sys.exit(1)

if __name__ == "__main__":
    main()
