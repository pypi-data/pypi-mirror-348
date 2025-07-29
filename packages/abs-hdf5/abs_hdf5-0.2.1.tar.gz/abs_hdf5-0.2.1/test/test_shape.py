from abs.utils import *
from abs.part_processor import *
import unittest
from abs.topology import Face
import os

def get_normal_func(part, topo, points):
    if isinstance(topo, Face):
        return topo.normal(points)
    else:
        return None





class TestShapeFunctions(unittest.TestCase):

    def test_get_parts_integration(self):
        name = 'Cone'
        sample_name = f'{name}.hdf5'
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_hdf5', sample_name)
        file_path = os.path.normpath(file_path)

        num_samples = 5000

        parts = read_parts(file_path)

        P, S = sample_parts(parts, num_samples, get_normal_func)
        save_file_path = os.path.join(os.path.dirname(__file__), '..', 'test', 'sample_results', f'{name}_normals.obj')

        # save_ply(save_file_path, P, S)
        # save_obj(save_file_path, P)

        self.assertEqual(len(P), len(parts))
        self.assertEqual(len(S), len(parts))

        self.assertEqual(len(P), len(S))

if __name__ == '__main__':
    unittest.main()
