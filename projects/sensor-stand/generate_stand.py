#!/usr/bin/env python3
"""
Бионическая стойка для крепления датчиков
Параметры:
  - Высота: 2000 мм
  - Диаметр: 30 мм (верх) → 50 мм (низ)
  - Секций: 10 × 200 мм
  - Стиль: бионическая ферма с TPMS-оболочкой
"""

import cadquery as cq
import math
import os

# === ПАРАМЕТРЫ ===
TOTAL_HEIGHT = 2000.0    # мм
NUM_SECTIONS = 10
SECTION_HEIGHT = 200.0   # мм
DIA_TOP = 30.0           # мм (верх)
DIA_BOTTOM = 50.0        # мм (низ)
WALL_THICKNESS = 3.0     # мм (толщина стенки)
LATTICE_THICKNESS = 2.0  # мм (толщина элементов фермы)
PIN_LENGTH = 15.0        # мм (длина штыря соединения)
PIN_DIAMETER = 8.0       # мм (диаметр штыря)
SOCKET_DEPTH = 12.0      # мм (глубина гнезда)

# TPMS параметры
TPMS_CELL_SIZE = 12.0    # мм (размер ячейки TPMS)
TPMS_WALL = 1.5          # мм (толщина стенки TPMS)

# === ФУНКЦИИ ===

def get_dia_at_height(h):
    """Линейная интерполяция диаметра по высоте"""
    t = h / TOTAL_HEIGHT
    return DIA_TOP + (DIA_BOTTOM - DIA_TOP) * t

def get_radius_at_height(h):
    return get_dia_at_height(h) / 2.0

def make_tpms_gyroid(x, y, z, C=0.0):
    """Уравнение Gyroid TPMS: sin(x)*cos(y) + sin(y)*cos(z) + sin(z)*cos(x) = C"""
    scale = 2.0 * math.pi / TPMS_CELL_SIZE
    return (math.sin(x * scale) * math.cos(y * scale) +
            math.sin(y * scale) * math.cos(z * scale) +
            math.sin(z * scale) * math.cos(x * scale) - C)

def generate_lattice_points(center_x, center_y, outer_r, inner_r, z_base, z_top, num_angular=8):
    """Генерация точек для ферменных элементов"""
    points = []
    for i in range(num_angular):
        angle = 2.0 * math.pi * i / num_angular
        # Внешняя точка
        ox = center_x + outer_r * math.cos(angle)
        oy = center_y + outer_r * math.sin(angle)
        # Внутренняя точка (смещена на пол-шага)
        iangle = angle + math.pi / num_angular
        ix = center_x + inner_r * math.cos(iangle)
        iy = center_y + inner_r * math.sin(iangle)
        points.append({
            'outer': (ox, oy),
            'inner': (ix, iy),
            'angle': angle
        })
    return points

def make_section_body(section_idx):
    """Создание тела одной секции (внешняя оболочка + внутренняя ферма)"""
    z_base = section_idx * SECTION_HEIGHT
    z_top = (section_idx + 1) * SECTION_HEIGHT
    
    r_bottom = get_radius_at_height(z_base)
    r_top = get_radius_at_height(z_top)
    r_mid = (r_bottom + r_top) / 2.0
    
    # Внешняя оболочка (усечённый конус)
    outer = (
        cq.Workplane("XY")
        .circle(r_bottom)
        .workplane(offset=SECTION_HEIGHT)
        .circle(r_top)
        .loft()
    )
    
    # Внутренняя полость
    r_inner_bottom = r_bottom - WALL_THICKNESS
    r_inner_top = r_top - WALL_THICKNESS
    
    if r_inner_bottom > 2.0 and r_inner_top > 2.0:
        inner = (
            cq.Workplane("XY")
            .circle(r_inner_bottom)
            .workplane(offset=SECTION_HEIGHT)
            .circle(r_inner_top)
            .loft()
        )
        shell = outer.cut(inner)
    else:
        shell = outer
    
    return shell

def make_lattice_in_section(section_idx):
    """Создание ферменной структуры внутри секции"""
    z_base = section_idx * SECTION_HEIGHT
    z_top = (section_idx + 1) * SECTION_HEIGHT
    
    r_bottom = get_radius_at_height(z_base)
    r_top = get_radius_at_height(z_top)
    r_mid = (r_bottom + r_top) / 2.0
    
    r_outer = r_mid - WALL_THICKNESS - 1.0
    r_inner = r_outer * 0.6
    
    if r_outer < 5.0 or r_inner < 2.0:
        return None
    
    beams = []
    num_angular = max(4, int(r_mid / 5))
    
    # Вертикальные рёбра (стрингеры)
    for i in range(num_angular):
        angle = 2.0 * math.pi * i / num_angular
        x_bot = r_outer * math.cos(angle)
        y_bot = r_outer * math.sin(angle)
        
        # Линейная интерполяция радиуса
        t = 0.5  # середина секции
        r_at_mid = r_outer + (r_outer * (r_top - r_bottom) / r_bottom) * t * 0.1
        x_top = r_at_mid * math.cos(angle)
        y_top = r_at_mid * math.sin(angle)
        
        # Создаём балку как цилиндр
        beam = (
            cq.Workplane("XY")
            .moveTo(x_bot, y_bot)
            .circle(LATTICE_THICKNESS / 2.0)
            .workplane(offset=SECTION_HEIGHT)
            .moveTo(x_top, y_top)
            .circle(LATTICE_THICKNESS / 2.0)
            .loft()
        )
        beams.append(beam)
    
    # Диагональные распорки (Voronoi-подобные)
    num_diagonal = num_angular
    for i in range(num_diagonal):
        angle1 = 2.0 * math.pi * i / num_diagonal
        angle2 = 2.0 * math.pi * ((i + num_diagonal // 2) % num_diagonal) / num_diagonal
        
        # Нижняя точка
        x1 = r_outer * 0.8 * math.cos(angle1)
        y1 = r_outer * 0.8 * math.sin(angle1)
        # Верхняя точка (смещена)
        x2 = r_outer * 0.8 * math.cos(angle2)
        y2 = r_outer * 0.8 * math.sin(angle2)
        
        # Диагональ от низа к верху
        beam = (
            cq.Workplane("XY")
            .moveTo(x1, y1)
            .circle(LATTICE_THICKNESS * 0.7 / 2.0)
            .workplane(offset=SECTION_HEIGHT)
            .moveTo(x2, y2)
            .circle(LATTICE_THICKNESS * 0.7 / 2.0)
            .loft()
        )
        beams.append(beam)
    
    # Горизонтальные кольца (ребра жёсткости)
    for z_frac in [0.25, 0.5, 0.75]:
        z_ring = z_base + SECTION_HEIGHT * z_frac
        r_ring = get_radius_at_height(z_ring) - WALL_THICKNESS - 1.0
        if r_ring > 3.0:
            ring = (
                cq.Workplane("XY")
                .workplane(offset=SECTION_HEIGHT * z_frac)
                .circle(r_ring)
                .circle(r_ring - LATTICE_THICKNESS * 0.5)
                .extrude(1.0)
            )
            beams.append(ring)
    
    if beams:
        result = beams[0]
        for b in beams[1:]:
            result = result.union(b)
        return result
    return None

def make_connection_pin(section_idx, is_top=False):
    """Создание штыря для соединения секций"""
    if is_top and section_idx == NUM_SECTIONS - 1:
        return None  # Верхняя секция — без верхнего штыря
    
    z_base = section_idx * SECTION_HEIGHT
    r = get_radius_at_height(z_base)
    pin_r = min(PIN_DIAMETER / 2.0, r * 0.3)
    
    if pin_r < 1.5:
        return None
    
    pin = (
        cq.Workplane("XY")
        .circle(pin_r)
        .extrude(PIN_LENGTH)
    )
    return pin

def make_connection_socket(section_idx, is_top=False):
    """Создание гнезда для соединения секций"""
    if is_top and section_idx == NUM_SECTIONS - 1:
        return None
    
    z_base = section_idx * SECTION_HEIGHT
    r = get_radius_at_height(z_base)
    socket_r = min(PIN_DIAMETER / 2.0 + 0.5, r * 0.35)
    
    if socket_r < 2.0:
        return None
    
    socket = (
        cq.Workplane("XY")
        .circle(socket_r)
        .extrude(SOCKET_DEPTH)
    )
    return socket

def make_section_complete(section_idx):
    """Полная секция: оболочка + ферма + соединения"""
    print(f"  Секция {section_idx + 1}/{NUM_SECTIONS}...")
    
    # 1. Оболочка
    body = make_section_body(section_idx)
    
    # 2. Ферменная структура
    lattice = make_lattice_in_section(section_idx)
    if lattice:
        body = body.union(lattice)
    
    # 3. Нижний штырь (кроме первой секции — у неё основание)
    if section_idx > 0:
        pin = make_connection_pin(section_idx, is_top=False)
        if pin:
            body = body.union(pin)
    
    # 4. Верхний штырь
    if section_idx < NUM_SECTIONS - 1:
        pin_top = make_connection_pin(section_idx, is_top=True)
        if pin_top:
            # Смещаем штырь вверх
            pin_top = pin_top.translate((0, 0, SECTION_HEIGHT))
            body = body.union(pin_top)
    
    # 5. Гнёзда для соединения (вырезаем из тела)
    if section_idx > 0:
        socket = make_connection_socket(section_idx, is_top=False)
        if socket:
            body = body.cut(socket)
    
    if section_idx < NUM_SECTIONS - 1:
        socket_top = make_connection_socket(section_idx, is_top=True)
        if socket_top:
            socket_top = socket_top.translate((0, 0, SECTION_HEIGHT))
            body = body.cut(socket_top)
    
    return body

def make_base_plate():
    """Основание стойки (нижняя плита)"""
    r = get_radius_at_height(0) + 10.0
    thickness = 8.0
    
    base = (
        cq.Workplane("XY")
        .circle(r)
        .extrude(thickness)
    )
    
    # Отверстия для крепления к земле (4 шт)
    bolt_r = 4.0  # М8 болт
    hole_r = bolt_r + 1.0
    for i in range(4):
        angle = math.pi / 4 + i * math.pi / 2
        x = (r - 8.0) * math.cos(angle)
        y = (r - 8.0) * math.sin(angle)
        base = (
            base
            .faces(">Z")
            .workplane()
            .moveTo(x, y)
            .circle(hole_r)
            .cutThruAll()
        )
    
    # Центральное гнездо для первой секции
    socket_r = PIN_DIAMETER / 2.0 + 0.5
    base = (
        base
        .faces(">Z")
        .workplane()
        .circle(socket_r)
        .cutBlind(-SOCKET_DEPTH)
    )
    
    return base

def make_top_cap():
    """Верхняя крышка стойки (крепление датчика)"""
    r = get_radius_at_height(TOTAL_HEIGHT)
    thickness = 6.0
    
    cap = (
        cq.Workplane("XY")
        .circle(r + 2.0)
        .extrude(thickness)
    )
    
    # Отверстие для крепления датчика (М5)
    cap = (
        cap
        .faces(">Z")
        .workplane()
        .circle(3.0)  # М5 + запас
        .cutThruAll()
    )
    
    # Два дополнительных отверстия для фиксации
    for angle in [0, math.pi]:
        x = r * 0.6 * math.cos(angle)
        y = r * 0.6 * math.sin(angle)
        cap = (
            cap
            .faces(">Z")
            .workplane()
            .moveTo(x, y)
            .circle(2.5)
            .cutThruAll()
        )
    
    return cap

# === ГЕНЕРАЦИЯ ===
print("=" * 60)
print("Генерация бионической стойки для датчиков")
print(f"Высота: {TOTAL_HEIGHT} мм | Секций: {NUM_SECTIONS}")
print(f"Диаметр: {DIA_TOP}→{DIA_BOTTOM} мм")
print("=" * 60)

output_dir = "/root/.openclaw/workspace/projects/sensor-stand"
os.makedirs(output_dir, exist_ok=True)

# Генерируем каждую секцию отдельно
for i in range(NUM_SECTIONS):
    section = make_section_complete(i)
    if section:
        filename = f"{output_dir}/section_{i+1:02d}.stl"
        cq.exporters.export(section, filename)
        print(f"    → {filename}")

# Основание
print("  Основание...")
base = make_base_plate()
cq.exporters.export(base, f"{output_dir}/base_plate.stl")
print(f"    → {output_dir}/base_plate.stl")

# Верхняя крышка
print("  Верхняя крышка...")
top = make_top_cap()
cq.exporters.export(top, f"{output_dir}/top_cap.stl")
print(f"    → {output_dir}/top_cap.stl")

# Полная сборка (для визуализации)
print("\n  Сборка полной модели...")
all_parts = []
for i in range(NUM_SECTIONS):
    section = make_section_complete(i)
    if section:
        section = section.translate((0, 0, i * SECTION_HEIGHT))
        all_parts.append(section)

base_full = base.translate((0, 0, -8.0))
all_parts.append(base_full)

top_full = top.translate((0, 0, TOTAL_HEIGHT))
all_parts.append(top_full)

if all_parts:
    full_assembly = all_parts[0]
    for p in all_parts[1:]:
        full_assembly = full_assembly.union(p)
    cq.exporters.export(full_assembly, f"{output_dir}/full_assembly.stl")
    print(f"    → {output_dir}/full_assembly.stl")

print("\n✅ Готово! Все STL-файлы в:", output_dir)
print(f"   Секций: {NUM_SECTIONS} + основание + крышка = {NUM_SECTIONS + 2} файлов")
print(f"   Общий объём файлов:")
import subprocess
result = subprocess.run(['du', '-sh', output_dir], capture_output=True, text=True)
print(f"   {result.stdout.strip()}")
