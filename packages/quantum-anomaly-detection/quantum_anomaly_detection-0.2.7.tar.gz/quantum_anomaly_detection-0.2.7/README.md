

Quantum Anomaly Detection is a Python package that leverages quantum computing (via Qiskit) to detect anomalies in datasets.


```bash
git clone https://github.com/MalekAlFakih/quantum-anomaly-detection.git
cd quantum-anomaly-detection
pip install -e .
```


```python
from quantum_anomaly_detection import QuantumAnomalyDetector
import numpy as np
data = np.random.rand(10, 2)
detector = QuantumAnomalyDetector()
detector.fit(data)
scores = detector.predict(data)
print("Scores:", scores)
```
