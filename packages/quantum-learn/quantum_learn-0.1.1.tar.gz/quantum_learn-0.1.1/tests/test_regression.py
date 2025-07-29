import unittest
import numpy as np
import pandas as pd
from qlearn import HybridRegression

def simple_regression_dataset():
    # For regression, we encode the continuous target as a 1D numpy array.
    def encode(value):
        return np.array([value])
    data = pd.DataFrame({
        "feature1": [0, 1, 2, 3],
        "feature2": [1, 2, 3, 4],
        "label": [encode(v) for v in [0.0, 1.0, 2.0, 3.0]]
    })
    return data

class TestRegression(unittest.TestCase):
    def setUp(self):
        data = simple_regression_dataset()
        self.features = data[["feature1", "feature2"]]
        self.labels = data[["label"]]
        self.reg = HybridRegression()

    def test_train_and_predict(self):
        # Test that training sets the model and predict returns the correct number of outputs.
        self.reg.train(self.features, self.labels)
        self.assertIsNotNone(self.reg.model)
        predictions = self.reg.predict(self.features)
        self.assertEqual(len(predictions), len(self.features))

    def test_predict_without_training(self):
        # Expect a ValueError if predict is called without training.
        with self.assertRaises(ValueError):
            self.reg.predict(self.features)

if __name__ == "__main__":
    unittest.main()
