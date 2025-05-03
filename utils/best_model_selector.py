# best_model_selector.py

import os
import pandas as pd

# Ruta donde están los resultados de entrenamiento
RUNS_DIR = "runs/train"
POSSIBLE_METRICS = ["metrics/mAP50(B)", "metrics/mAP50-95(B)", "metrics/mAP_0.5", "metrics/mAP_0.5:0.95"]

def find_best_model(runs_dir, possible_metrics):
    best_value = -1
    best_run = None
    best_metric = None
    all_results = []

    for run in os.listdir(runs_dir):
        results_path = os.path.join(runs_dir, run, "results.csv")
        if os.path.isfile(results_path):
            df = pd.read_csv(results_path)
            for metric in possible_metrics:
                if metric in df.columns:
                    max_value = df[metric].max()
                    all_results.append((run, metric, max_value))
                    if max_value > best_value:
                        best_value = max_value
                        best_run = run
                        best_metric = metric
                    break  # No seguir buscando otras métricas
    if not best_run:
        print("  No se encontró ningún modelo con las métricas especificadas.")
        print(" Columnas encontradas en los CSV disponibles:")
        for run in os.listdir(runs_dir):
            results_path = os.path.join(runs_dir, run, "results.csv")
            if os.path.isfile(results_path):
                df = pd.read_csv(results_path)
                print(f"{run}: {list(df.columns)}")
        return

    print("\n Resultados de los entrenamientos:")
    for run, metric, val in sorted(all_results, key=lambda x: x[2], reverse=True):
        print(f"{run:30} -> {metric}: {val:.4f}")

    best_path = os.path.join(runs_dir, best_run, "weights", "best.pt")
    print("\n Mejor modelo:")
    print(f"{best_run} con {best_metric} = {best_value:.4f}")
    print(f" Pesos: {best_path}")

if __name__ == "__main__":
    find_best_model(RUNS_DIR, POSSIBLE_METRICS)
