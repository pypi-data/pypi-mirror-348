import unittest
import numpy as np
from ecocrop import EcocropModel

class TestEcocropModel(unittest.TestCase):

    def setUp(self):
        self.model = EcocropModel()
        self.model.set_parameter('tmin', [8])
        self.model.set_parameter('topmin', [18])
        self.model.set_parameter('topmax', [30])
        self.model.set_parameter('tmax', [40])
        self.model.set_parameter('pmin', [300])
        self.model.set_parameter('popmin', [500])
        self.model.set_parameter('popmax', [800])
        self.model.set_parameter('pmax', [1200])
        self.model.set_predictor('temperature', np.full((5, 5), 25))
        self.model.set_predictor('precipitation', np.full((5, 5), 600))

    def test_run_suitability_range(self):
        suitability = self.model.run()
        self.assertTrue(np.all((suitability >= 0) & (suitability <= 1)))

    def test_run_output_shape(self):
        suitability = self.model.run()
        self.assertEqual(suitability.shape, (5, 5))

if __name__ == '__main__':
    unittest.main()
