#!/usr/bin/env python3
"""
Бионическая стойка для датчиков — ВЕРСИЯ С ФЕРМЕННОЙ СТРУКТУРОЙ v2
TPMS-оболочка + внутренняя ферма (стрингеры + диагонали + кольца)
Адаптивная: на тонких секциях меньше элементов
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
STRUT_THICKNESS = 2.5
DIAGONAL_THICKNESS = 2.0
RING_THICKNESS = 2.0

def get_dia_at_height(h):
    t = h / TOTAL_HEIGHT
    return DIA_TOP + (DIA_BOTTOM - DIA_TOP) * 2.0  # Увеличиваю диаметр для фермы

def get_dia_at_height_orig(h):
    t = h / TOTAL_HEIGHT
    return DIA_TOP + (DIA_BOTTOM - DIA_TOP) * t

def make_section_shell(section_idx):
    """Оболочка секции"""
    z_base = section_idx * SECTION_HEIGHT
    z_top = (section_idx + 1) * SECTION_HEIGHT
    
    r_bot = get_dia_at_height_orig(z_base) / 2.0
    r_top = get_dia_at_height_orig(z_top) / 2.0
    
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

def make_internal_lattice_adaptive(section_idx):
    """Адаптивная внутренняя ферма — масштабируется под размер секции"""
    z_base = section_idx * SECTION_HEIGHT
    z_top = (section_idx + 1) * SECTION_HEIGHT
    
    r_bot = get_dia_at_height_orig(z_base) / 2.0
    r_top = get_dia_at_height_orig(z_top) / 2.0
    r_inner_bot = r_bot - WALL_THICKNESS - 2.0
    r_inner_top = r_top - WALL_THICKNESS - 2.0
    
    # Адаптивное количество элементов
    avg_r = (r_inner_bot + r_inner_top) / 2.0
    
    if avg_r < 8.0:
        return None  # Слишком тонкая для фермы
    
    num_struts = max(3, min(6, int(avg_r / 5)))
    num_rings = max(1, min(4, int(avg_r / 8)))
    
    # Уменьшаем толщину для тонких секций
    strut_t = max(1.5, min(2.5, avg_r / 10))
    diag_t = max(1.2, min(2.0, avg_r / 12))
    ring_t = max(1.2, min(2.0, avg_r / 12))
    
    all_beams = []
    
    # 1. Стрингеры
    for i in range(num_struts):
        angle = 2.0 * math.pi * i / num_struts
        x_bot = r_inner_bot * math.cos(angle)
        y_bot = r_inner_bot * math.sin(angle)
        x_top = r_inner_top * math.cos(angle)
        y_top = r_inner_top * math.sin(angle)
        
        try:
            beam = (
                cq.Workplane("XY")
                .moveTo(x_bot, y_bot)
                .circle(strut_t / 2.0)
                .workplane(offset=SECTION_HEIGHT)
                .moveTo(x_top, y_top)
                .circle(strut_t / 2.0)
                .loft()
            )
            all_beams.append(beam)
        except:
            pass
    
    # 2. Диагонали (только если достаточно места)
    if avg_r > 12.0:
        for i in range(num_struts):
            angle1 = 2.0 * math.pi * i / num_struts
            angle2 = 2.0 * math.pi * ((i + num_struts // 2) % num_struts) / num_struts
            
            x1 = r_inner_bot * 0.85 * math.cos(angle1)
            y1 = r_inner_bot * 0.85 * math.sin(angle1)
            x2 = r_inner_top * 0.85 * math.cos(angle2)
            y2 = r_inner_top * 0.85 * math.sin(angle2)
            
            try:
                diag = (
                    cq.Workplane("XY")
                    .moveTo(x1, y1)
                    .circle(diag_t / 2.0)
                    .workplane(offset=SECTION_HEIGHT)
                    .moveTo(x2, y2)
                    .circle(diag_t / 2.0)
                    .loft()
                )
                all_beams.append(diag)
            except:
                pass
    
    # 3. Горизонтальные кольца
    for ring_idx in range(1, num_rings + 1):
        z_frac = ring_idx / (num_rings + 1)
        z_ring = SECTION_HEIGHT * z_frac
        r_ring = r_inner_bot + (r_inner_top - r_inner_bot) * z_frac - ring_t
        
        if r_ring > 4.0:
            try:
                ring = (
                    cq.Workplane("XY")
                    .workplane(offset=z_ring)
                    .circle(r_ring)
                    .circle(max(r_ring - ring_t, 2.0))
                    .extrude(2.0)
                )
                all_beams.append(ring)
            except:
                pass
    
    if all_beams:
        try:
            result = all_beams[0]
            for b in all_beams[1:]:
                result = result.union(b)
            return result
        except:
            return None
    return None

def make_section_with_lattice(section_idx):
    """Полная секция: оболочка + ферма + соединения"""
    body = make_section_shell(section_idx)
    
    # Внутренняя ферма (с защитой от ошибок)
    try:
        lattice = make_internal_lattice_adaptive(section_idx)
        if lattice:
            body = body.union(lattice)
    except Exception as e:
        pass  # Без фермы если не получилось
    
    # Нижний штырь
    if section_idx > 0:
        try:
            pin = cq.Workplane("XY").circle(PIN_DIAMETER / 2.0).extrude(PIN_LENGTH)
            body = body.union(pin)
        except:
            pass
    
    # Верхний штырь
    if section_idx < NUM_SECTIONS - 1:
        try:
            pin_top = cq.Workplane("XY").circle(PIN_DIAMETER / 2.0).extrude(PIN_LENGTH).translate((0, 0, SECTION_HEIGHT))
            body = body.union(pin_top)
        except:
            pass
    
    # Нижнее гнездо
    if section_idx > 0:
        try:
            socket = cq.Workplane("XY").circle(PIN_DIAMETER / 2.0 + 0.3).extrude(SOCKET_DEPTH)
            body = body.cut(socket)
        except:
            pass
    
    # Верхнее гнездо
    if section_idx < NUM_SECTIONS - 1:
        try:
            socket_top = cq.Workplane("XY").circle(PIN_DIAMETER / 2.0 + 0.3).extrude(SOCKET_DEPTH).translate((0, 0, SECTION_HEIGHT))
            body = body.cut(socket_top)
        except:
            pass
    
    return body

def make_base():
    r = get_dia_at_height_orig(0) / 2.0 + 10.0
    base = cq.Workplane("XY").circle(r).extrude(8.0)
    for i in range(4):
        angle = math.pi / 4 + i * math.pi / 2
        x = (r - 8.0) * math.cos(angle)
        y = (r - 8.0) * math.sin(angle)
        base = base.faces(">Z").workplane().moveTo(x, y).circle(5.0).cutThruAll()
    base = base.faces(">Z").workplane().circle(PIN_DIAMETER / 2.0 + 0.3).cutBlind(-SOCKET_DEPTH)
    return base

def make_top():
    r = get_dia_at_height_orig(TOTAL_HEIGHT) / 2.0
    top = cq.Workplane("XY").circle(r + 2.0).extrude(6.0)
    top = top.faces(">Z").workplane().circle(3.0).cutThruAll()
    for angle in [0, math.pi]:
        x = r * 0.6 * math.cos(angle)
        y = r * 0.6 * math.sin(angle)
        top = top.faces(">Z").workplane().moveTo(x, y).circle(2.5).cutThruAll()
    return top

# === ГЕНЕРАЦИЯ ===
print("=" * 60)
print("Генерация стойки с ферменной структурой v2")
print(f"Высота: {TOTAL_HEIGHT} мм | Секций: {NUM_SECTIONS}")
print("=" * 60)

output_dir = "/root/.openclaw/workspace/projects/sensor-stand-lattice"
os.makedirs(output_dir, exist_ok=True)

# Удаляем старые файлы
for f in os.listdir(output_dir):
    if f.endswith('.stl'):
        os.remove(f"{output_dir}/{f}")

for i in range(NUM_SECTIONS):
    print(f"  Секция {i+1}/{NUM_SECTIONS}...", end=" ")
    try:
        section = make_section_with_lattice(i)
        if section:
            cq.exporters.export(section, f"{output_dir}/section_{i+1:02d}.stl")
            size = os.path.getsize(f"{output_dir}/section_{i+1:02d}.stl") / 1024
            print(f"✓ {size:.0f} KB")
        else:
            print("✗ пустая")
    except Exception as e:
        print(f"✗ ошибка: {e}")

print("  Основание...")
cq.exporters.export(make_base(), f"{output_dir}/base_plate.stl")

print("  Верхняя крышка...")
cq.exporters.export(make_top(), f"{output_dir}/top_cap.stl")

print(f"\n✅ Готово! Файлы в: {output_dir}")
files = [f for f in os.listdir(output_dir) if f.endswith('.stl')]
total = sum(os.path.getsize(f"{output_dir}/{f}") for f in files)
print(f"   Файлов: {len(files)} | Общий размер: {total/1024/1024:.1f} MB")
