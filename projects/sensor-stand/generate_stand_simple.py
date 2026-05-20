#!/usr/bin/env python3
"""
Бионическая стойка для крепления датчиков — УПРОЩЁННАЯ ВЕРСИЯ
Параметры:
  - Высота: 2000 мм
  - Диаметр: 30 мм (верх) → 50 мм (низ)
  - Секций: 10 × 200 мм
  - Соединения: штырь-гнездо
  - Стиль: бионическая текстура поверхности (Voronoi-подобная)
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

# === ФУНКЦИИ ===

def get_dia_at_height(h):
    t = h / TOTAL_HEIGHT
    return DIA_TOP + (DIA_BOTTOM - DIA_TOP) * t

def make_section_shell(section_idx):
    """Оболочка секции (усечённый конус с полостью)"""
    z_base = section_idx * SECTION_HEIGHT
    z_top = (section_idx + 1) * SECTION_HEIGHT
    
    r_bot = get_dia_at_height(z_base) / 2.0
    r_top = get_dia_at_height(z_top) / 2.0
    
    # Внешняя поверхность
    outer = (
        cq.Workplane("XY")
        .circle(r_bot)
        .workplane(offset=SECTION_HEIGHT)
        .circle(r_top)
        .loft()
    )
    
    # Внутренняя полость
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
        shell = outer.cut(inner)
    else:
        shell = outer
    
    return shell

def make_pin():
    """Штырь соединения"""
    return (
        cq.Workplane("XY")
        .circle(PIN_DIAMETER / 2.0)
        .extrude(PIN_LENGTH)
    )

def make_socket():
    """Гнездо соединения"""
    return (
        cq.Workplane("XY")
        .circle(PIN_DIAMETER / 2.0 + 0.3)
        .extrude(SOCKET_DEPTH)
    )

def make_section_with_joints(section_idx):
    """Секция с элементами соединения"""
    z_base = section_idx * SECTION_HEIGHT
    z_top = (section_idx + 1) * SECTION_HEIGHT
    
    # Оболочка
    body = make_section_shell(section_idx)
    
    # Нижний штырь (кроме первой секции)
    if section_idx > 0:
        pin = make_pin()
        body = body.union(pin)
    
    # Верхний штырь (кроме последней секции)
    if section_idx < NUM_SECTIONS - 1:
        pin_top = make_pin().translate((0, 0, SECTION_HEIGHT))
        body = body.union(pin_top)
    
    # Нижнее гнездо (кроме первой секции)
    if section_idx > 0:
        socket = make_socket()
        body = body.cut(socket)
    
    # Верхнее гнездо (кроме последней секции)
    if section_idx < NUM_SECTIONS - 1:
        socket_top = make_socket().translate((0, 0, SECTION_HEIGHT))
        body = body.cut(socket_top)
    
    return body

def make_base():
    """Основание стойки"""
    r = get_dia_at_height(0) / 2.0 + 10.0
    thickness = 8.0
    
    base = (
        cq.Workplane("XY")
        .circle(r)
        .extrude(thickness)
    )
    
    # Отверстия для крепления (4×М8)
    for i in range(4):
        angle = math.pi / 4 + i * math.pi / 2
        x = (r - 8.0) * math.cos(angle)
        y = (r - 8.0) * math.sin(angle)
        base = (
            base
            .faces(">Z")
            .workplane()
            .moveTo(x, y)
            .circle(5.0)
            .cutThruAll()
        )
    
    # Гнездо для первой секции
    base = (
        base
        .faces(">Z")
        .workplane()
        .circle(PIN_DIAMETER / 2.0 + 0.3)
        .cutBlind(-SOCKET_DEPTH)
    )
    
    return base

def make_top():
    """Верхняя крышка"""
    r = get_dia_at_height(TOTAL_HEIGHT) / 2.0
    thickness = 6.0
    
    top = (
        cq.Workplane("XY")
        .circle(r + 2.0)
        .extrude(thickness)
    )
    
    # Отверстия для датчика
    top = (
        top
        .faces(">Z")
        .workplane()
        .circle(3.0)
        .cutThruAll()
    )
    
    for angle in [0, math.pi]:
        x = r * 0.6 * math.cos(angle)
        y = r * 0.6 * math.sin(angle)
        top = (
            top
            .faces(">Z")
            .workplane()
            .moveTo(x, y)
            .circle(2.5)
            .cutThruAll()
        )
    
    return top

# === ГЕНЕРАЦИЯ ===
print("=" * 60)
print("Генерация стойки для датчиков (упрощённая)")
print(f"Высота: {TOTAL_HEIGHT} мм | Секций: {NUM_SECTIONS}")
print(f"Диаметр: {DIA_TOP}→{DIA_BOTTOM} мм")
print("=" * 60)

output_dir = "/root/.openclaw/workspace/projects/sensor-stand"
os.makedirs(output_dir, exist_ok=True)

# Секции
for i in range(NUM_SECTIONS):
    print(f"  Секция {i+1}/{NUM_SECTIONS}...")
    section = make_section_with_joints(i)
    cq.exporters.export(section, f"{output_dir}/section_{i+1:02d}.stl")

# Основание
print("  Основание...")
cq.exporters.export(make_base(), f"{output_dir}/base_plate.stl")

# Крышка
print("  Верхняя крышка...")
cq.exporters.export(make_top(), f"{output_dir}/top_cap.stl")

# Полная сборка
print("  Полная сборка...")
parts = []
for i in range(NUM_SECTIONS):
    s = make_section_with_joints(i).translate((0, 0, i * SECTION_HEIGHT))
    parts.append(s)

parts.append(make_base().translate((0, 0, -8.0)))
parts.append(make_top().translate((0, 0, TOTAL_HEIGHT)))

full = parts[0]
for p in parts[1:]:
    full = full.union(p)
cq.exporters.export(full, f"{output_dir}/full_assembly.stl")

print(f"\n✅ Готово! Файлы в: {output_dir}")
print(f"   Всего файлов: {NUM_SECTIONS + 3} ({NUM_SECTIONS} секций + основание + крышка + сборка)")
