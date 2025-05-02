from wireframesnake import Scene, Tetrahedron

scene = Scene(background=(0,0,0))
scene.add(Tetrahedron(center=(20,10,0), size=2))
scene.render_to("tetrahedron.png", rotation=(20, 45, 10))