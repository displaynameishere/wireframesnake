import numpy as np

class Shape3D:
    def __init__(self, vertices, faces, center=(0, 0, 0)):
        self.vertices = np.array(vertices) + np.array(center)
        self.faces = faces  # list of index triplets

class Cube(Shape3D):
    def __init__(self, center=(0,0,0), size=1):
        s = size / 2
        vertices = [
            [-s, -s, -s], [ s, -s, -s], [ s,  s, -s], [-s,  s, -s],
            [-s, -s,  s], [ s, -s,  s], [ s,  s,  s], [-s,  s,  s],
        ]
        faces = [
            [0,1,2], [0,2,3],  [4,5,6], [4,6,7],
            [0,1,5], [0,5,4],  [2,3,7], [2,7,6],
            [1,2,6], [1,6,5],  [0,3,7], [0,7,4]
        ]
        super().__init__(vertices, faces, center)

class Tetrahedron(Shape3D):
    def __init__(self, center=(0,0,0), size=1):
        s = size
        vertices = [
            [0, 0,  s],
            [0, 2*s/3, -s/3],
            [-s*np.sqrt(3)/2, -s/3, -s/3],
            [ s*np.sqrt(3)/2, -s/3, -s/3],
        ]
        faces = [
            [0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 2, 3]
        ]
        super().__init__(vertices, faces, center)
