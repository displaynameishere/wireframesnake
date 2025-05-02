from wireframesnake import Scene, Cube, Tetrahedron

scene = Scene(background=(0,0,0))
scene.add(Cube(center=(0,0,0), size=1))
scene.render_to("cube.png", rotation=(20, 45, 10))