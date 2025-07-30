# Superior Scoring Rules: Enhanced Calibrated Metrics for Probabilistic Evaluation
[GitHub](https://github.com/Ruhallah93/superior-scoring-rules), [arXiv Preprint](https://arxiv.org/pdf/2407.17697)

`superior-scoring-rules` is a Python library that provides **strictly proper**, **confidence-aware evaluation metrics** for **probabilistic multi-class classification**. Unlike traditional metrics such as Brier Score or Log Loss, these scoring rules penalize **overconfident mispredictions**, ensuring **correct predictions are always scored better**.

---

## Why Accuracy, F1, Brier Score, and Log-Loss Fall Short in Probabilistic Classification

In many high-stakes applications, **confidence calibration** is critical. Traditional accuracy-based metrics (Accuracy, F1) ignore prediction confidence. Consider:

* **Cancer Diagnosis**: Differentiating 51% vs. 99% confidence in malignancy
* **ICU Triage**: Overconfident mispredictions risk patient safety
* **Autonomous Vehicles**: Handling uncertainties about obstacles
* **Financial Risk Modeling**: Pricing and investment decisions
* **Security Threat Detection**: High-confidence false negatives

**Accuracy** or **F1** score alone cannot capture this nuance.

## Problem with Traditional Metrics  
Accuracy-based metrics (Accuracy, F1) treat all correct predictions equally, ignoring confidence. In high-stakes domains, confidence calibration is critical:

- Cancer Diagnosis: 51% vs. 99% confidence in malignancy should not be treated differently.

- ICU Triage & Mortality: Overconfident mispredictions risk patient safety.

- Autonomous Vehicles: Decisions depend on uncertainty about obstacles.

- Financial Risk Modeling: Pricing and investment hinge on calibrated probabilities.

- Security Threat Detection: High-confidence false negatives undermine defenses.

Thus, Accuracy or F1 Score alone is insufficient: they ignore the confidence of predictions.

## Limitations of MSE & Cross-Entropy

Mean Squared Error (Brier Score) and Cross-Entropy (Log Loss) are strictly proper scoring rules, rewarding calibration. However, they can still favor incorrect predictions over correct ones. Example: 

| Vector | True Label (Y) | Predicted Probabilities (P) | Brier Score | Log Loss | State |
|--------|----------------|-----------------------------|-------------|----------|-------|
| **`A`**  | `[0, 1, 0]`    | `[0.33, 0.34, 0.33]`        | 0.6534      | 0.4685   |   Correct |
| **`B`**  | `[0, 1, 0]`    | `[0.51, 0.49, 0.00]`        | 0.5202      | 0.3098   |   Incorrect |  

Both MSE and Log Loss favor B over A, contradicting the principle of rewarding correct predictions.

## Our Solution: PBS & PLL  
To ensure correct predictions always receive better scores, we introduce a penalty term for misclassifications:

- **Penalized Brier Score (PBS)**

- **Penalized Logarithmic Loss (PLL)**

These metrics are both strictly proper and superior (never favor wrong over right).


## Quick Start

### Installation from PyPI
```bash
pip install superior-scoring-rules
```

### Install from Source (Development)
Clone the repository:
```bash
git clone https://github.com/Ruhallah93/superior-scoring-rules.git
```


### Basic Usage
```python
import tensorflow as tf
from superior_scoring_rules import pbs, pll

# Sample data (batch_size=3, num_classes=4)
y_true = tf.constant([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
y_pred = tf.constant([[0.9, 0.05, 0.05, 0], 
                     [0.1, 0.8, 0.05, 0.05],
                     [0.1, 0.1, 0.1, 0.7]])

print("PBS:", pbs(y_true, y_pred).numpy())
print("PLL:", pll(y_true, y_pred).numpy())
```

### Early Stopping & Checkpointing
Use PBS/PLL instead of val_loss:
```python
class PBSCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        logs['val_pbs'] = pbs(self.validation_data[1], self.model.predict(self.validation_data[0]))
        # or
        logs['val_pll'] = pll(self.validation_data[1], self.model.predict(self.validation_data[0]))

model.fit(..., callbacks=[PBSCallback(),
    tf.keras.callbacks.EarlyStopping(monitor='val_pbs', patience=5, mode='min'),
    tf.keras.callbacks.ModelCheckpoint('best.h5', monitor='val_pbs', save_best_only=True)
])
```

## Paper & Citation

- [Superior scoring rules for probabilistic evaluation of single-label multi-class classification tasks](https://www.sciencedirect.com/science/article/abs/pii/S0888613X25000623)

- arXiv: [2407.17697](https://arxiv.org/pdf/2407.17697)

```
@article{ahmadian2025superior,
  title={Superior scoring rules for probabilistic evaluation of single-label multi-class classification tasks},
  author={Ahmadian, Rouhollah and Ghatee, Mehdi and Wahlstr{\"o}m, Johan},
  journal={International Journal of Approximate Reasoning},
  pages={109421},
  year={2025},
  publisher={Elsevier}
}
```
---

## Related Topics

- Probabilistic classification evaluation
- Strictly proper scoring rules in machine learning
- Calibrated metrics for deep learning
- TensorFlow / Keras custom evaluation metrics
- AI safety and confidence in model predictions
- Penalized loss functions for classification

