"""
Computations for winding number and related operations for curves/surfaces.
"""

import numpy as np

def winding_number(curve_uv_values, surface_uv_values):
    """ Compute the winding number for a polyline and surface UV values efficiently. """
    a_values = curve_uv_values[:-1]
    b_values = curve_uv_values[1:]
    a = a_values[:, np.newaxis] - surface_uv_values
    b = b_values[:, np.newaxis] - surface_uv_values

    det = a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]

    dot = np.einsum('ijk,ijk->ij', a, b)
    winding_number_result = np.sum(np.arctan2(det, dot), axis=0) / (2 * np.pi)
    return winding_number_result.reshape(-1, 1)

def find_surface_uv_for_curve(surface_points, surface_uv_values, curve_points):
        """
        Calculate the nearest UV values on a surface for a given set of curve points.

        Args:
        surface_points (np.ndarray): Points on the surface.
        surface_uv_values (np.ndarray): UV values on the surface.
        curve_points (np.ndarray): Points on the curve.

        Returns:
        np.ndarray: UV values on the surface closest to the curve points.
        """
        # Calculate the nearest surface point for each curve point
        # nearest_3d_surface_points, curve_indexes = self._calculate_nearest_surface_points(surface_points, curve_points)
        from scipy.spatial import KDTree
        tree = KDTree(surface_points)
        _, curve_indexes = tree.query(curve_points)

        if type(curve_indexes) == np.int64:
            curve_indexes = [curve_indexes]

        if surface_uv_values.size > 0 and max(curve_indexes) < len(surface_uv_values):
            surface_uv_near_curve = surface_uv_values[curve_indexes]
        else:
            # Handle the case where surface_uv_values is empty or too small
            # This could be setting surface_uv_near_curve to an empty array
            # or some other default value, depending on your application's needs
            surface_uv_near_curve = np.array([])

        return surface_uv_near_curve
