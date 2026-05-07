"""
Разборная модель собаки для 3D-печати
Части: туловище, голова, 4 лапы, хвост, уши
Соединение: штифты в пазах с зазором
Масштаб: ~120 мм длина в собранном виде
"""
import cadquery as cq
import os

# === ПАРАМЕТРЫ ===
body_length = 120.0
body_width = 35.0
body_height = 28.0
wall_thick = 3.0
clearance = 0.3
pin_dia = 4.0
pin_len = 8.0
head_dia = 22.0
leg_dia = 8.0
leg_len = 25.0
tail_len = 20.0
ear_size = 12.0
joint_dia = 6.0

output_dir = "/root/.openclaw/workspace/3d-models/dog-assembly"
os.makedirs(output_dir, exist_ok=True)

# === ТУЛОВИЩЕ ===
# Базовая форма — скругленный параллелепипед
body = (
    cq.Workplane("XY")
    .box(body_length, body_width, body_height, centered=(True, True, False))
    .edges("|Z").fillet(10.0)
    .edges(">Z").fillet(5.0)
)

# Полость внутри
body_hollow = (
    cq.Workplane("XY")
    .box(body_length - 2*wall_thick, body_width - 2*wall_thick, body_height - wall_thick, centered=(True, True, False))
    .edges("|Z").fillet(8.0)
    .translate((0, 0, wall_thick))
)
body = body.cut(body_hollow)

# Пазы для лап (4 шт, горизонтальные)
for x_sign in [-1, 1]:
    for z_pos in [body_height * 0.3, body_height * 0.5]:
        leg_hole = (
            cq.Workplane("YZ")
            .circle(leg_dia/2 + clearance)
            .extrude(body_length/2 + 5)
            .translate((x_sign * body_length * 0.25, body_width/2 - 1, z_pos))
        )
        body = body.cut(leg_hole)

# Паз для головы (перед)
head_socket = (
    cq.Workplane("YZ")
    .circle(joint_dia/2 + clearance)
    .extrude(15)
    .translate((body_length/2 + 5, 0, body_height * 0.5))
)
body = body.cut(head_socket)

# Паз для хвоста (зад)
tail_socket = (
    cq.Workplane("YZ")
    .circle(joint_dia/2 + clearance)
    .extrude(12)
    .translate((-body_length/2 - 3, 0, body_height * 0.45))
)
body = body.cut(tail_socket)

# Пазы для ушей (верх)
for x_sign in [-1, 1]:
    ear_socket = (
        cq.Workplane("XY")
        .circle(joint_dia/2 + clearance)
        .extrude(10)
        .translate((x_sign * 10, 0, body_height - 2))
    )
    body = body.cut(ear_socket)

cq.exporters.export(body, f"{output_dir}/01_body.stl", tolerance=0.01, angularTolerance=0.1)
print("OK: Туловище")

# === ГОЛОВА ===
head = (
    cq.Workplane("XY")
    .sphere(head_dia)
    .translate((0, 0, head_dia * 0.8))
)

# Полость
head_hollow = (
    cq.Workplane("XY")
    .sphere(head_dia - wall_thick)
    .translate((0, 0, head_dia * 0.8))
)
head = head.cut(head_hollow)

# Штифт для соединения с туловищем
head_pin = (
    cq.Workplane("YZ")
    .circle(pin_dia/2)
    .extrude(pin_len)
    .translate((-pin_len/2 - 2, 0, head_dia * 0.8))
)
head = head.union(head_pin)

# Глаза
for x_sign in [-1, 1]:
    eye = (
        cq.Workplane("XZ")
        .circle(3.5)
        .extrude(10)
        .translate((x_sign * 7, head_dia * 0.65, head_dia * 1.0))
    )
    head = head.cut(eye)

# Нос
nose = (
    cq.Workplane("XZ")
    .circle(2.5)
    .extrude(8)
    .translate((0, head_dia * 0.78, head_dia * 0.65))
)
head = head.cut(nose)

# Рот
mouth = (
    cq.Workplane("XZ")
    .moveTo(-6, 0).lineTo(6, 0).close()
    .extrude(5)
    .translate((0, head_dia * 0.75, head_dia * 0.48))
)
head = head.cut(mouth)

cq.exporters.export(head, f"{output_dir}/02_head.stl", tolerance=0.01, angularTolerance=0.1)
print("OK: Голова")

# === ЛАПА ===
def make_leg():
    leg = (
        cq.Workplane("XY")
        .circle(leg_dia)
        .extrude(leg_len)
    )
    leg = leg.edges(">Z").fillet(2.0)
    # Штифт сверху
    pin = (
        cq.Workplane("XY")
        .circle(pin_dia/2)
        .extrude(pin_len)
        .translate((0, 0, leg_len))
    )
    leg = leg.union(pin)
    # Полость снизу
    leg_hole = (
        cq.Workplane("XY")
        .circle(leg_dia - wall_thick)
        .extrude(leg_len - wall_thick)
        .translate((0, 0, wall_thick))
    )
    leg = leg.cut(leg_hole)
    return leg

leg = make_leg()
cq.exporters.export(leg, f"{output_dir}/03_leg.stl", tolerance=0.01, angularTolerance=0.1)
print("OK: Лапа (x4)")

# === ХВОСТ ===
tail = (
    cq.Workplane("XY")
    .circle(joint_dia/2)
    .workplane(offset=tail_len)
    .circle(joint_dia/4)
    .loft()
)
tail_pin = (
    cq.Workplane("XY")
    .circle(pin_dia/2)
    .extrude(pin_len)
    .translate((0, 0, -pin_len))
)
tail = tail.union(tail_pin)
cq.exporters.export(tail, f"{output_dir}/04_tail.stl", tolerance=0.01, angularTolerance=0.1)
print("OK: Хвост")

# === УХО ===
def make_ear():
    ear = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .threePointArc((ear_size/2, ear_size*0.8), (0, ear_size))
        .close()
        .extrude(3.0)
    )
    ear_pin = (
        cq.Workplane("XY")
        .circle(pin_dia/2)
        .extrude(pin_len)
        .translate((0, 2, -pin_len))
    )
    ear = ear.union(ear_pin)
    return ear

ear = make_ear()
cq.exporters.export(ear, f"{output_dir}/05_ear.stl", tolerance=0.01, angularTolerance=0.1)
print("OK: Ухо (x2)")

# === ШТИФТЫ-ФИКСАТОРЫ ===
fix_pin = (
    cq.Workplane("XY")
    .circle(pin_dia/2)
    .extrude(pin_len)
)
cq.exporters.export(fix_pin, f"{output_dir}/06_fix_pin.stl", tolerance=0.01, angularTolerance=0.1)
print("OK: Штифты-фиксаторы")

# === СВОДКА ===
print(f"\n=== ГОТОВО ===")
print(f"Детали в: {output_dir}")
print(f"Состав: туловище(1), голова(1), лапы(4), хвост(1), уши(2), штифты(6)")
print(f"Всего деталей: 15")
