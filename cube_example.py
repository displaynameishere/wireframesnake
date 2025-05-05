from wireframesnake import Scene, Cube

scene = Scene(background=(0,0,0), face_culling=True, render_mode='solid')
scene.add(Cube(center=(0,0,0), size=1))
scene.render_to("cube.png", rotation=(0, 0, 0))