// Dog assembled preview
color("lightblue") import("/root/.openclaw/workspace/3d-models/dog-assembly/01_body.stl");
translate([70, 0, 14]) color("lightgreen") import("/root/.openclaw/workspace/3d-models/dog-assembly/02_head.stl");
translate([-30, 16, 8.4]) color("orange") import("/root/.openclaw/workspace/3d-models/dog-assembly/03_leg.stl");
translate([-30, -16, 8.4]) color("orange") import("/root/.openclaw/workspace/3d-models/dog-assembly/03_leg.stl");
translate([30, 16, 14]) color("orange") import("/root/.openclaw/workspace/3d-models/dog-assembly/03_leg.stl");
translate([30, -16, 14]) color("orange") import("/root/.openclaw/workspace/3d-models/dog-assembly/03_leg.stl");
translate([-68, 0, 12.6]) color("red") import("/root/.openclaw/workspace/3d-models/dog-assembly/04_tail.stl");
translate([-10, 0, 26]) color("yellow") import("/root/.openclaw/workspace/3d-models/dog-assembly/05_ear.stl");
translate([10, 0, 26]) color("yellow") import("/root/.openclaw/workspace/3d-models/dog-assembly/05_ear.stl");
