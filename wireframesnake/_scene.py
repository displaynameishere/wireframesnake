from PIL import Image, ImageDraw
import numpy as np
import math

class Scene:
    def __init__(self, width=800, height=600, fov=500, camera_distance=5, background=(30, 30, 30)):
        self.shapes = []
        self.width = width
        self.height = height
        self.fov = fov
        self.cam_dist = camera_distance
        self.background = background

    def add(self, shape):
        self.shapes.append(shape)

    def rotate(self, vertices, angles):
        ax, ay, az = np.radians(angles)
        rx = np.array([
            [1, 0, 0],
            [0, math.cos(ax), -math.sin(ax)],
            [0, math.sin(ax),  math.cos(ax)]
        ])
        ry = np.array([
            [math.cos(ay), 0, math.sin(ay)],
            [0, 1, 0],
            [-math.sin(ay), 0, math.cos(ay)]
        ])
        rz = np.array([
            [math.cos(az), -math.sin(az), 0],
            [math.sin(az),  math.cos(az), 0],
            [0, 0, 1]
        ])
        return vertices @ rx @ ry @ rz

    def project(self, v):
        x, y, z = v
        z += self.cam_dist
        if z == 0: z += 0.001
        factor = self.fov / z
        x_proj = int(x * factor + self.width / 2)
        y_proj = int(-y * factor + self.height / 2)
        return (x_proj, y_proj)

    def render_to(self, filepath, rotation=(0,0,0)):
        
        img = Image.new("RGB", (self.width, self.height), self.background)
        draw = ImageDraw.Draw(img)

        for shape in self.shapes:
            verts = self.rotate(shape.vertices - np.array(shape.vertices).mean(axis=0), rotation)
            verts = [self.project(v) for v in verts]
            for face in shape.faces:
                pts = [verts[i] for i in face]
                draw.polygon(pts, outline="white")

        img.save(filepath)
