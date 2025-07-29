import numpy as np
from abs.curve import *
from abs.surface import *
import os
from pathlib import Path

def get_file(sample_name):
    return os.path.abspath(os.path.join(Path(__file__), '..', '..', 'data', 'sample_hdf5', sample_name))

class H5Dataset:
    def __init__(self, value):
        self.value = value

    def __getitem__(self, key):
        if key == ():
            return self.value

        elif isinstance(key, str) and isinstance(self.value, (list, np.ndarray)):
            try:
                index = int(key)
                return H5Dataset(self.value[index])
            except (ValueError, IndexError):
                return None
        return None

    def __len__(self):
        return len(self.value)

class H5Group:
    def __init__(self, data_dict):
        self._data = {
            k: H5Group(v) if isinstance(v, dict) else H5Dataset(
                v.encode('utf-8') if isinstance(v, str) else np.array(v)
            )
            for k, v in data_dict.items()
        }

    def get(self, key):
        return self._data.get(key)

    def __contains__(self, key):
        return key in self._data

    def __getitem__(self, key):
        return self._data[key]









def line3d():
    data = {
        "type": "Line",
        "location": [0, 0, 0],
        "direction": [1, 0, 0],
        "interval": [0, 1],
        "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    }
    data = H5Group(data)
    return Line(data)


def line2d():
    data = {
        "type": "Line",
        "location": [0, 0],
        "direction": [1, 0],
        "interval": [0, 1]
    }

    data = H5Group(data)
    return Line(data)


def circle3d():
    data = {
        "type": "Circle",
        "location": [0, 0, 0],
        "radius": 1.0,
        "interval": [0, 2 * np.pi],
        "x_axis": [1, 0, 0],
        "y_axis": [0, 1, 0],
        "z_axis": [0, 0, 1],
        "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    }

    data = H5Group(data)
    return Circle(data)


def circle2d():
    data = {
        "type": "Circle",
        "location": [0, 0],
        "radius": 1.0,
        "interval": [0, 2 * np.pi],
        "x_axis": [1, 0],
        "y_axis": [0, 1]
    }

    data = H5Group(data)
    return Circle(data)


def ellipse3d():
    data = {
        "type": "Ellipse",
        "focus1": [0, 0, 0],
        "focus2": [1, 0, 0],
        "interval": [0, 1],
        "maj_radius": 1.0,
        "min_radius": 0.5,
        "x_axis": [1, 0, 0],
        "y_axis": [0, 1, 0],
        "z_axis": [0, 0, 1],
        "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    }

    data = H5Group(data)
    return Ellipse(data)


def ellipse2d():
    data = {
        "type": "Ellipse",
        "focus1": [0, 0],
        "focus2": [1, 0],
        "interval": [0, 1],
        "maj_radius": 1.0,
        "min_radius": 0.5,
        "x_axis": [1, 0],
        "y_axis": [0, 1]
    }

    data = H5Group(data)
    return Ellipse(data)


def bspline_curve3d():
    data = {
        "type": "BSplineCurve",
        "closed": False,
        "continuity": 6,
        "degree": 1,
        "interval": [-3.512e-17, 1.000e+0],
        "knots": [-3.512e-17, -3.512e-17, 1.000e+0, 1.000e+0],
        "poles": [[4.217e+0, -2.184e+1, 2.540e+1], [4.217e+0, -2.184e+1, 5.080e+1]],
        "rational": False,
        "weights": [1.000e+0, 1.000e+0],
        "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
        "periodic": False
    }

    data = H5Group(data)
    return BSplineCurve(data)


def bspline_curve2d():
    data = {
        "type": "BSplineCurve",
        "closed": False,
        "continuity": 4,
        "degree": 3,
        "periodic": False,
        "interval": [3.46944695195361e-18, 0.00133425534020762],
        "knots": [3.46944695195361e-18, 3.46944695195361e-18, 3.46944695195361e-18, 3.46944695195361e-18,
                  6.0647970009440586e-05, 0.0001212959400188777, 0.0001819439100283148, 0.00024259188003775194,
                  0.00030323985004718907, 0.00036388782005662614, 0.00042453579006606327, 0.0004851837600755004,
                  0.0005458317300849375, 0.0006064797000943747, 0.0006671276701038117, 0.0007277756401132488,
                  0.000788423610122686, 0.0008490715801321231, 0.0009097195501415603, 0.0009703675201509973,
                  0.0010310154901604345, 0.0010916634601698715, 0.0011523114301793087, 0.0012129594001887459,
                  0.0012736073701981828, 0.00133425534020762, 0.00133425534020762, 0.00133425534020762,
                  0.00133425534020762],
        "poles": [[4.9650692355267685, 17.494250000000005],
                  [4.961032874370447, 17.49425],
                  [4.952977520669924, 17.493791778653545],
                  [4.940944974056901, 17.4917230120382],
                  [4.9289612766339115, 17.488266040182666],
                  [4.917024838625153, 17.483414092751246],
                  [4.905134098009328, 17.477160398261084],
                  [4.893287539849633, 17.46949818950921],
                  [4.881483643961395, 17.460420683320176],
                  [4.8697210821991295, 17.449921156128774],
                  [4.857997988472691, 17.43799266190103],
                  [4.846314687796942, 17.424629084868016],
                  [4.8346635160710045, 17.40982121066919],
                  [4.823066817519954, 17.393571389045626],
                  [4.811553478951728, 17.375897830257383],
                  [4.800122534023212, 17.35680718046304],
                  [4.78878115074683, 17.336309184412688],
                  [4.777534441903705, 17.31441275659142],
                  [4.766388184656843, 17.291127033953135],
                  [4.755348081572766, 17.266461093841347],
                  [4.744419948230315, 17.24042402957224],
                  [4.733609654800948, 17.213024930181962],
                  [4.722923127191439, 17.184272885853893],
                  [4.715885281266602, 17.164208952926344],
                  [4.712388980384689, 17.1539545256125]],
        "rational": False,
        "weights": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    }

    data = H5Group(data)
    return BSplineCurve(data)


def plane():
    data = {
        "type": "Plane",
        "coefficients": [1, 0, 0, 0],
        "location": [0, 0, 0],
        "trim_domain": [[0, 1], [0, 1]],
        "x_axis": [1, 0, 0],
        "y_axis": [0, 1, 0],
        "z_axis": [0, 0, 1],
        "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    }

    data = H5Group(data)
    return Plane(data)


def cylinder():
    data = {
        "type": "Cylinder",
        "location": [0, 0, 0],
        "radius": 1.0,
        "coefficients": [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1, 0.0, 0.5, 1],
        "trim_domain": [[0, 1], [0, 1]],
        "x_axis": [1, 0, 0],
        "y_axis": [0, 1, 0],
        "z_axis": [0, 0, 1],
        "transform":[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    }

    data = H5Group(data)
    return Cylinder(data)


def cone():
    data = {
        "type": "Cone",
        "angle": 0.5,
        "apex": [0, 0, 0],
        "coefficients": [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1, 0.0, 0.5, 1],
        "location": [0, 0, 0],
        "radius": 1.0,
        "trim_domain": [[0, 1], [0, 1]],
        "x_axis": [1, 0, 0],
        "y_axis": [0, 1, 0],
        "z_axis": [0, 0, 1],
        "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    }

    data = H5Group(data)
    return Cone(data)


def sphere():
    data = {
        "type": "Sphere",
        "coefficients": [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1, 0.0, 0.5, 1],
        "location": [0, 0, 0],
        "radius": 1.0,
        "trim_domain": [[0, 1], [0, 1]],
        "x_axis": [1, 0, 0],
        "y_axis": [0, 1, 0],
        "z_axis": [0, 0, 1],
        "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    }

    data = H5Group(data)
    return Sphere(data)


def torus():
    data = {
        "type": "Torus",
        "location": [0, 0, 0],
        "max_radius": 1.0,
        "min_radius": 0.5,
        "trim_domain": [[0, 1], [0, 1]],
        "x_axis": [1, 0, 0],
        "y_axis": [0, 1, 0],
        "z_axis": [0, 0, 1],
        "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    }

    data = H5Group(data)
    return Torus(data)


def bspline_surface():
    data = {
        "continuity": 6,
        "face_domain": [0.0, 0.785398163397494, 1.5707963267949, 3.14159265358979],
        "is_trimmed": True,
        "poles":
            [[[-0.498364597137595, 10.0, 5.67148872467595],
              [-0.498364597137595, 10.0, 7.00482205800928],
              [-0.498364597137595, 8.66666666666666, 7.00482205800928]],
             [[-0.22222222222218102, 10.0, 5.67148872467595],
              [-0.22222222222218102, 10.0, 7.00482205800928],
              [-0.22222222222218102, 8.66666666666666, 7.00482205800928]],
             [[-0.026960076346542003, 9.80473785412434, 5.67148872467595],
              [-0.026960076346542003, 9.80473785412434, 6.80955991213362],
              [-0.026960076346542003, 8.66666666666666, 6.80955991213362]]],
        "trim_domain": [0.0, 0.785398163397494, 1.5707963267949, 3.141592653589791],
        "type": "BSpline",
        "u_closed": False,
        "u_degree": 2,
        "u_knots": [0.0, 0.0, 0.0, 0.785398163397494, 0.785398163397494, 0.785398163397494],
        "u_rational": True,
        "v_closed": False,
        "v_degree": 2,
        "v_knots": [1.5707963267949, 1.5707963267949, 1.5707963267949, 3.14159265358979,
                    3.14159265358979, 3.14159265358979],
        "v_rational": True,
        "weights":
            [[1.0, 0.707106781186548, 1.0],
             [0.923879532511278, 0.653281482438182, 0.923879532511278],
             [1.0, 0.707106781186548, 1.0]],
        "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
        "u_periodic": False,
        "v_periodic": False
    }

    data = H5Group(data)
    return BSplineSurface(data)

