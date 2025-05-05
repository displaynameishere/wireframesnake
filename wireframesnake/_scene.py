from PIL import Image, ImageDraw
import numpy as np
import math


class Scene:
    def __init__(self, width=800, height=600, fov=500, camera_distance=5, background=(30, 30, 30), 
                 render_mode='wireframe', face_culling=False, face_color=(255, 0, 0)):
        self.shapes = []
        self.width = width
        self.height = height
        self.fov = fov
        self.cam_dist = camera_distance
        self.background = background
        self.render_mode = render_mode  # 'wireframe' or 'solid'
        self.face_culling = face_culling 
        self.face_color = face_color
    
    def add(self, shape):
        self.shapes.append(shape)

    def rotate(self, vertices, angles):
        ax, ay, az = np.radians(angles)
        rx = np.array([
            [1, 0, 0],
            [0, math.cos(ax), -math.sin(ax)],
            [0, math.sin(ax), math.cos(ax)]
        ])
        ry = np.array([
            [math.cos(ay), 0, math.sin(ay)],
            [0, 1, 0],
            [-math.sin(ay), 0, math.cos(ay)]
        ])
        rz = np.array([
            [math.cos(az), -math.sin(az), 0],
            [math.sin(az), math.cos(az), 0],
            [0, 0, 1]
        ])
        # matrix mult in zxy order
        return vertices @ rz @ ry @ rx

    def project(self, v):
        x, y, z = v
        z += self.cam_dist
        if z == 0: z += 0.001
        factor = self.fov / z
        x_proj = int(x * factor + self.width / 2)
        y_proj = int(-y * factor + self.height / 2)
        return (x_proj, y_proj)

    def is_face_visible(self, vertices, face_indices):
        v0 = np.array(vertices[face_indices[0]]).flatten()
        v1 = np.array(vertices[face_indices[1]]).flatten()
        v2 = np.array(vertices[face_indices[2]]).flatten()
    
        edge1 = v1 - v0
        edge2 = v2 - v0
        normal = np.cross(edge1, edge2)

        camera_direction = np.array([0, 0, -1])
        dot_product = np.dot(normal, camera_direction)
        
        return dot_product < 0

    def render_to(self, filepath, rotation=(0, 0, 0)):
        img = Image.new("RGB", (self.width, self.height), self.background)
        draw = ImageDraw.Draw(img)

        for shape in self.shapes:
            verts = shape.vertices - np.array(shape.vertices).mean(axis=0)
            verts = self.rotate(verts, rotation)
            
            projected = [self.project(v) for v in verts]

            for face in shape.faces:
                if self.face_culling and not self.is_face_visible(verts, face):
                    continue

                pts = [projected[i] for i in face]
                
                if self.render_mode == 'solid':
                    draw.polygon(pts, fill=self.face_color)
                else:
                    draw.polygon(pts, outline="white")

        img.save(filepath)
