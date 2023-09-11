from manim import *
import numpy as np

class hypercube2(ThreeDScene):
    def construct(self):
        coords = np.array([[i, j, k, l] for i in [-1, 1] for j in [-1, 1] for k in [-1, 1] for l in [-1, 1]])

        def rotate_4d(coords, theta, axis1, axis2):
            R = np.identity(4)
            R[axis1, axis1], R[axis1, axis2], R[axis2, axis1], R[axis2, axis2] = np.cos(theta), -np.sin(theta), np.sin(theta), np.cos(theta)
            return coords @ R.T  # Matrix multiplication in 4D space

        projection_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0]
        ])

        for angle in np.linspace(0, 2 * np.pi, 100):
            rotated_coords = rotate_4d(coords, angle, 0, 1)
            rotated_coords = rotate_4d(rotated_coords, angle, 2, 3)
            rotated_coords = rotate_4d(rotated_coords, angle / 2, 1, 2)

            coords_3d = rotated_coords @ projection_matrix.T  # 4D to 3D projection

            dots = [Dot3D(point=coord, radius=0.08).set_opacity(0.7) for coord in coords_3d]

            edges = []
            for i, coord1 in enumerate(coords):  # Using original 4D coordinates to determine adjacency
                for j, coord2 in enumerate(coords):
                    if np.sum(np.abs(coord1 - coord2)) == 2:
                        edge = Line3D(dots[i].get_center(), dots[j].get_center(), stroke_width=2)
                        edges.append(edge)
            
            self.clear()
            self.add(*dots, *edges)
            self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
            self.wait(0.1)
