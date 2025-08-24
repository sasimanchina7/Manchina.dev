from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn.linear_model import LogisticRegression
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

pipe = Pipeline([
    ("smote", SMOTE(k_neighbors=5, random_state=42)),
    ("clf", LogisticRegression(class_weight=None, max_iter=1000, n_jobs=-1))
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
probs = cross_val_predict(pipe, X, y, cv=cv, method="predict_proba")[:,1]
ap = average_precision_score(y, probs)
prec, rec, thr = precision_recall_curve(y, probs)
# choose threshold that maximizes F1
import numpy as np
f1 = 2*prec[:-1]*rec[:-1]/(prec[:-1]+rec[:-1]+1e-12)
best_t = thr[np.argmax(f1)]
