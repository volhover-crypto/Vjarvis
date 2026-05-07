// LoRaWAN Modem LVM-485-SOLAR-01
// 3D PCB Model
// Board: 100x150x1.6mm, 4-layer FR-4

$fn = 32;

board_width = 100;
board_height = 150;
board_thickness = 1.6;
hole_diameter = 3.2;
hole_offset = 5;

// PCB material color (FR-4 green)
pcb_color = [0.1, 0.4, 0.15];
copper_color = [0.8, 0.5, 0.2];
silkscreen_color = [0.9, 0.9, 0.9];

module board_outline() {
    // Main board
    color(pcb_color)
    cube([board_width, board_height, board_thickness]);
    
    // Copper layers (thin)
    color(copper_color)
    translate([0, board_height, board_thickness/2 - 0.02])
    cube([board_width, board_height, 0.04]);
}

module mounting_holes() {
    positions = [
        [hole_offset, hole_offset],
        [board_width - hole_offset, hole_offset],
        [board_width - hole_offset, board_height - hole_offset],
        [hole_offset, board_height - hole_offset]
    ];
    
    for (pos = positions) {
        translate([pos[0], pos[1], -0.1])
        cylinder(d = hole_diameter, h = board_thickness + 0.2);
    }
}

module component_3d(name, x, y, w, h, t, color_val) {
    translate([x, y, board_thickness])
    color(color_val)
    cube([w, h, t]);
}

// Main PCB
difference() {
    board_outline();
    mounting_holes();
}

// Components (simplified 3D representations)

// MCU (center) - QFN-48
component_3d("U4", 46.5, 71.5, 7, 7, 1.0, [0.1, 0.1, 0.1]);

// Charge controller (left-center) - QFN-24
component_3d("U1", 23, 28, 4, 4, 0.9, [0.1, 0.1, 0.1]);

// DC-DC (center-bottom) - DSBGA-8
component_3d("U2", 49, 19, 1.6, 1.6, 0.5, [0.1, 0.1, 0.1]);

// LDO (center) - SOT-23-5
component_3d("U3", 49, 39, 1.5, 3, 1.0, [0.1, 0.1, 0.1]);

// RS-485 (right) - SOIC-20
component_3d("U5", 76, 35, 7.5, 12.8, 2.5, [0.1, 0.1, 0.1]);

// Flash (right-center) - SOIC-8
component_3d("U6", 73, 73, 3.9, 4.9, 1.7, [0.1, 0.1, 0.1]);

// Fuel gauge (right-bottom) - TDFN-8
component_3d("U7", 74, 24, 2, 3, 0.8, [0.1, 0.1, 0.1]);

// Crystals
component_3d("Y1", 33, 73, 3.2, 2.5, 1.0, [0.7, 0.7, 0.8]);
component_3d("Y2", 63, 63, 3.2, 1.5, 0.8, [0.7, 0.7, 0.8]);

// Inductors
component_3d("L1", 42, 28, 7.3, 7.3, 3.5, [0.3, 0.3, 0.3]);
component_3d("L2", 59, 19, 2.0, 1.6, 1.0, [0.3, 0.3, 0.3]);

// Capacitors (sample)
component_3d("C1", 38, 8, 3.2, 2.5, 1.5, [0.6, 0.5, 0.3]);
component_3d("C3", 63, 18, 2.0, 1.25, 1.0, [0.6, 0.5, 0.3]);

// Connectors
// Solar input J1
color([0.9, 0.9, 0.7])
translate([8, 8, board_thickness])
cube([4, 5, 3]);

// Battery J2
color([0.9, 0.9, 0.7])
translate([78, 8, board_thickness])
cube([4, 5, 3]);

// Antenna J4 (SMA)
color([0.8, 0.8, 0.8])
translate([2, 92, board_thickness])
cube([6, 6, 4]);

// RS-485 J5 (screw terminal)
color([0.2, 0.6, 0.2])
translate([92, 47, board_thickness])
cube([6, 8, 5]);

// SWD J6
color([0.9, 0.9, 0.9])
translate([37, 3, board_thickness])
cube([6, 3, 2]);

// UART J7
color([0.9, 0.9, 0.9])
translate([52, 3, board_thickness])
cube([6, 3, 2]);

// LEDs (top edge)
led_colors = [
    [0.0, 0.8, 0.0],  // Green
    [0.0, 0.0, 0.8],  // Blue
    [0.8, 0.8, 0.0],  // Yellow
    [0.8, 0.0, 0.0]   // Red
];

for (i = [0:3]) {
    translate([18 + i*15, 138, board_thickness])
    color(led_colors[i])
    cube([1.6, 0.8, 0.5]);
}

// Silkscreen labels
color(silkscreen_color)
translate([50, 140, board_thickness + 0.01])
linear_extrude(height = 0.1)
text("LVM-485-SOLAR-01", size = 2.5, halign = "center");

color(silkscreen_color)
translate([50, 145, board_thickness + 0.01])
linear_extrude(height = 0.1)
text("Rev 0.1 | AgroELEMENT", size = 1.5, halign = "center");
