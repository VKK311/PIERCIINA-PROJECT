"""Render stills / panoramas from apartment.blend.

usage: python render.py <view> <out.png> [--res WxH] [--samples N] [--mode day|evening] [--exposure E]
"""
import bpy, math, sys, os
from mathutils import Vector

args = sys.argv[1:]
view, out = args[0], args[1]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


res = opt("--res", "1600x1000")
samples = int(opt("--samples", "128"))
mode = opt("--mode", "day")
exposure = float(opt("--exposure", "0.0"))
HERE = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "apartment.blend"))
scene = bpy.context.scene
D = bpy.data
H = 2.60

# name: (eye x, y, z, target x, y, z, focal mm)
VIEWS = {
    "entrance": (2.73, 0.40, 1.50, 2.05, 8.1, 1.15, 18),
    "kitchen": (2.85, 4.20, 1.40, 0.6, 2.2, 1.15, 17),
    "dining": (0.75, 3.55, 1.40, 3.5, 5.9, 1.05, 17),
    "tv": (3.60, 4.85, 1.15, 0.0, 5.65, 1.15, 19),
    "reading": (1.05, 5.70, 1.40, 3.3, 8.0, 1.10, 18),
    "work": (2.62, 6.45, 1.40, 0.2, 7.65, 1.10, 18),
    "back": (2.30, 7.75, 1.50, 1.6, 1.5, 1.20, 16),
    "bath": (1.62, 0.36, 1.60, 0.15, 1.45, 1.05, 12),
    "bath2": (1.55, 0.98, 1.55, 1.05, 0.0, 1.25, 15),
}
PANOS = {
    "p_hall": (2.75, 1.05, 1.55),
    "p_kitchen": (1.55, 3.30, 1.55),
    "p_dining": (1.25, 5.20, 1.55),
    "p_living": (2.30, 6.90, 1.55),
    "p_bath": (1.55, 0.72, 1.55),
}

cam_data = D.cameras.new("cam")
cam = D.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam_data.clip_start = 0.02
cam_data.sensor_width = 36
W, Hh = map(int, res.split("x"))
scene.render.resolution_x, scene.render.resolution_y = W, Hh
scene.render.resolution_percentage = 100

if view in VIEWS:
    ex, ey, ez, tx, ty, tz, f = VIEWS[view]
    d = Vector((tx - ex, ty - ey, 0)).normalized()
    cam.location = (ex, ey, ez)
    yaw = math.atan2(-d.x, d.y)
    cam.rotation_euler = (math.radians(90), 0, yaw)
    cam_data.lens = f
    # two-point perspective: keep verticals straight, frame with lens shift
    dist = Vector((tx - ex, ty - ey)).length
    sensor_h = 36 * Hh / W if W >= Hh else 36
    cam_data.sensor_fit = "HORIZONTAL"
    shift = ((tz - ez) / dist) * f / 36
    cam_data.shift_y = max(-0.25, min(0.25, shift))
elif view in PANOS:
    cam.location = PANOS[view]
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam_data.type = "PANO"
    cam_data.panorama_type = "EQUIRECTANGULAR"
elif view == "plan":
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = 9.0
    cam.location = (1.95, 4.05, 20)
    cam.rotation_euler = (0, 0, 0)
    for ob in D.objects:
        if ob.name.startswith(("Таван", "Шина", "Спот", "Розетка", "Кабел", "Пендел", "Крушка пендел", "Плафон", "Аспиратор комин",
                               "Колона пълнеж", "Гардероб пълнеж", "Корниз", "Перде")):
            ob.hide_render = True
    for ob in D.objects:
        if ob.name.startswith("Стена") and ob.dimensions.z > 0.5:
            pass
elif view == "iso":
    cam_data.lens = 30
    cam.location = (8.6, -3.2, 9.6)
    d = Vector((1.95, 4.3, 0.2)) - Vector(cam.location)
    cam.rotation_euler = Vector((0, 0, -1)).rotation_difference(d).to_track_quat("-Z", "Y").to_euler()
    for ob in D.objects:
        if ob.name.startswith(("Таван", "Перде")):
            ob.hide_render = True

# lighting mode
groups_day_on = {"pendant", "led", "vitrine", "bath", "hall"}
sky_bg = scene.world.node_tree.nodes["sky_bg"]
sun = D.objects["Слънце"]
for ob in D.objects:
    if ob.type == "LIGHT" and "group" in ob:
        on = mode == "evening" or ob["group"] in groups_day_on
        ob.hide_render = not on
if mode == "evening":
    sun.hide_render = True
    sky = scene.world.node_tree.nodes["Sky Texture"]
    sky.sun_elevation = math.radians(-3.5)
    sky_bg.inputs["Strength"].default_value = 0.9
    for m in D.materials:
        if m.name == "ТВ екран":
            m.node_tree.nodes["screen_emit"].inputs["Strength"].default_value = 1.2
else:
    m = D.materials.get("Абажур лампи")
    if m:
        m.node_tree.nodes["Emission"].inputs["Strength"].default_value = 0.0
if mode == "day":
    # lamps that are switched off by day: kill their shade glow
    pass

scene.cycles.samples = samples
scene.view_settings.exposure = exposure
scene.render.image_settings.file_format = "PNG" if out.endswith(".png") else "JPEG"
if out.endswith(".jpg"):
    scene.render.image_settings.quality = 92
scene.render.filepath = out
scene.cycles.use_animated_seed = False
scene.render.use_persistent_data = False
bpy.ops.render.render(write_still=True)
print("rendered", out)
