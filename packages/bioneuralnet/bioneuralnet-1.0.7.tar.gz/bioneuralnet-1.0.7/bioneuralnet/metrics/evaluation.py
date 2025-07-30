import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score, f1_score
from xgboost import XGBClassifier, XGBRegressor
from bioneuralnet.utils import get_logger

logger = get_logger(__name__)

def evaluate_model(X: np.ndarray,y: np.ndarray,model_type: str = "rf_classif",n_estimators: int = 150,runs: int = 100,seed: int = 119,):
    """
    Evaluate a single model (RF or XGB, classif or reg) over multiple runs, returning three tuples.
    For classification:

      - (accuracy_mean, accuracy_std)
      - (f1_weighted_mean, f1_weighted_std)
      - (f1_macro_mean, f1_macro_std)
    
    For regression:

      - (r2_mean, r2_std)
      - (None, None)
      - (None, None)
    """
    accs, f1ws, f1ms, rsqs = [], [], [], []
    is_classif = "classif" in model_type

    for run in range(runs):
        stratify = y if is_classif else None
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=0.3, random_state=seed + run, stratify=stratify
        )

        if model_type == "rf_classif":
            mdl = RandomForestClassifier(n_estimators=n_estimators, random_state=seed + run)
        elif model_type == "xgb_classif":
            mdl = XGBClassifier( n_estimators=n_estimators, eval_metric="logloss", random_state=seed + run)
        elif model_type == "rf_reg":
            mdl = RandomForestRegressor(n_estimators=n_estimators, random_state=seed + run)
        elif model_type == "xgb_reg":
            mdl = XGBRegressor(n_estimators=n_estimators, random_state=seed + run)
        else:
            raise ValueError("model_type must be one of: rf_classif, xgb_classif, rf_reg, xgb_reg")

        mdl.fit(X_tr, y_tr)
        y_pred = mdl.predict(X_te)

        if is_classif:
            accs.append(accuracy_score(y_te, y_pred))
            f1ws.append(f1_score(y_te, y_pred, average="weighted"))
            f1ms.append(f1_score(y_te, y_pred, average="macro"))
        else:
            rsqs.append(r2_score(y_te, y_pred))

    if is_classif:
        return (
            (np.mean(accs), np.std(accs)),
            (np.mean(f1ws), np.std(f1ws)),
            (np.mean(f1ms), np.std(f1ms)))
    else:
        return (
            (np.mean(rsqs), np.std(rsqs)),
            (None, None),
            (None, None))

def evaluate_single_run(X: np.ndarray,y: np.ndarray,model_type: str = "rf_classif",n_estimators: int = 100,test_size: float = 0.3,seed: int = 119):
    """
    Do one train/test split, train the specified model.
      
    Return: (accuracy, f1_weighted, f1_macro)
    """
    stratify = y if "classif" in model_type else None
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=test_size, random_state=seed, stratify=stratify)

    if model_type == "rf_classif":
        mdl = RandomForestClassifier(n_estimators=n_estimators, random_state=seed)
    elif model_type == "xgb_classif":
        mdl = XGBClassifier(n_estimators=n_estimators,eval_metric="logloss",random_state=seed)
    else:
        raise ValueError("model_type must be 'rf_classif' or 'xgb_classif'")

    mdl.fit(X_tr, y_tr)
    y_pred = mdl.predict(X_te)

    acc  = accuracy_score(y_te, y_pred)
    f1w  = f1_score(y_te, y_pred, average="weighted")
    f1m  = f1_score(y_te, y_pred, average="macro")

    return acc, f1w, f1m

def evaluate_rf(X: np.ndarray,y: np.ndarray,mode: str = "classification",n_estimators: int = 150,runs: int = 100,seed: int = 119,return_all: bool = False):
    """
    Shortcut function: evaluate a RandomForest (classification or regression).
    """
    mt = "rf_classif" if mode == "classification" else "rf_reg"
    return evaluate_model(X, y, model_type=mt, n_estimators=n_estimators,runs=runs, seed=seed, return_all=return_all)

def evaluate_xgb(X: np.ndarray,y: np.ndarray,mode: str = "classification",n_estimators: int = 150,runs: int = 100,seed: int = 119,return_all: bool = False):
    """
    Shortcut function: evaluate an XGBoost (classification or regression).
    """

    mt = "xgb_classif" if mode == "classification" else "xgb_reg"
    return evaluate_model(X, y, model_type=mt, n_estimators=n_estimators, runs=runs, seed=seed, return_all=return_all)

def evaluate_f1w(X: np.ndarray,y: np.ndarray,model_type: str = "rf_classif",n_estimators: int = 100,runs: int = 5,seed: int = 119):
    """
    Evaluate weighted F1-score over multiple runs.
    """
    scores = []
    for run in range(runs):
        stratify = y if "classif" in model_type else None
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=seed+run, stratify=stratify)
        if model_type == "rf_classif":
            mdl = RandomForestClassifier(n_estimators=n_estimators, random_state=seed+run)
        elif model_type == "xgb_classif":
            mdl = XGBClassifier(n_estimators=n_estimators,eval_metric="logloss",random_state=seed+run)
        else:
            raise ValueError("Unsupported model_type for F1 scoring")
        
        mdl.fit(X_train, y_train)
        y_pred = mdl.predict(X_test)
        scores.append(f1_score(y_test, y_pred, average="weighted"))

    return np.mean(scores), np.std(scores)

def evaluate_f1m(X: np.ndarray,y: np.ndarray,model_type: str = "rf_classif",n_estimators: int = 100,runs: int = 5,seed: int = 119):
    """Evaluate macro F1-score over multiple runs."""
    scores = []
    for run in range(runs):
        stratify = y if "classif" in model_type else None

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=seed+run, stratify=stratify)

        if model_type == "rf_classif":
            mdl = RandomForestClassifier(n_estimators=n_estimators, random_state=seed+run)
        elif model_type == "xgb_classif":
            mdl = XGBClassifier(n_estimators=n_estimators,eval_metric="logloss",random_state=seed+run)
        else:
            raise ValueError("Unsupported model_type for F1 scoring")
        
        mdl.fit(X_train, y_train)
        y_pred = mdl.predict(X_test)
        scores.append(f1_score(y_test, y_pred, average="macro"))

    return np.mean(scores), np.std(scores)

def plot_grouped_performance(scores: dict[str, dict[str, tuple[float, float]]],title: str,ylabel: str = "Score",filename: str | Path = None):
    """
    Plot grouped bar chart and save results to text file.
    """

    logger.info(f"Plotting grouped performance: {title}")
    groups = list(scores.keys())
    sublabels = list(next(iter(scores.values())).keys())
    means = []
    errs = []
    for g in groups:
        row_m = []
        row_e = []
        for s in sublabels:
            m, e = scores[g][s]
            row_m.append(m)
            row_e.append(e)
        means.append(row_m)
        errs.append(row_e)
    means = np.array(means)
    errs = np.array(errs)
    ind = np.arange(len(groups))
    width = 0.8 / len(sublabels)

    fig, ax = plt.subplots(figsize=(1.2*len(groups), 4))
    for i, s in enumerate(sublabels):
        ax.bar(
            ind + i*width,
            means[:, i],
            width,
            yerr=errs[:, i],
            capsize=3,
            label=s
        )
    ax.set_xticks(ind + width*(len(sublabels)-1)/2)
    ax.set_xticklabels(groups, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, pad=12)
    if "Accuracy" in ylabel or "F1" in ylabel:
        ax.set_ylim(0, 1)
    ax.legend(title="Method", fontsize=10)
    ax.grid(True, axis="y", linestyle="--", alpha=0.3)
    for i in range(len(groups)):
        for j in range(len(sublabels)):
            x = ind[i] + j*width
            h = means[i, j]
            e = errs[i, j]
            ax.text(x + width/2, h + e + 0.01, f"{h:.3f}", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()

    if filename:
        fig_path = Path(filename)
        txt_path = fig_path.with_suffix('.txt')
        with open(txt_path, 'w') as f:
            for g in groups:
                for s in sublabels:
                    m, e = scores[g][s]
                    f.write(f"{g}\t{s}\t{m:.3f}\t{e:.3f}\n")
        logger.info(f"Saved results to {txt_path}")
        fig.savefig(str(fig_path), dpi=300)
        logger.info(f"Saved plot to {fig_path}")
    plt.show()

def plot_multiple_metrics(metrics: dict[str, dict[str, dict[str, tuple[float, float]]]],title_map: dict[str, str] = None,ylabel_map: dict[str, str] = None,filename: Path = None):
    """
    Consolidate multiple metric grouped performances into one figure.

    Adds numeric labels on top of each bar.
    """
    logger.info(f"Plotting multiple metrics: {list(metrics.keys())}")
    n = len(metrics)
    fig, axes = plt.subplots(1, n, figsize=(5*n, 5), sharey=True)
    if n == 1:
        axes = [axes]

    for ax, (metric, sc) in zip(axes, metrics.items()):
        groups = list(sc.keys())
        sublabels = list(next(iter(sc.values())).keys())

        means = []
        errs = []

        for g in groups:
            rm = []
            re = []

            for s in sublabels:
                m, e = sc[g][s]
                rm.append(m)
                re.append(e)

            means.append(rm)
            errs.append(re)

        means = np.array(means)
        errs = np.array(errs)
        ind = np.arange(len(groups))
        total = 0.7
        width = total / len(sublabels)

        # plot bars and annotate
        for i in range(len(sublabels)):
            x = ind + i * width
            y = means[:, i]
            yerr = errs[:, i]

            bars = ax.bar(x, y, width, yerr=yerr, capsize=3, label=sublabels[i])

            # add value labels
            for bar in bars:
                height = bar.get_height()
                x = bar.get_x() + bar.get_width() / 2
                y = height + 0.01
                label = f"{height:.2f}"

                ax.text(x,y,label,ha='center', va='bottom', fontsize=8)

        ax.set_xticks(ind + total/2 - width/2)
        ax.set_xticklabels(groups, fontsize=11)

        if title_map:
            title = title_map.get(metric, metric)
        else:
            title = metric
        ax.set_title(title, fontsize=14, pad=12)

        if ylabel_map:
            ylabel = ylabel_map.get(metric, metric)
        else:
            ylabel = metric

        ax.set_ylabel(ylabel, fontsize=12)

        if "Accuracy" in ylabel or "F1" in ylabel:
            ax.set_ylim(0, 1)

        ax.legend(title="Method", fontsize=9)
        ax.grid(True, axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout(pad=2.0)

    if filename:
        fig.savefig(str(filename), dpi=300, bbox_inches="tight")
        logger.info(f"Saved combined figure to {filename}")

    plt.close(fig)
