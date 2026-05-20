#!/usr/bin/env python3
"""
Бионическая стойка для датчиков — ВЕРСИЯ С ФЕРМЕННОЙ СТРУКТУРОЙ
TPMS-оболочка + внутренняя ферма (стрингеры + диагонали + кольца)
"""

import cadquery as cq
import math
import os

# === ПАРАМЕТРЫ ===
TOTAL_HEIGHT = 2000.0
NUM_SECTIONS = 10
SECTION_HEIGHT = 200.0
DIA_TOP = 30.0
DIA_BOTTOM = 50.0
WALL_THICKNESS = 3.0
PIN_LENGTH = 15.0
PIN_DIAMETER = 8.0
SOCKET_DEPTH = 12.0

# Ферменная структура
STRUT_THICKNESS = 2.5      # Толщина стрингеров (вертикальных)
DIAGONAL_THICKNESS = 2.0   # Толщина диагоналей
RING_THICKNESS = 2.0       # Толщина горизонтальных колец
NUM_STRUTS = 6             # Количество стрингеров (вертикальных рёбер)
NUM_RINGS = 4              # Количество горизонтальных колец на секцию

def get_dia_at_height(h):
    t = h / TOTAL_HEIGHT
    return DIA_TOP + (DIA_BOTTOM - DIA_TOP) * t

def make_section_shell(section_idx):
    """Оболочка секции (усечённый конус с полостью)"""
    z_base = section_idx * SECTION_HEIGHT
    z_top = (section_idx + 1) * SECTION_HEIGHT
    
    r_bot = get_dia_at_height(z_base) / 2.0
    r_top = get_dia_at_height(z_top) / 2.0
    
    outer = (
        cq.Workplane("XY")
        .circle(r_bot)
        .workplane(offset=SECTION_HEIGHT)
        .circle(r_top)
        .loft()
    )
    
    r_inner_bot = r_bot - WALL_THICKNESS
    r_inner_top = r_top - WALL_THICKNESS
    
    if r_inner_bot > 3.0 and r_inner_top > 3.0:
        inner = (
            cq.Workplane("XY")
            .circle(r_inner_bot)
            .workplane(offset=SECTION_HEIGHT)
            .circle(r_inner_top)
            .loft()
        )
        return outer.cut(inner)
    return outer

def make_internal_lattice(section_idx):
    """Внутренняя ферменная структура: стрингеры + диагонали + кольца"""
    z_base = section_idx * SECTION_HEIGHT
    z_top = (section_idx + 1) * SECTION_HEIGHT
    
    r_bot = get_dia_at_height(z_base) / 2.0
    r_top = get_dia_at_height(z_top) / 2.0
    r_inner_bot = r_bot - WALL_THICKNESS - 1.0
    r_inner_top = r_top - WALL_THICKNESS - 1.0
    
    if r_inner_bot < 5.0 or r_inner_top < 5.0:
        return None
    
    all_beams = []
    
    # 1. Стрингеры (вертикальные рёбра)
    for i in range(NUM_STRUTS):
        angle = 2.0 * math.pi * i / NUM_STRUTS
        x_bot = r_inner_bot * math.cos(angle)
        y_bot = r_inner_bot * math.sin(angle)
        x_top = r_inner_top * math.cos(angle)
        y_top = r_inner_top * math.sin(angle)
        
        # Создаём балку как loft между двумя кругами
        beam = (
            cq.Workplane("XY")
            .moveTo(x_bot, y_bot)
            .circle(STRUT_THICKNESS / 2.0)
            .workplane(offset=SECTION_HEIGHT)
            .moveTo(x_top, y_top)
            .circle(STRUT_THICKNESS / 2.0)
            .loft()
        )
        all_beams.append(beam)
    
    # 2. Диагональные распорки (X-образные)
    for i in range(NUM_STRUTS):
        angle1 = 2.0 * math.pi * i / NUM_STRUTS
        angle2 = 2.0 * math.pi * ((i + NUM_STRUTS // 2) % NUM_STRUTS) / NUM_STRUTS
        
        # Нижняя точка
        x1 = r_inner_bot * 0.85 * math.cos(angle1)
        y1 = r_inner_bot * 0.85 * math.sin(angle1)
        # Верхняя точка (смещена на пол-шага)
        x2 = r_inner_top * 0.85 * math.cos(angle2)
        y2 = r_inner_top * 0.85 * math.sin(angle2)
        
        diag = (
            cq.Workplane("XY")
            .moveTo(x1, y1)
            .circle(DIAGONAL_THICKNESS / 2.0)
            .workplane(offset=SECTION_HEIGHT)
            .moveTo(x2, y2)
            .circle(DIAGONAL_THICKNESS / 2.0)
            .loft()
        )
        all_beams.append(diag)
    
    # 3. Горизонтальные кольца (ребра жёсткости)
    for ring_idx in range(1, NUM_RINGS + 1):
        z_frac = ring_idx / (NUM_RINGS + 1)
        z_ring = SECTION_HEIGHT * z_frac
        r_ring_bot = r_inner_bot + (r_inner_top - r_inner_bot) * z_frac
        r_ring = r_ring_bot - RING_THICKNESS / 2.0
        
        if r_ring > 3.0:
            ring = (
                cq.Workplane("XY")
                .workplane(offset=z_ring)
                .circle(r_ring)
                .circle(r_ring - RING_THICKNESS)
                .extrude(2.0)
            )
            all_beams.append(ring)
    
    # Объединяем все балки
    if all_beams:
        result = all_beams[0]
        for b in all_beams[1:]:
            result = result.union(b)
        return result
    return None

def make_section_with_lattice(section_idx):
    """Полная секция: оболочка + ферма + соединения"""
    # Оболочка
    body = make_section_shell(section_idx)
    
    # Внутренняя ферма
    lattice = make_internal_lattice(section_idx)
    if lattice:
        body = body.union(lattice)
    
    # Нижний штырь (кроме первой секции)
    if section_idx > 0:
        pin = (
            cq.Workplane("XY")
            .circle(PIN_DIAMETER / 2.0)
            .extrude(PIN_LENGTH)
        )
        body = body.union(pin)
    
    # Верхний штырь (кроме последней)
    if section_idx < NUM_SECTIONS - 1:
        pin_top = (
            cq.Workplane("XY")
            .circle(PIN_DIAMETER / 2.0)
            .extrude(PIN_LENGTH)
            .translate((0, 0, SECTION_HEIGHT))
        )
        body = body.union(pin_top)
    
    # Нижнее гнездо (кроме первой)
    if section_idx > 0:
        socket = (
            cq.Workplane("XY")
            .circle(PIN_DIAMETER / 2.0 + 0.3)
            .extrude(SOCKET_DEPTH)
        )
        body = body.cut(socket)
    
    # Верхнее гнездо (кроме последней)
    if section_idx < NUM_SECTIONS - 1:
        socket_top = (
            cq.Workplane("XY")
            .circle(PIN_DIAMETER / 2.0 + 0.3)
            .extrude(SOCKET_DEPTH)
            .translate((0, 0, SECTION_HEIGHT))
        )
        body = body.cut(socket_top)
    
    return body

def make_base():
    """Основание"""
    r = get_dia_at_height(0) / 2.0 + 10.0
    thickness = 8.0
    
    base = cq.Workplane("XY").circle(r).extrude(thickness)
    
    for i in range(4):
        angle = math.pi / 4 + i * math.pi / 2
        x = (r - 8.0) * math.cos(angle)
        y = (r - 8.0) * math.sin(angle)
        base = base.faces(">Z").workplane().moveTo(x, y).circle(5.0).cutThruAll()
    
    base = base.faces(">Z").workplane().circle(PIN_DIAMETER / 2.0 + 0.3).cutBlind(-SOCKET_DEPTH)
    return base

def make_top():
    """Верхняя крышка"""
    r = get_dia_at_height(TOTAL_HEIGHT) / 2.0
    thickness = 6.0
    
    top = cq.Workplane("XY").circle(r + 2.0).extrude(thickness)
    top = top.faces(">Z").workplane().circle(3.0).cutThruAll()
    
    for angle in [0, math.pi]:
        x = r * 0.6 * math.cos(angle)
        y = r * 0.6 * math.sin(angle)
        top = top.faces(">Z").workplane().moveTo(x, y).circle(2.5).cutThruAll()
    
    return top

# === ГЕНЕРАЦИЯ ===
print("=" * 60)
print("Генерация стойки с ферменной структурой")
print(f"Высота: {TOTAL_HEIGHT} мм | Секций: {NUM_SECTIONS}")
print(f"Стрингеров: {NUM_STRUTS} | Колец/секцию: {NUM_RINGS}")
print("=" * 60)

output_dir = "/root/.openclaw/workspace/projects/sensor-stand-lattice"
os.makedirs(output_dir, exist_ok=True)

# Сначала тестируем одну секцию
print("\nТест: секция 5...")
test = make_section_with_lattice(4)
if test:
    cq.exporters.export(test, f"{output_dir}/test_section_05.stl")
    print(f"  → test_section_05.stl: {os.path.getsize(f'{output_dir}/test_section_05.stl')/1024:.0f} KB")
    print("  ✅ Тест пройден, генерирую все секции...")
else:
    print("  ❌ Ошибка генерации")

# Генерируем все секции
for i in range(NUM_SECTIONS):
    print(f"  Секция {i+1}/{NUM_SECTIONS}...")
    section = make_section_with_lattice(i)
    if section:
        cq.exporters.export(section, f"{output_dir}/section_{i+1:02d}.stl")

# Основание и крышка
print("  Основание...")
cq.exporters.export(make_base(), f"{output_dir}/base_plate.stl")

print("  Верхняя крышка...")
cq.exporters.export(make_top(), f"{output_dir}/top_cap.stl")

# Удаляем тестовый файл
test_file = f"{output_dir}/test_section_05.stl"
if os.path.exists(test_file):
    os.remove(test_file)

print(f"\n✅ Готово! Файлы в: {output_dir}")
print(f"   Всего: {NUM_SECTIONS + 2} файлов")
total = sum(os.path.getsize(f"{output_dir}/{f}") for f in os.listdir(output_dir) if f.endswith('.stl'))
print(f"   Общий размер: {total/1024/1024:.1f} MB")
