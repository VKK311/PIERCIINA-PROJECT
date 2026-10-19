"""Builds the studio apartment in Blender (plan coordinates: x = across 0..3.90, y = along 0..8.10, z up).

Source plan: Apartment_Plan_A3_1-50.pdf (interior 390 x 810 cm).
"""
import bpy, bmesh, math, random, os, sys
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")
OUT_BLEND = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(HERE, "apartment.blend")

bpy.ops.wm.read_factory_settings(use_empty=True)
D = bpy.data
scene = bpy.context.scene
COL = scene.collection
H = 2.60
R = random.Random(42)
WORLD_UV = []


# ---------------------------------------------------------------- helpers
def srgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)


def link(ob, parent=None):
    COL.objects.link(ob)
    if parent is not None:
        ob.parent = parent
    return ob


def smooth_bm(bm, angle=0.6):
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(0) > angle:
            e.smooth = False


def mesh_obj(name, bm, mat, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    me = D.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = D.objects.new(name, me)
    ob.location = loc
    ob.rotation_euler = rot
    if mat is not None:
        if isinstance(mat, (list, tuple)):
            for m in mat:
                me.materials.append(m)
        else:
            me.materials.append(mat)
    return link(ob, parent)


JIT = random.Random(7)


def box(name, x0, x1, y0, y1, z0, z1, mat, parent=None, bevel=0.0, seg=2, wuv=False, smooth=False, jit=True):
    if jit:  # break exact coplanarity between overlapping parts (avoids black self-shadow squares in Cycles)
        j = [JIT.uniform(0.0002, 0.0009) for _ in range(6)]
        x0, x1, y0, y1, z0, z1 = x0 + j[0], x1 - j[1], y0 + j[2], y1 - j[3], z0 + j[4], z1 - j[5]
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= (x1 - x0)
        v.co.y *= (y1 - y0)
        v.co.z *= (z1 - z0)
    if smooth:
        for f in bm.faces:
            f.smooth = True
    ob = mesh_obj(name, bm, mat, parent, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    if bevel > 0:
        m = ob.modifiers.new("bevel", "BEVEL")
        m.width = bevel
        m.segments = seg
        m.limit_method = "ANGLE"
        m.harden_normals = smooth
    if wuv:
        WORLD_UV.append(ob)
    return ob


def soft(ob, bevel, seg=3, sub=2):
    """Rounded upholstery: bevel + subdivision, smooth shading."""
    for p in ob.data.polygons:
        p.use_smooth = True
    m = ob.modifiers.new("bevel", "BEVEL")
    m.width = bevel
    m.segments = seg
    m.limit_method = "NONE"
    if sub:
        s = ob.modifiers.new("sub", "SUBSURF")
        s.levels = sub
        s.render_levels = sub
    return ob


def cyl(name, r, h, loc, mat, parent=None, axis="Z", segs=32, r2=None, rot=None, wuv=False):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r,
                          radius2=r if r2 is None else r2, depth=h)
    smooth_bm(bm)
    if rot is None:
        rot = {"Z": (0, 0, 0), "X": (0, math.pi / 2, 0), "Y": (math.pi / 2, 0, 0)}[axis]
    ob = mesh_obj(name, bm, mat, parent, loc, rot)
    if wuv:
        WORLD_UV.append(ob)
    return ob


def sphere(name, r, loc, mat, parent=None, scale=(1, 1, 1), segs=24, rings=12):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=r)
    for f in bm.faces:
        f.smooth = True
    ob = mesh_obj(name, bm, mat, parent, loc)
    ob.scale = scale
    return ob


def lathe(name, prof, loc, mat, parent=None, segs=48, angle=0.5):
    """prof: list of (radius, z). Builds a surface of revolution around Z."""
    bm = bmesh.new()
    rings = []
    for r, z in prof:
        ring = []
        for i in range(segs):
            a = 2 * math.pi * i / segs
            ring.append(bm.verts.new((r * math.cos(a), r * math.sin(a), z)))
        rings.append(ring)
    for j in range(len(rings) - 1):
        for i in range(segs):
            a, b = rings[j][i], rings[j][(i + 1) % segs]
            c, d = rings[j + 1][(i + 1) % segs], rings[j + 1][i]
            try:
                bm.faces.new((a, b, c, d))
            except ValueError:
                pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    smooth_bm(bm, angle)
    return mesh_obj(name, bm, mat, parent, loc)


def tube(name, pts, r, mat, parent=None, res=6):
    cu = D.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for p, co in zip(sp.bezier_points, pts):
        p.co = co
        p.handle_left_type = p.handle_right_type = "AUTO"
    cu.bevel_depth = r
    cu.bevel_resolution = res
    cu.use_fill_caps = True
    ob = D.objects.new(name, cu)
    ob.data.materials.append(mat)
    return link(ob, parent)


def poly_tube(name, pts, r, mat, parent=None):
    cu = D.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, co in zip(sp.points, pts):
        p.co = (co[0], co[1], co[2], 1)
    cu.bevel_depth = r
    cu.bevel_resolution = 4
    cu.use_fill_caps = True
    ob = D.objects.new(name, cu)
    ob.data.materials.append(mat)
    return link(ob, parent)


def empty(name, x, y, rz=0.0, z=0.0, parent=None):
    e = D.objects.new(name, None)
    e.location = (x, y, z)
    e.rotation_euler = (0, 0, rz)
    return link(e, parent)


FACE = {"S": 0.0, "E": math.pi / 2, "N": math.pi, "W": -math.pi / 2}  # front (local -Y) faces this way


def world_uvs():
    bpy.context.view_layer.update()
    for ob in WORLD_UV:
        me = ob.data
        if not me.uv_layers:
            me.uv_layers.new(name="UVMap")
        uv = me.uv_layers.active.data
        mw = ob.matrix_world
        nm = mw.to_3x3().inverted().transposed()
        for poly in me.polygons:
            n = (nm @ poly.normal).normalized()
            ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
            for li in poly.loop_indices:
                p = mw @ me.vertices[me.loops[li].vertex_index].co
                if az >= ax and az >= ay:
                    uv[li].uv = (p.x, p.y)
                elif ax >= ay:
                    uv[li].uv = (p.y, p.z)
                else:
                    uv[li].uv = (p.x, p.z)


# ---------------------------------------------------------------- materials
def newmat(name):
    m = D.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    return m, nt, out


def node(nt, t, **kw):
    n = nt.nodes.new(t)
    for k, v in kw.items():
        setattr(n, k, v)
    return n


def sock(n, ident, out=False):
    for s in (n.outputs if out else n.inputs):
        if s.identifier == ident:
            return s
    raise KeyError(ident)


def lk(nt, a, b):
    nt.links.new(a, b)


def principled(nt, color=None, rough=0.5, metal=0.0, **kw):
    p = nt.nodes.new("ShaderNodeBsdfPrincipled")
    if color is not None:
        p.inputs["Base Color"].default_value = srgb(color) if isinstance(color, str) else color
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    for k, v in kw.items():
        key = k.replace("_", " ")
        val = srgb(v) if isinstance(v, str) else v
        p.inputs[key].default_value = val
    return p


def ramp(nt, stops):
    r = nt.nodes.new("ShaderNodeValToRGB")
    els = r.color_ramp.elements
    for i, (pos, col) in enumerate(stops):
        e = els[i] if i < len(els) else els.new(pos)
        e.position = pos
        e.color = srgb(col) if isinstance(col, str) else col
    return r


def mix_rgb(nt, fac, a, b, blend="MIX"):
    m = nt.nodes.new("ShaderNodeMix")
    m.data_type = "RGBA"
    m.blend_type = blend
    if isinstance(fac, (int, float)):
        sock(m, "Factor_Float").default_value = fac
    else:
        lk(nt, fac, sock(m, "Factor_Float"))
    for ident, v in (("A_Color", a), ("B_Color", b)):
        if isinstance(v, str):
            sock(m, ident).default_value = srgb(v)
        elif isinstance(v, tuple):
            sock(m, ident).default_value = v
        else:
            lk(nt, v, sock(m, ident))
    return sock(m, "Result_Color", out=True)


def bump(nt, height, strength=0.1, dist=0.01, normal=None):
    b = nt.nodes.new("ShaderNodeBump")
    b.inputs["Strength"].default_value = strength
    b.inputs["Distance"].default_value = dist
    lk(nt, height, b.inputs["Height"])
    if normal is not None:
        lk(nt, normal, b.inputs["Normal"])
    return b.outputs["Normal"]


def uvmap(nt, scale=(1, 1, 1), loc=(0, 0, 0), coord="UV"):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = scale
    mp.inputs["Location"].default_value = loc
    lk(nt, tc.outputs[coord], mp.inputs["Vector"])
    return mp.outputs["Vector"], tc


def paint(name, color, rough=0.82, bumpy=0.012):
    m, nt, out = newmat(name)
    p = principled(nt, color, rough)
    p.inputs["Specular IOR Level"].default_value = 0.35
    vec, _ = uvmap(nt, coord="Object")
    nz = node(nt, "ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 180
    nz.inputs["Detail"].default_value = 6
    lk(nt, vec, nz.inputs["Vector"])
    lk(nt, bump(nt, nz.outputs["Fac"], bumpy, 0.004), p.inputs["Normal"])
    lk(nt, p.outputs[0], out.inputs[0])
    return m


def simple(name, color, rough=0.5, metal=0.0, **kw):
    m, nt, out = newmat(name)
    p = principled(nt, color, rough, metal, **kw)
    lk(nt, p.outputs[0], out.inputs[0])
    return m


def wood(name, light="#D2B08A", dark="#A27C58", axis="X", rough=0.42, per_plank=False, scale_mul=1.0, coat=0.0):
    """Procedural oak. Grain runs along the UV axis that is NOT `axis` (bands vary along `axis`)."""
    m, nt, out = newmat(name)
    tc = node(nt, "ShaderNodeTexCoord")
    vec = tc.outputs["UV"]
    if per_plank:
        at = node(nt, "ShaderNodeAttribute", attribute_name="rnd", attribute_type="GEOMETRY")
        off = node(nt, "ShaderNodeCombineXYZ")
        mul = node(nt, "ShaderNodeMath", operation="MULTIPLY")
        mul.inputs[1].default_value = 37.0
        lk(nt, at.outputs["Fac"], mul.inputs[0])
        lk(nt, mul.outputs[0], off.inputs[0])
        lk(nt, mul.outputs[0], off.inputs[1])
        lk(nt, mul.outputs[0], off.inputs[2])
        add = node(nt, "ShaderNodeVectorMath", operation="ADD")
        lk(nt, vec, add.inputs[0])
        lk(nt, off.outputs[0], add.inputs[1])
        vec = add.outputs[0]
    # stretch so features elongate along grain
    mp = node(nt, "ShaderNodeMapping")
    s_along, s_across = 0.08 * scale_mul, 1.0 * scale_mul
    mp.inputs["Scale"].default_value = (s_across, s_along, 1) if axis == "X" else (s_along, s_across, 1)
    lk(nt, vec, mp.inputs["Vector"])
    v = mp.outputs["Vector"]
    wave = node(nt, "ShaderNodeTexWave", wave_type="BANDS", bands_direction=axis, wave_profile="SIN")
    wave.inputs["Scale"].default_value = 42
    wave.inputs["Distortion"].default_value = 7
    wave.inputs["Detail"].default_value = 4
    wave.inputs["Detail Scale"].default_value = 1.4
    lk(nt, v, wave.inputs["Vector"])
    nz = node(nt, "ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 9
    nz.inputs["Detail"].default_value = 8
    lk(nt, v, nz.inputs["Vector"])
    fine = node(nt, "ShaderNodeTexNoise")
    fine.inputs["Scale"].default_value = 260
    fine.inputs["Detail"].default_value = 4
    lk(nt, v, fine.inputs["Vector"])
    g = node(nt, "ShaderNodeMath", operation="MULTIPLY_ADD")
    lk(nt, wave.outputs["Fac"], g.inputs[0])
    g.inputs[1].default_value = 0.55
    lk(nt, nz.outputs["Fac"], g.inputs[2])
    rp = ramp(nt, [(0.35, light), (0.95, dark)])
    lk(nt, g.outputs[0], rp.inputs["Fac"])
    col = rp.outputs["Color"]
    if per_plank:
        hs = node(nt, "ShaderNodeHueSaturation")
        mv = node(nt, "ShaderNodeMapRange")
        mv.inputs["To Min"].default_value = 0.86
        mv.inputs["To Max"].default_value = 1.10
        lk(nt, at.outputs["Fac"], mv.inputs["Value"])
        lk(nt, mv.outputs[0], hs.inputs["Value"])
        mh = node(nt, "ShaderNodeMapRange")
        mh.inputs["To Min"].default_value = 0.485
        mh.inputs["To Max"].default_value = 0.515
        lk(nt, at.outputs["Fac"], mh.inputs["Value"])
        lk(nt, mh.outputs[0], hs.inputs["Hue"])
        lk(nt, col, hs.inputs["Color"])
        col = hs.outputs["Color"]
    p = principled(nt, None, rough)
    p.inputs["Coat Weight"].default_value = coat
    lk(nt, col, p.inputs["Base Color"])
    rr = node(nt, "ShaderNodeMapRange")
    rr.inputs["To Min"].default_value = rough - 0.08
    rr.inputs["To Max"].default_value = rough + 0.12
    lk(nt, fine.outputs["Fac"], rr.inputs["Value"])
    lk(nt, rr.outputs[0], p.inputs["Roughness"])
    h = node(nt, "ShaderNodeMath", operation="ADD")
    lk(nt, wave.outputs["Fac"], h.inputs[0])
    lk(nt, fine.outputs["Fac"], h.inputs[1])
    lk(nt, bump(nt, h.outputs[0], 0.06, 0.002), p.inputs["Normal"])
    lk(nt, p.outputs[0], out.inputs[0])
    return m


def tiles(name, w, h, c1, c2, grout, rough=0.12, offset=0.5, mortar=0.0025, wavy=0.0, var_scale=0.0, coat=0.6, nscale=18):
    m, nt, out = newmat(name)
    vec, tc = uvmap(nt)
    br = node(nt, "ShaderNodeTexBrick", offset=offset, offset_frequency=2, squash=1.0, squash_frequency=2)
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = w
    br.inputs["Row Height"].default_value = h
    br.inputs["Mortar Size"].default_value = mortar
    br.inputs["Mortar Smooth"].default_value = 0.35
    br.inputs["Bias"].default_value = 0.0
    br.inputs["Color1"].default_value = srgb(c1)
    br.inputs["Color2"].default_value = srgb(c2)
    br.inputs["Mortar"].default_value = srgb(grout)
    lk(nt, vec, br.inputs["Vector"])
    col = br.outputs["Color"]
    nz = node(nt, "ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = nscale
    nz.inputs["Detail"].default_value = 5
    lk(nt, vec, nz.inputs["Vector"])
    if var_scale:
        col = mix_rgb(nt, var_scale, col, nz.outputs["Fac"], "OVERLAY")
    p = principled(nt, None, rough)
    p.inputs["Coat Weight"].default_value = coat
    p.inputs["Coat Roughness"].default_value = 0.05
    lk(nt, col, p.inputs["Base Color"])
    inv = node(nt, "ShaderNodeMath", operation="SUBTRACT")
    inv.inputs[0].default_value = 1.0
    lk(nt, br.outputs["Fac"], inv.inputs[1])
    hgt = inv.outputs[0]
    if wavy:
        add = node(nt, "ShaderNodeMath", operation="MULTIPLY_ADD")
        lk(nt, nz.outputs["Fac"], add.inputs[0])
        add.inputs[1].default_value = wavy
        lk(nt, hgt, add.inputs[2])
        hgt = add.outputs[0]
    lk(nt, bump(nt, hgt, 0.35, 0.004), p.inputs["Normal"])
    lk(nt, p.outputs[0], out.inputs[0])
    return m


def checker_tiles(name, size, ca, cb, grout):
    m, nt, out = newmat(name)
    vec, tc = uvmap(nt)
    sep = node(nt, "ShaderNodeSeparateXYZ")
    lk(nt, vec, sep.inputs[0])
    parts = []
    for i in (0, 1):
        dv = node(nt, "ShaderNodeMath", operation="DIVIDE")
        lk(nt, sep.outputs[i], dv.inputs[0])
        dv.inputs[1].default_value = size
        fl = node(nt, "ShaderNodeMath", operation="FLOOR")
        lk(nt, dv.outputs[0], fl.inputs[0])
        parts.append(fl.outputs[0])
    ad = node(nt, "ShaderNodeMath", operation="ADD")
    lk(nt, parts[0], ad.inputs[0])
    lk(nt, parts[1], ad.inputs[1])
    md = node(nt, "ShaderNodeMath", operation="FLOORED_MODULO")
    lk(nt, ad.outputs[0], md.inputs[0])
    md.inputs[1].default_value = 2
    col = mix_rgb(nt, md.outputs[0], ca, cb)
    br = node(nt, "ShaderNodeTexBrick", offset=0.0)
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = size
    br.inputs["Row Height"].default_value = size
    br.inputs["Mortar Size"].default_value = 0.002
    br.inputs["Mortar Smooth"].default_value = 0.3
    lk(nt, vec, br.inputs["Vector"])
    col = mix_rgb(nt, br.outputs["Fac"], col, grout)
    p = principled(nt, None, 0.35)
    lk(nt, col, p.inputs["Base Color"])
    inv = node(nt, "ShaderNodeMath", operation="SUBTRACT")
    inv.inputs[0].default_value = 1
    lk(nt, br.outputs["Fac"], inv.inputs[1])
    lk(nt, bump(nt, inv.outputs[0], 0.3, 0.003), p.inputs["Normal"])
    lk(nt, p.outputs[0], out.inputs[0])
    return m


def image_mat(name, path, size, rough=0.8, sheen=0.0, bump_img=None, bump_strength=0.2, uv_coord="UV", scale=None):
    m, nt, out = newmat(name)
    sc = scale or (1 / size[0], 1 / size[1], 1)
    vec, _ = uvmap(nt, sc, coord=uv_coord)
    im = node(nt, "ShaderNodeTexImage")
    im.image = D.images.load(path)
    im.interpolation = "Cubic"
    lk(nt, vec, im.inputs["Vector"])
    p = principled(nt, None, rough)
    p.inputs["Sheen Weight"].default_value = sheen
    lk(nt, im.outputs["Color"], p.inputs["Base Color"])
    if bump_img:
        bi = node(nt, "ShaderNodeTexImage")
        bi.image = D.images.load(bump_img)
        bi.image.colorspace_settings.name = "Non-Color"
        lk(nt, vec, bi.inputs["Vector"])
        lk(nt, bump(nt, bi.outputs["Color"], bump_strength, 0.003), p.inputs["Normal"])
    lk(nt, p.outputs[0], out.inputs[0])
    return m


def fabric(name, color, rough=0.85, sheen=0.6, scale=320, strength=0.25, boucle=False):
    m, nt, out = newmat(name)
    vec, _ = uvmap(nt, coord="Object")
    p = principled(nt, color, rough)
    p.inputs["Sheen Weight"].default_value = sheen
    p.inputs["Sheen Roughness"].default_value = 0.4
    if boucle:
        vo = node(nt, "ShaderNodeTexVoronoi")
        vo.inputs["Scale"].default_value = scale
        lk(nt, vec, vo.inputs["Vector"])
        h = vo.outputs["Distance"]
        nz = node(nt, "ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 40
        lk(nt, vec, nz.inputs["Vector"])
        cmix = mix_rgb(nt, 0.12, color, nz.outputs["Fac"], "OVERLAY")
        lk(nt, cmix, p.inputs["Base Color"])
    else:
        w1 = node(nt, "ShaderNodeTexWave", wave_type="BANDS", bands_direction="X")
        w1.inputs["Scale"].default_value = scale
        w2 = node(nt, "ShaderNodeTexWave", wave_type="BANDS", bands_direction="Z")
        w2.inputs["Scale"].default_value = scale
        lk(nt, vec, w1.inputs["Vector"])
        lk(nt, vec, w2.inputs["Vector"])
        mx = node(nt, "ShaderNodeMath", operation="MULTIPLY")
        lk(nt, w1.outputs["Fac"], mx.inputs[0])
        lk(nt, w2.outputs["Fac"], mx.inputs[1])
        nz = node(nt, "ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 60
        nz.inputs["Detail"].default_value = 6
        lk(nt, vec, nz.inputs["Vector"])
        hh = node(nt, "ShaderNodeMath", operation="MULTIPLY_ADD")
        lk(nt, nz.outputs["Fac"], hh.inputs[0])
        hh.inputs[1].default_value = 0.6
        lk(nt, mx.outputs[0], hh.inputs[2])
        h = hh.outputs[0]
        cmix = mix_rgb(nt, 0.08, color, nz.outputs["Fac"], "OVERLAY")
        lk(nt, cmix, p.inputs["Base Color"])
    lk(nt, bump(nt, h, strength, 0.002), p.inputs["Normal"])
    lk(nt, p.outputs[0], out.inputs[0])
    return m


def window_glass(name, tint="#EEF3F2"):
    m, nt, out = newmat(name)
    g = principled(nt, tint, 0.0, IOR=1.5)
    g.inputs["Transmission Weight"].default_value = 1.0
    tr = node(nt, "ShaderNodeBsdfTransparent")
    lp = node(nt, "ShaderNodeLightPath")
    mx = node(nt, "ShaderNodeMath", operation="MAXIMUM")
    lk(nt, lp.outputs["Is Shadow Ray"], mx.inputs[0])
    lk(nt, lp.outputs["Is Diffuse Ray"], mx.inputs[1])
    ms = node(nt, "ShaderNodeMixShader")
    lk(nt, mx.outputs[0], ms.inputs[0])
    lk(nt, g.outputs[0], ms.inputs[1])
    lk(nt, tr.outputs[0], ms.inputs[2])
    lk(nt, ms.outputs[0], out.inputs[0])
    return m


def emissive(name, color="#FFE2B8", strength=6.0, base=None, translucent=False):
    m, nt, out = newmat(name)
    em = node(nt, "ShaderNodeEmission")
    em.inputs["Color"].default_value = srgb(color)
    em.inputs["Strength"].default_value = strength
    if base or translucent:
        if translucent:
            b = node(nt, "ShaderNodeBsdfTranslucent")
            b.inputs["Color"].default_value = srgb(base or "#F3E9DA")
        else:
            b = principled(nt, base, 0.6)
        ad = node(nt, "ShaderNodeAddShader")
        lk(nt, b.outputs[0], ad.inputs[0])
        lk(nt, em.outputs[0], ad.inputs[1])
        lk(nt, ad.outputs[0], out.inputs[0])
    else:
        lk(nt, em.outputs[0], out.inputs[0])
    return m


def sheer(name, color="#F7F4EE"):
    m, nt, out = newmat(name)
    tl = node(nt, "ShaderNodeBsdfTranslucent")
    tl.inputs["Color"].default_value = srgb(color)
    tr = node(nt, "ShaderNodeBsdfTransparent")
    df = principled(nt, color, 0.9)
    df.inputs["Sheen Weight"].default_value = 0.5
    m1 = node(nt, "ShaderNodeMixShader")
    m1.inputs[0].default_value = 0.30
    lk(nt, tr.outputs[0], m1.inputs[1])
    lk(nt, tl.outputs[0], m1.inputs[2])
    m2 = node(nt, "ShaderNodeMixShader")
    m2.inputs[0].default_value = 0.14
    lk(nt, m1.outputs[0], m2.inputs[1])
    lk(nt, df.outputs[0], m2.inputs[2])
    lk(nt, m2.outputs[0], out.inputs[0])
    return m


def leafmat(name, c1, c2):
    m, nt, out = newmat(name)
    at = node(nt, "ShaderNodeAttribute", attribute_name="rnd", attribute_type="GEOMETRY")
    col = mix_rgb(nt, at.outputs["Fac"], c1, c2)
    p = principled(nt, None, 0.45)
    p.inputs["Subsurface Weight"].default_value = 0.0
    lk(nt, col, p.inputs["Base Color"])
    tl = node(nt, "ShaderNodeBsdfTranslucent")
    lk(nt, col, tl.inputs["Color"])
    ms = node(nt, "ShaderNodeMixShader")
    ms.inputs[0].default_value = 0.3
    lk(nt, p.outputs[0], ms.inputs[1])
    lk(nt, tl.outputs[0], ms.inputs[2])
    lk(nt, ms.outputs[0], out.inputs[0])
    return m


def beadboard(name, color, pitch=0.10):
    m, nt, out = newmat(name)
    tc = node(nt, "ShaderNodeTexCoord")
    sep = node(nt, "ShaderNodeSeparateXYZ")
    lk(nt, tc.outputs["UV"], sep.inputs[0])
    dv = node(nt, "ShaderNodeMath", operation="DIVIDE")
    lk(nt, sep.outputs[0], dv.inputs[0])
    dv.inputs[1].default_value = pitch
    fr = node(nt, "ShaderNodeMath", operation="FRACT")
    lk(nt, dv.outputs[0], fr.inputs[0])
    rp = ramp(nt, [(0.0, (0, 0, 0, 1)), (0.03, (1, 1, 1, 1))])
    rp.color_ramp.elements.new(0.97).color = (1, 1, 1, 1)
    e = rp.color_ramp.elements.new(1.0)
    e.color = (0.3, 0.3, 0.3, 1)
    lk(nt, fr.outputs[0], rp.inputs["Fac"])
    p = principled(nt, color, 0.5)
    p.inputs["Specular IOR Level"].default_value = 0.4
    occl = mix_rgb(nt, 0.35, color, rp.outputs["Color"], "MULTIPLY")
    lk(nt, occl, p.inputs["Base Color"])
    lk(nt, bump(nt, rp.outputs["Color"], 0.6, 0.004), p.inputs["Normal"])
    lk(nt, p.outputs[0], out.inputs[0])
    return m


def tv_screen(name):
    m, nt, out = newmat(name)
    im = node(nt, "ShaderNodeTexImage")
    im.image = D.images.load(os.path.join(TEX, "tv.png"))
    tc = node(nt, "ShaderNodeTexCoord")
    mp = node(nt, "ShaderNodeMapping")
    mp.inputs["Location"].default_value = (-4.892 / 1.21, -0.96 / 0.69, 0)
    mp.inputs["Scale"].default_value = (1 / 1.21, 1 / 0.69, 1)
    lk(nt, tc.outputs["UV"], mp.inputs["Vector"])
    lk(nt, mp.outputs["Vector"], im.inputs["Vector"])
    em = node(nt, "ShaderNodeEmission")
    em.inputs["Strength"].default_value = 0.0
    em.name = "screen_emit"
    lk(nt, im.outputs["Color"], em.inputs["Color"])
    gl = principled(nt, "#050606", 0.06)
    ad = node(nt, "ShaderNodeAddShader")
    lk(nt, gl.outputs[0], ad.inputs[0])
    lk(nt, em.outputs[0], ad.inputs[1])
    lk(nt, ad.outputs[0], out.inputs[0])
    return m


M = {}
M["wall"] = paint("Стени топло бяло", "#EEE9E1")
M["ceil"] = paint("Таван", "#F4F2EE", 0.9, 0.006)
M["pink"] = paint("Стени пепел от рози", "#C4877A")
M["sage_paint"] = paint("Шалвия боя", "#8C9C89", 0.55)
M["cab"] = simple("Фронтове мръсно бяло", "#ECE8DF", 0.38, Specular_IOR_Level=0.45)
M["cab_in"] = simple("Корпус вътре", "#E7E2D8", 0.55)
M["white_satin"] = simple("Бяла сатенена боя", "#EFECE6", 0.32)
M["hood"] = simple("Аспиратор бял", "#F1F0EC", 0.25)
M["hemnes"] = simple("HEMNES сиво-зелено", "#8B9C8B", 0.5, Specular_IOR_Level=0.45)
M["hemnes_bead"] = beadboard("HEMNES ламперия", "#8B9C8B", 0.085)
M["bead"] = beadboard("Ламперия шалвия", "#7F917F", 0.10)
M["floor"] = wood("Дъб рибена кост", "#D6B48C", "#A88158", axis="Y", rough=0.45, per_plank=True)
M["oak"] = wood("Масивен дъб", "#C9A27A", "#9A7350", axis="X", rough=0.4)
M["oak_flute"] = wood("Дъб рифелован", "#C7A07A", "#96704E", axis="X", rough=0.5)
M["subfloor"] = simple("Фуга", "#3A2C21", 0.9)
M["subway"] = tiles("Метро плочки", 0.15, 0.075, "#F4F2EC", "#ECE9E1", "#D9D4CB", 0.08, 0.5, 0.0022, 0.02, 0.25)
M["zellige"] = tiles("Зелиж шалвия", 0.10, 0.10, "#97AB97", "#86A087", "#E4E0D6", 0.06, 0.0, 0.0025, 0.22, 0.10, 0.9, 70)
M["bathfloor"] = checker_tiles("Под баня шах", 0.20, "#E2B7A8", "#F1E9DE", "#D8CFC4")
M["wallpaper"] = image_mat("Тапет ботанически", os.path.join(TEX, "wallpaper.png"), (0.53, 0.53), 0.85)
M["bedding"] = image_mat("Спално бельо", os.path.join(TEX, "bedding.png"), (0.6, 0.6), 0.9, 0.6)
M["rug"] = image_mat("Килим винтидж", os.path.join(TEX, "rug.png"), (1, 1), 0.95, 0.5,
                     os.path.join(TEX, "rug_bump.png"), 0.6, scale=(1, 1, 1))
M["chrome"] = simple("Хром", "#D5D7D9", 0.18, 1.0)
M["steel"] = simple("Неръждаема стомана", "#B9BCBE", 0.32, 1.0, Anisotropic=0.6)
M["brass"] = simple("Месинг четкан", "#C49A5C", 0.28, 1.0, Anisotropic=0.4)
M["black"] = simple("Черен емайл", "#151716", 0.28, 0.0, Coat_Weight=0.6)
M["black_matte"] = simple("Черен мат", "#1B1C1B", 0.55, 0.3)
M["black_glass"] = simple("Черно стъкло", "#060707", 0.05, 0.0, Coat_Weight=1.0)
M["glass"] = window_glass("Стъкло прозорци")
M["glass_obj"] = simple("Стъкло", "#F2F6F5", 0.02, 0.0, Transmission_Weight=1.0, IOR=1.5)
M["mirror"] = simple("Огледало", "#EDEFEF", 0.02, 1.0)
M["ceramic"] = simple("Керамика бяла", "#F6F5F1", 0.12, 0.0, Coat_Weight=0.8)
M["ceramic_matte"] = simple("Керамика мат", "#EFECE6", 0.35)
M["pvc"] = simple("PVC дограма", "#F2F2EF", 0.3)
M["sill"] = simple("Подпрозоречен плот", "#ECEAE5", 0.18, Coat_Weight=0.5)
M["linen_beige"] = fabric("Лен бежов", "#D3C8B8")
M["linen_pink"] = fabric("Лен розов", "#D7A39A")
M["linen_cream"] = fabric("Лен кремав", "#ECE5D8")
M["linen_sage"] = fabric("Лен шалвия", "#9DAE9B")
M["curtain_pink"] = fabric("Завеси пудра", "#DDB2A9", 0.9, 0.7, 200, 0.15)
M["boucle"] = fabric("Букле", "#ECE6DA", 0.95, 0.4, 420, 0.5, boucle=True)
M["sheet"] = fabric("Чаршаф", "#F2F0EB", 0.9, 0.3, 500, 0.1)
M["towel"] = fabric("Хавлия", "#D9A9A0", 0.95, 0.6, 600, 0.6, boucle=True)
M["sheer"] = sheer("Перде")
M["cane"] = fabric("Ратан плетка", "#C8A97E", 0.7, 0.0, 90, 0.5)
M["terracotta"] = simple("Теракота", "#B9735A", 0.75)
M["soil"] = simple("Почва", "#3B2E25", 0.95)
M["bark"] = simple("Кора", "#6E6152", 0.85)
M["olive_leaf"] = leafmat("Маслинови листа", "#7F8F70", "#A3AE92")
M["green_leaf"] = leafmat("Листа", "#4E6B3E", "#6E8A4F")
M["flower_pink"] = simple("Цвят розов", "#E7A6A5", 0.6, Subsurface_Weight=0.3)
M["tv"] = tv_screen("ТВ екран")
M["led"] = emissive("LED лента", "#FFE3C0", 12)
M["bulb"] = emissive("Крушка", "#FFD9A8", 40)
M["shade_on"] = emissive("Абажур", "#FFDDB2", 2.5, "#F1E6D6", translucent=True)
M["shade_lamp"] = emissive("Абажур лампи", "#FFDDB2", 2.5, "#F1E6D6", translucent=True)
M["cab_glow"] = emissive("Шкаф подсветка", "#FFE6C8", 6)
M["lampcream"] = simple("Керамика крем", "#EEE5D6", 0.25, Coat_Weight=0.6)
M["plaster_ext"] = simple("Фасада", "#D9D2C6", 0.9)
M["ext_glass"] = simple("Стъкла фасада", "#3B4650", 0.08, 0.6)
M["ground"] = simple("Тротоар", "#8F8A82", 0.9)
M["grass"] = simple("Трева", "#5E7444", 0.95)
M["book"] = [simple(f"Книга {i}", c, 0.7) for i, c in enumerate(
    ["#C4877A", "#8C9C89", "#E5DACB", "#6E7F72", "#D6B8A6", "#3E4944", "#B7A38A", "#F0ECE4", "#A35F52"])]
M["paper"] = simple("Хартия", "#F3EFE6", 0.9)
M["art1"] = image_mat("Картина 1", os.path.join(TEX, "wallpaper.png"), (0.9, 0.9), 0.9)
M["dark_wood"] = wood("Орех", "#7A5A42", "#4E3828", axis="X", rough=0.45)
M["washer"] = simple("Пералня", "#F4F4F2", 0.25)


# ---------------------------------------------------------------- floor: real herringbone planks
def herringbone(x0, x1, y0, y1, w=0.09, ratio=6, gap=0.0016, th=0.012):
    bm = bmesh.new()
    rnd_layer = bm.faces.layers.float.new("rnd")
    uv_layer = bm.loops.layers.uv.new("UVMap")
    s = w / math.sqrt(2)

    def W(a, b):  # unit plank coords -> world (chain axis along +y)
        return Vector(((a - b) * s + (x0 + x1) / 2, (a + b) * s + y0, 0))

    kmin = int(-2 * ratio)
    kmax = int((y1 - y0) / (2 * s)) + 2 * ratio
    mmax = int((x1 - x0) / (2 * ratio * s)) + 3
    g = gap / w
    for m in range(-mmax, mmax + 1):
        for k in range(kmin, kmax):
            for t in (0, 1):
                a0, b0 = k + ratio * m, k - ratio * m
                if t == 0:
                    ra, rb = (a0 + g, a0 + ratio - g), (b0 + g, b0 + 1 - g)
                else:
                    ra, rb = (a0 + g, a0 + 1 - g), (b0 + 1 + g, b0 + 1 + ratio - g)
                corners = [W(ra[0], rb[0]), W(ra[1], rb[0]), W(ra[1], rb[1]), W(ra[0], rb[1])]
                c = sum(corners, Vector()) / 4
                if not (x0 - 0.3 < c.x < x1 + 0.3 and y0 - 0.3 < c.y < y1 + 0.3):
                    continue
                top = [bm.verts.new((p.x, p.y, 0.0)) for p in corners]
                bot = [bm.verts.new((p.x, p.y, -th)) for p in corners]
                f = bm.faces.new(top)
                sides = []
                for i in range(4):
                    j = (i + 1) % 4
                    sides.append(bm.faces.new((bot[i], bot[j], top[j], top[i])))
                rv = R.random()
                ou, ov = R.uniform(0, 30), R.uniform(0, 30)
                along_a = t == 0
                for ff in [f] + sides:
                    ff[rnd_layer] = rv
                    for lo in ff.loops:
                        p = lo.vert.co
                        # local plank coords: u along length, v across
                        rel = p - corners[0]
                        ea = (W(1, 0) - W(0, 0)).normalized()
                        eb = (W(0, 1) - W(0, 0)).normalized()
                        ua, ub = rel.dot(ea), rel.dot(eb)
                        u, v = (ua, ub) if along_a else (ub, ua)
                        lo[uv_layer].uv = (u + ou, v + ov)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = mesh_obj("Паркет рибена кост", bm, M["floor"])
    bv = ob.modifiers.new("bevel", "BEVEL")
    bv.width = 0.0012
    bv.segments = 1
    bv.limit_method = "ANGLE"
    return ob


herringbone(-0.12, 4.02, -0.12, 8.22)
box("Подложка", -0.3, 4.2, -0.3, 8.4, -0.06, -0.011, M["subfloor"])

# ---------------------------------------------------------------- shell
WALLS = []


def wall(x0, x1, y0, y1, z0=0.0, z1=H, mat=None):
    WALLS.append(box("Стена", x0, x1, y0, y1, z0, z1, mat or M["wall"], jit=False))


wall(-0.25, 0, -0.25, 8.35)  # west
for a, b in ((-0.25, 0.30), (3.60, 4.15)):
    wall(a, b, 8.10, 8.35)
wall(0.30, 3.60, 8.10, 8.35, 0, 0.85)
wall(0.30, 3.60, 8.10, 8.35, 2.35, H)
wall(3.90, 4.15, -0.25, 4.75)
wall(3.90, 4.15, 4.75, 5.40, 0, 0.95)
wall(3.90, 4.15, 4.75, 5.40, 2.25, H)
wall(3.90, 4.15, 5.40, 5.60)
wall(3.90, 4.15, 5.60, 6.25, 0, 0.95)
wall(3.90, 4.15, 5.60, 6.25, 2.25, H)
wall(3.90, 4.15, 6.25, 8.35)
wall(3.60, 3.90, 6.90, 7.20)  # pilaster
wall(-0.25, 2.69, -0.25, 0)
wall(3.59, 4.15, -0.25, 0)
wall(2.69, 3.59, -0.25, 0, 2.05, H)
CEILING = box("Таван", -0.25, 4.15, -0.25, 8.35, H, H + 0.2, M["ceil"], jit=False)
# partitions (12 cm, axes per plan)
wall(0, 2.16, 1.84, 1.96)
wall(2.04, 2.16, 0, 0.15)
wall(2.04, 2.16, 0.78, 1.16)
wall(2.04, 2.16, 0.15, 0.78, 2.02, H)
wall(1.24, 2.16, 1.04, 1.16)
wall(1.24, 1.36, 1.16, 1.84)
wall(2.04, 2.16, 1.16, 1.84, 2.22, H)
box("Комин (обшит)", 0, 0.70, 1.96, 2.26, 0, H, M["pink"], jit=False)

# wall finishes
box("Боя кухня", 0, 0.004, 1.96, 4.75, 0, H, M["pink"])
box("Боя кухня ъгъл", 0.70, 2.16, 1.96, 1.964, 0, H, M["pink"])
box("Ламперия", 3.892, 3.90, 4.10, 6.85, 0, 0.92, M["bead"], wuv=True)
box("Профил ламперия", 3.872, 3.90, 4.10, 6.85, 0.92, 0.95, M["sage_paint"], bevel=0.004)
for a, b, z0 in ((4.10, 4.75, 0.95), (5.40, 5.60, 0.95), (6.25, 6.85, 0.95), (4.75, 5.40, 2.25), (5.60, 6.25, 2.25)):
    box("Тапет", 3.895, 3.90, a, b, z0, H, M["wallpaper"], wuv=True)
# skirting
for args in ((0, 0.012, 6.25, 8.10), (0, 3.60, 8.088, 8.10), (3.888, 3.90, 6.85, 6.90), (3.888, 3.90, 7.20, 8.10),
             (3.588, 3.60, 6.90, 7.20), (3.60, 3.90, 6.888, 6.90), (3.60, 3.90, 7.20, 7.212), (3.888, 3.90, 2.80, 3.20),
             (2.16, 2.69, 0, 0.012), (3.59, 3.90, 0, 0.012), (0.70, 2.16, 1.964, 1.976), (2.16, 2.172, 0.78, 1.16),
             (2.16, 2.172, 0, 0.15)):
    box("Перваз", *args, 0, 0.09, M["white_satin"], bevel=0.002)
# bathroom floor & tiles
box("Под баня", 0, 2.04, 0, 1.84, -0.02, 0.006, M["bathfloor"], wuv=True)
box("Праг", 2.04, 2.16, 0.15, 0.78, -0.01, 0.006, M["sill"])
for args in ((0, 0.008, 0, 1.04, 0, 1.20), (0, 0.008, 1.04, 1.84, 0, 2.25), (0, 2.04, 0, 0.008, 0, 1.20),
             (0, 1.24, 1.832, 1.84, 0, 2.25), (1.232, 1.24, 1.04, 1.84, 0, 2.25), (1.24, 2.04, 1.032, 1.04, 0, 1.20),
             (2.032, 2.04, 0, 0.15, 0, 1.20), (2.032, 2.04, 0.78, 1.04, 0, 1.20)):
    box("Зелиж", *args, M["zellige"], wuv=True)
M["bath_paint"] = paint("Баня пудра", "#E5C9BF", 0.6, 0.02)
for args in ((0, 0.008, 0, 1.04, 1.20, H), (0, 0.008, 1.04, 1.84, 2.25, H), (0, 2.04, 0, 0.008, 1.20, H),
             (0, 1.24, 1.832, 1.84, 2.25, H), (1.232, 1.24, 1.04, 1.84, 2.25, H), (1.24, 2.04, 1.032, 1.04, 1.20, H),
             (2.032, 2.04, 0, 0.15, 1.20, H), (2.032, 2.04, 0.78, 1.04, 1.20, H), (2.032, 2.04, 0.15, 0.78, 2.02, H)):
    box("Баня боя", *args, M["bath_paint"])


# ---------------------------------------------------------------- windows
def window(axis, a0, a1, z0, z1, mid, sashes, inner):
    """axis 'N': opening along x at wall y=mid; 'E': along y at wall x=mid. inner: room-side wall face coord."""
    def B(name, aa, ab, da, db, za, zb, mat, bevel=0.0):
        if axis == "N":
            return box(name, aa, ab, da, db, za, zb, mat, bevel=bevel)
        return box(name, da, db, aa, ab, za, zb, mat, bevel=bevel)

    f, d = 0.065, 0.035
    sill_a0, sill_a1, sill_z0 = a0, a1, z0
    a0, a1, z0, z1 = a0 + 0.003, a1 - 0.003, z0 + 0.003, z1 - 0.003
    B("Каса", a0, a1, mid - d, mid + d, z0, z0 + f, M["pvc"], 0.003)
    B("Каса", a0, a1, mid - d, mid + d, z1 - f, z1, M["pvc"], 0.003)
    B("Каса", a0, a0 + f, mid - d, mid + d, z0, z1, M["pvc"], 0.003)
    B("Каса", a1 - f, a1, mid - d, mid + d, z0, z1, M["pvc"], 0.003)
    sw = (a1 - a0 - 2 * f) / sashes
    for i in range(sashes):
        s0 = a0 + f + i * sw
        s1 = s0 + sw
        sf = 0.055
        B("Крило", s0, s1, mid - d - 0.012, mid - d + 0.02, z0 + f, z0 + f + sf, M["pvc"], 0.004)
        B("Крило", s0, s1, mid - d - 0.012, mid - d + 0.02, z1 - f - sf, z1 - f, M["pvc"], 0.004)
        B("Крило", s0, s0 + sf, mid - d - 0.012, mid - d + 0.02, z0 + f, z1 - f, M["pvc"], 0.004)
        B("Крило", s1 - sf, s1, mid - d - 0.012, mid - d + 0.02, z0 + f, z1 - f, M["pvc"], 0.004)
        B("Стъкло", s0 + sf, s1 - sf, mid - 0.003, mid + 0.003, z0 + f + sf, z1 - f - sf, M["glass"])
        hx = s1 - sf / 2 if i % 2 == 0 else s0 + sf / 2
        hz = (z0 + z1) / 2
        side = -1 if axis == "N" else -1
        B("Дръжка", hx - 0.012, hx + 0.012, mid - d - 0.05, mid - d - 0.012, hz - 0.03, hz + 0.03, M["chrome"], 0.004)
        B("Дръжка", hx - 0.009, hx + 0.009, mid - d - 0.065, mid - d - 0.045, hz - 0.12, hz + 0.02, M["chrome"], 0.004)
    # interior sill
    if axis == "N":
        box("Подпрозоречен плот", sill_a0 - 0.03, sill_a1 + 0.03, inner - 0.04, mid - d - 0.002, sill_z0 - 0.022, sill_z0 + 0.008, M["sill"], bevel=0.004)
    else:
        box("Подпрозоречен плот", inner - 0.04, mid - d - 0.002, sill_a0 - 0.03, sill_a1 + 0.03, sill_z0 - 0.022, sill_z0 + 0.008, M["sill"], bevel=0.004)


window("N", 0.30, 3.60, 0.85, 2.35, 8.22, 5, 8.10)
window("E", 4.75, 5.40, 0.95, 2.25, 4.02, 1, 3.90)
window("E", 5.60, 6.25, 0.95, 2.25, 4.02, 1, 3.90)


# ---------------------------------------------------------------- furniture primitives
def shaker(par, x0, x1, z0, z1, yb, mat=None, glass=False, handle=None, hpos=None, frame=None, mid=None, t=0.02):
    """Shaker door in parent-local coords: front faces -y, back at y=yb."""
    mat = mat or M["cab"]
    w, h = x1 - x0, z1 - z0
    f = frame or max(0.035, min(0.07, min(w, h) * 0.16))
    yf = yb - t
    box("Рамка", x0, x0 + f, yf, yb, z0, z1, mat, par, bevel=0.002)
    box("Рамка", x1 - f, x1, yf, yb, z0, z1, mat, par, bevel=0.002)
    box("Рамка", x0 + f, x1 - f, yf, yb, z1 - f, z1, mat, par, bevel=0.002)
    box("Рамка", x0 + f, x1 - f, yf, yb, z0, z0 + f, mat, par, bevel=0.002)
    panels = [(z0 + f, z1 - f)]
    if mid:
        box("Рамка", x0 + f, x1 - f, yf, yb, mid - f / 2, mid + f / 2, mat, par, bevel=0.002)
        panels = [(z0 + f, mid - f / 2), (mid + f / 2, z1 - f)]
    for pa, pb in panels:
        if glass:
            box("Стъкло врата", x0 + f - 0.004, x1 - f + 0.004, yb - t / 2 - 0.002, yb - t / 2 + 0.002, pa - 0.004, pb + 0.004,
                M["glass"], par)
        else:
            box("Пано", x0 + f - 0.003, x1 - f + 0.003, yb - 0.011, yb, pa - 0.003, pb + 0.003, mat, par, bevel=0.003)
    if handle:
        hx, hz = hpos if hpos else ((x0 + x1) / 2, z1 - f / 2)
        y = yf
        hm = M["chrome"] if handle in ("v", "h") else M["brass"]
        if handle == "v":
            L = 0.16 if h > 0.3 else 0.10
            cyl("Дръжка", 0.0065, L, (hx, y - 0.032, hz), hm, par)
            for dz in (-L / 2 + 0.02, L / 2 - 0.02):
                cyl("Дръжка", 0.0045, 0.032, (hx, y - 0.016, hz + dz), hm, par, axis="Y")
        elif handle == "h":
            L = min(0.16, w * 0.5)
            cyl("Дръжка", 0.0065, L, (hx, y - 0.032, hz), hm, par, axis="X")
            for dx in (-L / 2 + 0.02, L / 2 - 0.02):
                cyl("Дръжка", 0.0045, 0.032, (hx + dx, y - 0.016, hz), hm, par, axis="Y")
        elif handle == "knob":
            cyl("Копче", 0.006, 0.02, (hx, y - 0.01, hz), hm, par, axis="Y")
            sphere("Копче", 0.016, (hx, y - 0.027, hz), hm, par, scale=(1, 0.7, 1))
        elif handle == "woodknob":
            cyl("Копче", 0.014, 0.022, (hx, y - 0.011, hz), M["oak"], par, axis="Y", r2=0.018)
            sphere("Копче", 0.02, (hx, y - 0.028, hz), M["oak"], par, scale=(1, 0.55, 1))


def turned_leg(name, h, loc, mat, par=None, scale=1.0):
    prof = [(0.0, 0), (0.016, 0), (0.017, 0.02), (0.02, 0.06), (0.024, 0.10), (0.02, 0.13), (0.017, 0.30),
            (0.021, 0.42), (0.026, 0.46), (0.021, 0.50), (0.018, 0.53), (0.026, 0.56), (0.03, 0.58), (0.03, 0.62),
            (0.03, 1.0), (0.0, 1.0)]
    prof = [(r * scale, z * h) for r, z in prof]
    return lathe(name, prof, loc, mat, par, segs=24)


def books(par, x0, y, z, length, along="X", depth=0.2, seed=1, lean_end=True):
    r = random.Random(seed)
    pos = x0
    while pos < x0 + length - 0.03:
        t = r.uniform(0.018, 0.04)
        hgt = r.uniform(0.17, 0.26)
        mat = r.choice(M["book"])
        if along == "X":
            box("Книга", pos, pos + t, y - depth, y, z, z + hgt, mat, par, bevel=0.002)
        else:
            box("Книга", y - depth, y, pos, pos + t, z, z + hgt, mat, par, bevel=0.002)
        pos += t + 0.002


def plant_leaves(par, center, radius, n, mat, leaf=(0.06, 0.018), seed=3, zstretch=1.0, droop=0.0):
    r = random.Random(seed)
    bm = bmesh.new()
    lay = bm.faces.layers.float.new("rnd")
    for _ in range(n):
        while True:
            p = Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1)))
            if p.length < 1:
                break
        p = Vector((p.x * radius, p.y * radius, p.z * radius * zstretch)) + Vector(center)
        rot = Euler((r.uniform(-1.2, 1.2) + droop, r.uniform(-1.2, 1.2), r.uniform(0, 6.28))).to_matrix()
        L, W = leaf[0] * r.uniform(0.7, 1.2), leaf[1] * r.uniform(0.7, 1.2)
        fold, bend = W * 0.18, L * 0.12
        n_ = 5
        mid = [Vector((L * i / n_, 0, -bend * (i / n_) ** 2)) for i in range(n_ + 1)]
        sides = []
        for s_ in (1, -1):
            row = []
            for i in range(1, n_):
                tt = i / n_
                wdt = W / 2 * math.sin(math.pi * tt) ** 0.8
                row.append(Vector((L * tt, s_ * wdt, fold - bend * tt * tt)))
            sides.append(row)
        rv = r.random()
        vm = [bm.verts.new(p + rot @ q) for q in mid]
        for row in sides:
            vr = [bm.verts.new(p + rot @ q) for q in row]
            for i in range(n_):
                quad = [vm[i], vm[i + 1]]
                tri = []
                if i == 0:
                    tri = [vm[0], vm[1], vr[0]]
                elif i == n_ - 1:
                    tri = [vm[n_ - 1], vm[n_], vr[n_ - 2]]
                if tri:
                    f = bm.faces.new(tri)
                else:
                    f = bm.faces.new((vm[i], vm[i + 1], vr[i], vr[i - 1]))
                f[lay] = rv
                f.smooth = True
    return mesh_obj("Листа", bm, mat, par)


def flowers(par, base, n, seed=5, radius=0.08, height=0.25):
    r = random.Random(seed)
    for i in range(n):
        top = (base[0] + r.uniform(-radius, radius), base[1] + r.uniform(-radius, radius), base[2] + height * r.uniform(0.7, 1.1))
        poly_tube("Стрък", [base, top], 0.002, M["green_leaf"], par)
        sphere("Цвят", 0.022, top, M["flower_pink"], par, scale=(1, 1, 0.8), segs=12, rings=8)


# ---------------------------------------------------------------- kitchen: L around the chimney on the bathroom's back wall
# Run A: against the bathroom partition (back y=1.96), x 0.70..2.16 — sink + dishwasher (plumbing from the bathroom).
# Run B: against the west wall (back x=0), y 2.26..4.56 — hob under a hood vented into the chimney, drawers, fridge, pantry.


def wall_cab(P, x0, x1, glass=True, hside=1):
    z0, z1, d = 1.45, 2.35, -0.35
    t = 0.018
    box("Горен шкаф", x0, x0 + t, d, 0, z0, z1, M["cab"], P)
    box("Горен шкаф", x1 - t, x1, d, 0, z0, z1, M["cab"], P)
    box("Горен шкаф", x0, x1, d, 0, z1 - t, z1, M["cab"], P)
    box("Горен шкаф", x0, x1, d, 0, z0, z0 + t, M["cab"], P)
    box("Горен шкаф гръб", x0, x1, -0.012, 0, z0, z1, M["cab_in"], P)
    if glass:
        box("Подсветка", x0 + 0.03, x1 - 0.03, -0.30, -0.29, z1 - t - 0.006, z1 - t, M["cab_glow"], P)
    for zs in (1.75, 2.05):
        box("Рафт", x0 + t, x1 - t, d + 0.01, -0.012, zs, zs + 0.016, M["cab_in"], P)
    shaker(P, x0 + 0.002, x1 - 0.002, z0 + 0.002, z1 - 0.002, d, glass=glass, handle="v",
           hpos=(x1 - 0.035 if hside > 0 else x0 + 0.035, z0 + 0.12))
    w = x1 - x0
    if w > 0.3:
        for i in range(4):
            cyl("Чиния", 0.105, 0.012, (x0 + w / 2, -0.16, z0 + t + 0.006 + i * 0.014), M["ceramic"], P, r2=0.11)
    for i in range(max(1, int(w / 0.08))):
        cyl("Чаша", 0.032, 0.11, (x0 + 0.05 + i * 0.08, -0.17, 1.766 + 0.055), M["glass_obj"], P, r2=0.036)
    for i in range(max(1, int(w / 0.13))):
        lathe("Купа", [(0.0, 0), (0.04, 0), (0.06, 0.02), (0.065, 0.05), (0.06, 0.05), (0.035, 0.008), (0.0, 0.008)],
              (x0 + 0.075 + i * 0.13, -0.17, 2.066), M["ceramic"], P, segs=32)


def worktop(P, x0, x1, y0=-0.62, y1=0.0):
    box("Плот дъб", x0, x1, y0, y1, 0.88, 0.92, M["oak"], P, bevel=0.003, wuv=True)


# Run A
KA = empty("Кухня рамо А", 2.16, 1.96, FACE["N"])
box("Цокъл", 0, 1.46, -0.54, 0, 0, 0.10, M["cab"], KA)
box("Корпус", 0, 0.21, -0.58, 0, 0.10, 0.88, M["cab"], KA)
box("Корпус мивка", 0.21, 1.01, -0.58, 0, 0.10, 0.69, M["cab"], KA)
box("Корпус", 1.01, 1.46, -0.58, 0, 0.10, 0.88, M["cab"], KA)
box("Страница", -0.02, 0, -0.62, 0, 0, 0.88, M["cab"], KA, bevel=0.002)
shaker(KA, 0.003, 0.207, 0.103, 0.877, -0.58, handle="v", hpos=(0.105, 0.80))
shaker(KA, 0.213, 0.607, 0.103, 0.877, -0.58, handle="v", hpos=(0.565, 0.79))
shaker(KA, 0.613, 1.007, 0.103, 0.877, -0.58, handle="v", hpos=(0.655, 0.79))
shaker(KA, 1.013, 1.457, 0.103, 0.877, -0.58, handle="h", hpos=(1.235, 0.84))
sx = 0.61
for a, b, c, d in ((-0.02, sx - 0.24, -0.62, 0), (sx + 0.24, 1.46, -0.62, 0), (sx - 0.24, sx + 0.24, -0.62, -0.50),
                   (sx - 0.24, sx + 0.24, -0.10, 0)):
    worktop(KA, a, b, c, d)
box("Мивка дъно", sx - 0.24, sx + 0.24, -0.50, -0.10, 0.70, 0.72, M["ceramic"], KA)
for a, b, c, d in ((sx - 0.24, sx - 0.22, -0.50, -0.10), (sx + 0.22, sx + 0.24, -0.50, -0.10),
                   (sx - 0.24, sx + 0.24, -0.50, -0.48), (sx - 0.24, sx + 0.24, -0.12, -0.10)):
    box("Мивка стена", a, b, c, d, 0.70, 0.92, M["ceramic"], KA)
for a, b, c, d in ((sx - 0.26, sx - 0.22, -0.52, -0.08), (sx + 0.22, sx + 0.26, -0.52, -0.08),
                   (sx - 0.22, sx + 0.22, -0.52, -0.48), (sx - 0.22, sx + 0.22, -0.12, -0.08)):
    box("Мивка борд", a, b, c, d, 0.92, 0.935, M["ceramic"], KA, bevel=0.006)
cyl("Сифон", 0.035, 0.004, (sx, -0.30, 0.722), M["steel"], KA)
cyl("Батерия основа", 0.026, 0.06, (sx, -0.045, 0.965), M["chrome"], KA)
tube("Батерия", [(sx, -0.045, 0.99), (sx, -0.045, 1.22), (sx, -0.14, 1.30), (sx, -0.25, 1.24), (sx, -0.26, 1.17)], 0.011, M["chrome"], KA)
tube("Лост", [(sx + 0.02, -0.045, 1.03), (sx + 0.09, -0.06, 1.06)], 0.006, M["chrome"], KA)
box("Метро плочки", -0.02, 1.46, -0.009, 0, 0.92, 1.45, M["subway"], KA, wuv=True)
for z in (1.62, 1.98):
    box("Отворен рафт", -0.02, 0.21, -0.24, 0, z, z + 0.03, M["oak"], KA, bevel=0.002, wuv=True)
for i, (hgt, r) in enumerate(((0.16, 0.045), (0.12, 0.045))):
    cyl("Буркан", r, hgt, (0.05 + i * 0.10, -0.12, 1.65 + hgt / 2), M["glass_obj"], KA)
    cyl("Съдържание", r * 0.9, hgt * 0.6, (0.05 + i * 0.10, -0.12, 1.652 + hgt * 0.3),
        simple(f"Храна{i}", ["#E8D9B5", "#B07443"][i], 0.8), KA)
    cyl("Капак", r * 1.02, 0.02, (0.05 + i * 0.10, -0.12, 1.65 + hgt + 0.01), M["oak"], KA)
lathe("Кана", [(0, 0), (0.06, 0), (0.07, 0.08), (0.05, 0.2), (0.03, 0.22), (0, 0.22)], (0.10, -0.12, 2.01), M["lampcream"], KA)
for a, b in ((0.21, 0.61), (0.61, 1.01), (1.01, 1.46)):
    wall_cab(KA, a, b, hside=1 if b < 0.9 else -1)
box("LED лента", 0.23, 1.44, -0.33, -0.31, 1.441, 1.449, M["led"], KA)
box("Дъска", 1.05, 1.35, -0.035, -0.015, 0.92, 1.30, M["oak"], KA, bevel=0.01, wuv=True)
box("Дъска", 1.18, 1.42, -0.06, -0.04, 0.92, 1.22, M["dark_wood"], KA, bevel=0.01, wuv=True)
lathe("Купа плодове", [(0, 0), (0.07, 0), (0.13, 0.06), (0.135, 0.07), (0.12, 0.07), (0, 0.015)], (0.13, -0.33, 0.92), M["lampcream"], KA)
for i in range(5):
    sphere("Плод", 0.038, (0.13 + R.uniform(-0.05, 0.05), -0.33 + R.uniform(-0.05, 0.05), 0.97 + i * 0.008),
           simple(f"Плод{i}", R.choice(["#D9A441", "#C9573E", "#E8C14E"]), 0.4), KA)
lathe("Бутилка сапун", [(0, 0), (0.03, 0), (0.03, 0.14), (0.012, 0.17), (0, 0.17)], (0.92, -0.06, 0.92), M["lampcream"], KA)

# corner between the runs, in front of the chimney
box("Ъгъл корпус", 0.60, 0.70, 2.26, 2.56, 0.10, 0.88, M["cab"])
box("Ъгъл цокъл", 0.60, 0.70, 2.26, 2.52, 0, 0.10, M["cab"])
box("Ъгъл плот", 0.60, 0.70, 2.26, 2.58, 0.88, 0.92, M["oak"], bevel=0.003, wuv=True)

# Run B
KB = empty("Кухня рамо Б", 0.0, 2.26, FACE["E"])
box("Цокъл", 0, 2.30, -0.54, 0, 0, 0.10, M["cab"], KB)
box("Корпус", 0, 1.30, -0.58, 0, 0.10, 0.88, M["cab"], KB)
shaker(KB, 0.003, 0.297, 0.103, 0.877, -0.58, handle="v", hpos=(0.15, 0.80))
shaker(KB, 0.303, 0.897, 0.103, 0.297, -0.58, handle="h", hpos=(0.60, 0.255))
box("Фурна рамка", 0.306, 0.894, -0.60, -0.58, 0.30, 0.878, M["steel"], KB, bevel=0.002)
box("Фурна стъкло", 0.34, 0.86, -0.603, -0.598, 0.34, 0.74, M["black_glass"], KB, bevel=0.002)
box("Фурна панел", 0.32, 0.88, -0.603, -0.598, 0.79, 0.865, M["black_glass"], KB)
cyl("Фурна дръжка", 0.008, 0.46, (0.60, -0.635, 0.765), M["steel"], KB, axis="X")
for dx in (-0.2, 0.2):
    cyl("Стойка", 0.005, 0.035, (0.60 + dx, -0.617, 0.765), M["steel"], KB, axis="Y")
for dx in (-0.18, -0.12, 0.12, 0.18):
    cyl("Копче фурна", 0.012, 0.012, (0.60 + dx, -0.606, 0.828), M["steel"], KB, axis="Y")
for z0, z1 in ((0.103, 0.357), (0.363, 0.617), (0.623, 0.877)):
    shaker(KB, 0.903, 1.297, z0, z1, -0.58, handle="h", hpos=(1.10, z1 - 0.05))
worktop(KB, 0.0, 1.31)
box("Метро плочки", 0.0, 1.30, -0.009, 0, 0.92, 1.45, M["subway"], KB, wuv=True)
box("Метро плочки зад аспиратора", 0.30, 0.90, -0.009, 0, 1.45, 1.56, M["subway"], KB, wuv=True)
box("Плоча", 0.33, 0.87, -0.56, -0.07, 0.92, 0.927, M["black_glass"], KB, bevel=0.003)
box("Плоча управление", 0.50, 0.70, -0.545, -0.53, 0.927, 0.9272, M["steel"], KB)
box("Аспиратор лента", 0.30, 0.90, -0.50, 0, 1.56, 1.62, M["steel"], KB, bevel=0.002)
bm = bmesh.new()
for x, y, z in ((0.30, -0.50, 1.62), (0.90, -0.50, 1.62), (0.90, 0, 1.62), (0.30, 0, 1.62),
                (0.46, -0.30, 1.86), (0.74, -0.30, 1.86), (0.74, 0, 1.86), (0.46, 0, 1.86)):
    bm.verts.new((x, y, z))
bmesh.ops.convex_hull(bm, input=bm.verts)
mesh_obj("Аспиратор", bm, M["hood"], KB)
box("Аспиратор комин", 0.46, 0.74, -0.30, 0, 1.86, H, M["hood"], KB, bevel=0.002)
wall_cab(KB, 0.0, 0.30, hside=1)
wall_cab(KB, 0.90, 1.30, hside=-1)
box("LED лента", 0.02, 0.28, -0.33, -0.31, 1.441, 1.449, M["led"], KB)
box("LED лента", 0.92, 1.28, -0.33, -0.31, 1.441, 1.449, M["led"], KB)
# tall fridge column + pantry
box("Колона", 1.30, 2.30, -0.58, 0, 0.10, 2.35, M["cab"], KB)
box("Колона пълнеж", 1.30, 2.30, -0.60, 0, 2.35, H, M["cab"], KB)
box("Корниз", 1.30, 2.31, -0.615, 0, 2.38, 2.42, M["cab"], KB, bevel=0.006)
shaker(KB, 1.303, 1.897, 0.103, 0.905, -0.58, handle="v", hpos=(1.34, 0.80))
shaker(KB, 1.303, 1.897, 0.911, 2.347, -0.58, handle="v", hpos=(1.34, 1.05), mid=1.70)
shaker(KB, 1.903, 2.297, 0.103, 2.347, -0.58, handle="v", hpos=(1.94, 1.05), mid=1.25)
box("Страница", 2.30, 2.32, -0.62, 0, 0, 2.42, M["cab"], KB, bevel=0.002)
# counter decor
for i, (h, r) in enumerate(((0.22, 0.06), (0.18, 0.055), (0.14, 0.05))):
    lathe("Буркан", [(0, 0), (r, 0), (r, h), (r * 0.7, h + 0.01), (0, h + 0.01)], (1.00 + i * 0.12, -0.12, 0.92), M["lampcream"], KB)
lathe("Саксия", [(0, 0), (0.06, 0), (0.08, 0.12), (0.085, 0.12), (0, 0.12)], (0.12, -0.25, 0.92), M["terracotta"], KB)
plant_leaves(KB, (0.12, -0.25, 1.10), 0.11, 220, M["green_leaf"], (0.04, 0.028), 7, 0.6)
flowers(KB, (0.12, -0.25, 1.04), 14, 8, 0.09, 0.16)
lathe("Чайник", [(0, 0), (0.09, 0), (0.1, 0.06), (0.09, 0.15), (0.05, 0.19), (0.02, 0.2), (0, 0.2)], (1.15, -0.40, 0.92),
      simple("Чайник", "#E9E3D7", 0.2, Coat_Weight=0.8), KB)
# ceiling track lights: one along each run
box("Шина", 0.92, 0.96, 2.60, 3.65, H - 0.03, H, M["black_matte"])
box("Шина", 0.92, 2.05, 2.60, 2.64, H - 0.03, H, M["black_matte"])
SPOTS = []
for px_, py_, tx, ty in ((0.94, 2.95, 0.25, 2.95), (0.94, 3.45, 0.25, 3.45), (1.25, 2.62, 1.25, 2.20), (1.85, 2.62, 1.85, 2.20)):
    SPOTS.append(((px_, py_, H - 0.16), (tx, ty, 0.92)))
    d = Vector((tx, ty, 0.92)) - Vector((px_, py_, H - 0.08))
    sp = cyl("Спот", 0.032, 0.11, (px_, py_, H - 0.12), M["black_matte"])
    sp.rotation_euler = Vector((0, 0, -1)).rotation_difference(d).to_euler()

# ---------------------------------------------------------------- TV wall (west, opposite the inner windows, py 4.75..6.25)
TVY = 5.50
box("Рифелован панел основа", 0, 0.012, 4.75, 6.25, 0, H, M["oak_flute"], wuv=True)
fl = cyl("Рифел", 0.015, H, (0.012, 4.765, H / 2), M["oak_flute"], segs=16, wuv=True)
arr = fl.modifiers.new("arr", "ARRAY")
arr.use_relative_offset = False
arr.use_constant_offset = True
arr.constant_offset_displace = (0, 0.03, 0)
arr.count = 50
box("Конзола", 0.012, 0.40, 4.85, 6.15, 0.30, 0.66, M["cab"], bevel=0.002)
box("Конзола плот", 0.012, 0.415, 4.84, 6.16, 0.66, 0.685, M["oak"], bevel=0.003, wuv=True)
TVC = empty("Конзола фронт", 0.40, TVY, FACE["E"])
for a, b in ((-0.647, -0.219), (-0.213, 0.213), (0.219, 0.647)):
    shaker(TVC, a, b, 0.303, 0.657, 0.0, handle="knob", hpos=((a + b) / 2, 0.48))
box("ТВ рамка", 0.03, 0.06, TVY - 0.615, TVY + 0.615, 0.95, 1.66, M["black_matte"], bevel=0.004)
box("ТВ екран", 0.06, 0.0605, TVY - 0.608, TVY + 0.608, 0.957, 1.653, M["tv"], wuv=True)
vase = lathe("Ваза", [(0, 0), (0.07, 0), (0.1, 0.12), (0.09, 0.24), (0.045, 0.32), (0.05, 0.36), (0, 0.36)],
             (0.22, 5.03, 0.685), M["lampcream"])
r2 = random.Random(4)
for i in range(9):
    a = r2.uniform(0, 6.28)
    top = (0.22 + 0.25 * math.cos(a) * r2.uniform(0.3, 1), 5.03 + 0.25 * math.sin(a) * r2.uniform(0.3, 1), 1.40 + r2.uniform(-0.1, 0.25))
    poly_tube("Пампас", [(0.22, 5.03, 1.0), top], 0.003, M["cane"])
    sphere("Пампас", 0.05, top, M["linen_cream"], scale=(0.7, 0.7, 2.6), segs=12, rings=8)
books(None, 5.72, 0.38, 0.685, 0.22, along="Y", depth=0.24, seed=3)
box("Книги легнали", 0.10, 0.34, 5.98, 6.12, 0.685, 0.72, M["book"][1], bevel=0.002)
box("Книги легнали", 0.12, 0.32, 6.00, 6.10, 0.72, 0.745, M["book"][0], bevel=0.002)
sphere("Свещ", 0.04, (0.22, 6.05, 0.79), M["lampcream"], scale=(1, 1, 1.1))
# tall plant between TV wall and desk
lathe("Саксия голяма", [(0, 0), (0.15, 0), (0.18, 0.36), (0.19, 0.38), (0, 0.38)], (0.25, 6.55, 0), M["lampcream"])
for i, (dz, r) in enumerate(((0.75, 0.22), (1.05, 0.25), (1.35, 0.2))):
    plant_leaves(None, (0.25, 6.55, dz), r, 70, M["green_leaf"], (0.22, 0.12), 300 + i, 1.0, 0.5)
for i in range(7):
    a = i * 0.9
    poly_tube("Стъбло", [(0.25, 6.55, 0.36), (0.25 + 0.15 * math.cos(a), 6.55 + 0.15 * math.sin(a), 0.9 + 0.08 * i)], 0.006, M["green_leaf"])


# ---------------------------------------------------------------- dining & HEMNES daybed
rug = bpy.data.meshes.new("Килим")
bm = bmesh.new()
uvl = bm.loops.layers.uv.new("UVMap")
vs = [bm.verts.new(p) for p in ((1.40, 4.25, 0.009), (3.40, 4.25, 0.009), (3.40, 6.75, 0.009), (1.40, 6.75, 0.009))]
f = bm.faces.new(vs)
for lo, uvv in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
    lo[uvl].uv = uvv
mesh_obj("Килим", bm, M["rug"])
box("Килим кант", 1.40, 3.40, 4.25, 6.75, 0.0, 0.0085, M["linen_beige"])

T = empty("Маса", 2.51, 5.525, FACE["E"])
box("Плот маса", -0.775, 0.775, -0.435, 0.435, 0.715, 0.745, M["white_satin"], T, bevel=0.006, seg=3)
for a, b, c, d in ((-0.68, 0.68, -0.345, -0.325), (-0.68, 0.68, 0.325, 0.345), (-0.70, -0.68, -0.34, 0.34), (0.68, 0.70, -0.34, 0.34)):
    box("Царга", a, b, c, d, 0.62, 0.715, M["white_satin"], T, bevel=0.002)
for x in (-0.69, 0.69):
    for y in (-0.335, 0.335):
        turned_leg("Крак", 0.715, (x, y, 0), M["white_satin"], T)
# table decor (concept)
cyl("Подложка", 0.17, 0.008, (0.25, 0.0, 0.749), M["oak"], T, segs=64)
lathe("Чиния", [(0, 0), (0.08, 0), (0.12, 0.012), (0.13, 0.018), (0.12, 0.018), (0, 0.006)], (0.25, 0.0, 0.753), M["linen_pink"], T)
lathe("Ваза", [(0, 0), (0.035, 0), (0.05, 0.05), (0.025, 0.12), (0.03, 0.14), (0, 0.14)], (-0.15, 0.02, 0.745), M["ceramic"], T)
flowers(T, (-0.15, 0.02, 0.86), 7, 12, 0.07, 0.14)
plant_leaves(T, (-0.15, 0.02, 0.93), 0.06, 40, M["green_leaf"], (0.035, 0.015), 2)
for i, (x, y) in enumerate(((-0.35, -0.12), (-0.42, 0.15))):
    lathe("Купичка", [(0, 0), (0.035, 0), (0.06, 0.03), (0.062, 0.045), (0.056, 0.045), (0, 0.008)], (x, y, 0.745),
          simple(f"Купичка{i}", ["#B9CFC0", "#F1EADB"][i], 0.2, Coat_Weight=0.8), T)


def chair(px, py, face):
    C = empty("Стол", px, py, FACE[face])
    seat = box("Седалка", -0.23, 0.23, -0.47, -0.02, 0.40, 0.49, M["linen_beige"], C)
    soft(seat, 0.03, 3, 1)
    back = box("Облегалка", -0.22, 0.22, -0.08, 0.0, 0.47, 0.93, M["linen_beige"], C)
    back.rotation_euler = (math.radians(-6), 0, 0)
    soft(back, 0.035, 3, 1)
    for x in (-0.19, 0.19):
        cyl("Крак", 0.017, 0.40, (x, -0.42, 0.20), M["white_satin"], C, r2=0.022)
        cyl("Крак", 0.017, 0.42, (x, -0.05, 0.21), M["white_satin"], C, r2=0.022)
    return C


chair(1.60, 5.12, "E")
chair(1.60, 5.93, "E")
# pendant (concept black dome)
PX, PY = 2.51, 5.525
cyl("Розетка", 0.05, 0.02, (PX, PY, H - 0.01), M["black"])
cyl("Кабел", 0.003, H - 1.74, (PX, PY, (H + 1.74) / 2), M["black_matte"], segs=8)
shade = [(0.018, 0.0), (0.035, -0.004), (0.06, -0.04), (0.11, -0.09), (0.165, -0.165), (0.197, -0.235), (0.202, -0.245)]
lathe("Пендел", [(r, 1.745 + z) for r, z in shade], (PX, PY, 0), M["black"])
lathe("Пендел вътре", [(r * 0.985, 1.742 + z * 0.99) for r, z in shade], (PX, PY, 0), M["white_satin"])
sphere("Крушка пендел", 0.03, (PX, PY, 1.585), M["bulb"])

# HEMNES daybed 80x200 with 3 drawers, grey-green (user requirement)
HB = empty("HEMNES", 3.90, 5.50, FACE["W"])
Lh = 2.07
box("Гръб", -Lh / 2, Lh / 2, -0.045, -0.015, 0.05, 0.80, M["hemnes_bead"], HB, wuv=True)
box("Гръб горна рамка", -Lh / 2, Lh / 2, -0.06, -0.004, 0.80, 0.845, M["hemnes"], HB, bevel=0.004)
box("Гръб долна рамка", -Lh / 2, Lh / 2, -0.05, -0.01, 0.05, 0.12, M["hemnes"], HB)
for s in (-1, 1):
    xo = s * Lh / 2
    xi = xo - s * 0.05
    a, b = min(xo, xi), max(xo, xi)
    box("Табла", a + 0.005, b - 0.005, -0.84, -0.06, 0.06, 0.80, M["hemnes_bead"], HB, wuv=True)
    box("Табла рамка", a, b, -0.885, -0.004, 0.80, 0.845, M["hemnes"], HB, bevel=0.004)
    box("Стълб", a, b, -0.885, -0.825, 0.0, 0.845, M["hemnes"], HB, bevel=0.003)
    box("Стълб", a, b, -0.07, -0.004, 0.0, 0.845, M["hemnes"], HB, bevel=0.003)
    box("Табла долна", a, b, -0.84, -0.06, 0.04, 0.12, M["hemnes"], HB)
box("Основа фронт", -0.985, 0.985, -0.87, -0.845, 0.04, 0.39, M["hemnes"], HB, bevel=0.003)
box("Основа", -0.985, 0.985, -0.845, -0.05, 0.30, 0.38, M["hemnes"], HB)
dw = (1.97 - 0.04) / 3
for i in range(3):
    a = -0.965 + i * (dw + 0.02) - 0.005
    shaker(HB, a, a + dw, 0.075, 0.335, -0.87, M["hemnes"], handle="woodknob", hpos=(a + dw / 2, 0.205), frame=0.045)
mat_ob = box("Матрак", -0.975, 0.975, -0.855, -0.05, 0.38, 0.53, M["sheet"], HB)
soft(mat_ob, 0.04, 3, 1)
duv = box("Завивка", -0.30, 0.965, -0.86, -0.06, 0.53, 0.60, M["bedding"], HB, wuv=True)
soft(duv, 0.03, 3, 1)


def cushion(par, x, z, w, h, t, mat, tilt=0.3, yaw=0.0, y=-0.14, pompoms=False):
    E = empty("Възглавница", x, y, yaw, z, par)
    E.rotation_euler = (-tilt, 0, yaw)
    c = box("Възглавница", -w / 2, w / 2, -t / 2, t / 2, -h / 2, h / 2, mat, E, wuv=True)
    soft(c, min(t * 0.45, 0.06), 3, 2)
    if pompoms:
        r = random.Random(int(x * 100))
        for i in range(4):
            for j in range(4):
                sphere("Пухче", 0.013, (-w / 2 + 0.07 + i * (w - 0.14) / 3, -t / 2 - 0.006, -h / 2 + 0.07 + j * (h - 0.14) / 3),
                       r.choice([M["linen_sage"], M["linen_pink"], M["linen_beige"]]), E, segs=10, rings=6)
    return E


cushion(HB, -0.70, 0.76, 0.48, 0.46, 0.16, M["linen_pink"], 0.32)
cushion(HB, -0.22, 0.74, 0.50, 0.42, 0.15, M["bedding"], 0.30)
cushion(HB, 0.26, 0.74, 0.45, 0.45, 0.15, M["linen_cream"], 0.30, pompoms=True)
cushion(HB, 0.70, 0.72, 0.42, 0.40, 0.14, M["linen_pink"], 0.36, 0.12)
# throw over the arm end
throw = box("Одеяло", 0.55, 0.97, -0.86, -0.08, 0.60, 0.625, M["linen_sage"], HB)
soft(throw, 0.01, 2, 1)

# wall sconces either side of the inner windows (plug-in, pleated)
for py in (4.55, 6.45):
    cyl("Аплик основа", 0.04, 0.02, (3.89, py, 1.55), M["brass"], axis="X")
    cyl("Аплик рамо", 0.006, 0.14, (3.82, py, 1.55), M["brass"], axis="X")
    cyl("Аплик абажур", 0.07, 0.15, (3.74, py, 1.60), M["shade_lamp"], r2=0.05, segs=40)

# ---------------------------------------------------------------- vitrine (east, py 3.20..4.10)
V = empty("Витрина", 3.90, 3.65, FACE["W"])
t = 0.018
box("Витрина страна", -0.45, -0.45 + t, -0.37, 0, 0.0, 1.97, M["cab"], V)
box("Витрина страна", 0.45 - t, 0.45, -0.37, 0, 0.0, 1.97, M["cab"], V)
box("Витрина капак", -0.465, 0.465, -0.39, 0.0, 1.97, 2.0, M["cab"], V, bevel=0.004)
box("Витрина цокъл", -0.432, 0.432, -0.34, 0, 0.0, 0.09, M["cab"], V)
box("Витрина гръб", -0.432, 0.432, -0.012, 0, 0.09, 1.97, M["pink"], V)
for z in (0.09, 0.83, 1.22, 1.58):
    box("Витрина рафт", -0.432, 0.432, -0.36, -0.012, z, z + 0.018, M["cab"], V)
shaker(V, -0.448, -0.002, 0.092, 0.83, -0.37, handle="knob", hpos=(-0.05, 0.75))
shaker(V, 0.002, 0.448, 0.092, 0.83, -0.37, handle="knob", hpos=(0.05, 0.75))
shaker(V, -0.448, -0.002, 0.85, 1.965, -0.37, glass=True, handle="knob", hpos=(-0.05, 1.0))
shaker(V, 0.002, 0.448, 0.85, 1.965, -0.37, glass=True, handle="knob", hpos=(0.05, 1.0))
books(V, 0.02, -0.03, 0.848, 0.38, along="X", depth=0.24, seed=8)
lathe("Ваза", [(0, 0), (0.05, 0), (0.08, 0.1), (0.04, 0.2), (0.05, 0.24), (0, 0.24)], (-0.2, -0.18, 1.238), simple("Ваза зелена", "#9FB5A3", 0.15, Coat_Weight=1.0), V)
for i in range(3):
    lathe("Чашка", [(0, 0), (0.03, 0), (0.042, 0.08), (0.0, 0.08)], (0.05 + i * 0.11, -0.18, 1.238), M["ceramic"], V)
for i in range(4):
    cyl("Чиния", 0.1, 0.012, (0.18, -0.18, 1.598 + i * 0.014), M["linen_pink"], V)
lathe("Купа", [(0, 0), (0.05, 0), (0.1, 0.06), (0.0, 0.06)], (-0.18, -0.18, 1.598), M["lampcream"], V)
box("LED витрина", -0.40, 0.40, -0.34, -0.32, 1.955, 1.965, M["led"], V)
lathe("Саксия висяща", [(0, 0), (0.06, 0), (0.08, 0.11), (0, 0.11)], (0.0, -0.18, 2.0), M["terracotta"], V)
plant_leaves(V, (0.0, -0.18, 2.06), 0.18, 160, M["green_leaf"], (0.05, 0.03), 13, 0.4, 0.8)


# ---------------------------------------------------------------- hall wardrobe (east, py 1.00..2.80)
WD = empty("Гардероб", 3.90, 1.90, FACE["W"])
box("Гардероб корпус", -0.90, 0.90, -0.58, 0, 0.08, 2.36, M["cab"], WD)
box("Гардероб цокъл", -0.90, 0.90, -0.54, 0, 0, 0.08, M["cab"], WD)
box("Гардероб пълнеж", -0.90, 0.90, -0.60, 0, 2.36, H, M["cab"], WD)
box("Корниз", -0.905, 0.905, -0.615, 0, 2.38, 2.42, M["cab"], WD, bevel=0.006)
for i, (a, b) in enumerate(((-0.897, -0.453), (-0.447, -0.003), (0.003, 0.447), (0.453, 0.897))):
    hx = b - 0.04 if i % 2 == 0 else a + 0.04
    shaker(WD, a, b, 0.083, 2.357, -0.58, handle="knob", hpos=(hx, 1.05), mid=1.30)

# hall: bench, mirror, niche doors, entry door, bath door
box("Пейка", 2.18, 2.66, 0.02, 0.36, 0.40, 0.43, M["oak"], bevel=0.003, wuv=True)
for x in (2.19, 2.62):
    box("Пейка крак", x, x + 0.035, 0.03, 0.35, 0, 0.40, M["oak"], wuv=True)
box("Пейка рафт", 2.225, 2.62, 0.04, 0.34, 0.10, 0.12, M["oak"], wuv=True)
cush = box("Пейка възглавница", 2.20, 2.64, 0.04, 0.34, 0.43, 0.48, M["linen_sage"])
soft(cush, 0.02, 2, 1)
for i, x in enumerate((2.28, 2.45)):
    box("Обувка", x, x + 0.10, 0.06, 0.32, 0.12, 0.20, [M["linen_cream"], M["black_matte"]][i], bevel=0.03, seg=3)
cyl("Огледало", 0.25, 0.008, (2.42, 0.014, 1.32), M["mirror"], axis="Y", segs=64)
bm = bmesh.new()
bmesh.ops.create_circle(bm, cap_ends=False, segments=64, radius=0.255)
ring = mesh_obj("Рамка огледало", bm, M["brass"], loc=(2.42, 0.02, 1.32), rot=(math.pi / 2, 0, 0))
sk = ring.modifiers.new("skin", "SCREW")
bpy.data.objects.remove(ring)
tor = bpy.data.meshes.new("Тор")
bm = bmesh.new()
segs, rs = 64, 10
for i in range(segs):
    a = 2 * math.pi * i / segs
    for j in range(rs):
        b = 2 * math.pi * j / rs
        rr = 0.255 + 0.012 * math.cos(b)
        bm.verts.new((rr * math.cos(a), 0.012 * math.sin(b), rr * math.sin(a)))
bm.verts.ensure_lookup_table()
for i in range(segs):
    for j in range(rs):
        a = bm.verts[i * rs + j]
        b = bm.verts[((i + 1) % segs) * rs + j]
        c = bm.verts[((i + 1) % segs) * rs + (j + 1) % rs]
        d = bm.verts[i * rs + (j + 1) % rs]
        bm.faces.new((a, b, c, d))
for f in bm.faces:
    f.smooth = True
mesh_obj("Рамка огледало", bm, M["brass"], loc=(2.42, 0.022, 1.32))
ND = empty("Ниша врати", 2.16, 1.50, FACE["E"])
shaker(ND, -0.34, -0.002, 0.03, 2.20, 0.0, handle="knob", hpos=(-0.04, 1.05), mid=1.25)
shaker(ND, 0.002, 0.34, 0.03, 2.20, 0.0, handle="knob", hpos=(0.04, 1.05), mid=1.25)
box("Пералня", 1.40, 2.00, 1.22, 1.80, 0, 0.85, M["washer"], bevel=0.01)
# entry door B1 (90 cm, closed)
box("Входна врата", 2.70, 3.58, -0.08, -0.03, 0.0, 2.035, M["cab"], bevel=0.002)
ED = empty("Входна врата фронт", 3.14, -0.03, FACE["N"])
shaker(ED, -0.44, 0.44, 0.0, 2.035, 0.0, M["cab"], frame=0.11, mid=1.0, t=0.012)
for x0, x1, z0, z1 in ((2.61, 2.69, 0, 2.13), (3.59, 3.67, 0, 2.13), (2.61, 3.67, 2.05, 2.13)):
    box("Каса", x0, x1, 0, 0.015, z0, z1, M["white_satin"], bevel=0.003)
cyl("Брава розетка", 0.026, 0.012, (2.79, -0.012, 1.02), M["brass"], axis="Y")
tube("Брава", [(2.79, -0.02, 1.02), (2.79, -0.06, 1.02), (2.92, -0.065, 1.015)], 0.009, M["brass"])
cyl("Шпионка", 0.012, 0.012, (3.14, -0.012, 1.55), M["brass"], axis="Y")
box("Изтривалка", 2.75, 3.50, 0.08, 0.60, 0.0, 0.012, M["cane"], bevel=0.004)
# bath door B2 (63 cm, open ~75 deg into bathroom)
BDp = empty("Врата баня", 2.10, 0.15, math.pi / 2 + math.radians(88))
box("Врата баня", 0.0, 0.63, -0.02, 0.02, 0.0, 2.0, M["cab"], BDp, bevel=0.002)
for side in (-1, 1):
    SD = empty("Врата баня страна", 0.315, side * 0.02, 0 if side < 0 else math.pi, 0, BDp)
    shaker(SD, -0.315, 0.315, 0.0, 2.0, 0.0, M["cab"], frame=0.09, mid=1.05, t=0.01, handle="knob", hpos=(0.25 * (-side), 1.0))
for y0, y1, z0, z1 in ((0.07, 0.15, 0, 2.10), (0.78, 0.86, 0, 2.10), (0.07, 0.86, 2.02, 2.10)):
    box("Каса баня", 2.16, 2.175, y0, y1, z0, z1, M["white_satin"], bevel=0.003)

# ---------------------------------------------------------------- bathroom
box("Инсталация WC", 0, 0.20, 0.0, 1.04, 0, 1.10, M["zellige"], wuv=True)
box("Инсталация WC плот", 0, 0.215, 0.0, 1.04, 1.10, 1.125, M["sill"], bevel=0.004)
wc = box("Тоалетна", 0.20, 0.72, 0.44, 0.80, 0.14, 0.40, M["ceramic"])
soft(wc, 0.07, 4, 1)
seat = box("Седалка WC", 0.21, 0.74, 0.445, 0.795, 0.40, 0.425, M["ceramic"])
soft(seat, 0.03, 3, 1)
box("Бутон", 0.20, 0.206, 0.54, 0.70, 0.88, 1.00, M["brass"], bevel=0.004)
box("Шкаф мивка", 0.95, 1.45, 0.0, 0.42, 0.52, 0.80, M["oak"], bevel=0.004, wuv=True)
for i in range(16):
    cyl("Рифел мивка", 0.0075, 0.26, (0.965 + i * 0.031, 0.425, 0.66), M["oak"], segs=12, wuv=True)
# vessel basin built from real walls (no boolean)
box("Мивка дъно", 0.99, 1.41, 0.05, 0.37, 0.80, 0.83, M["ceramic"], bevel=0.008, seg=3)
for a, b, c, d in ((0.98, 1.0, 0.04, 0.38), (1.40, 1.42, 0.04, 0.38), (0.98, 1.42, 0.04, 0.06), (0.98, 1.42, 0.36, 0.38)):
    box("Мивка стена", a, b, c, d, 0.80, 0.92, M["ceramic"], bevel=0.006, seg=3)
cyl("Сифон мивка", 0.02, 0.004, (1.20, 0.21, 0.832), M["brass"])
tube("Чучур", [(1.20, 0.0, 1.03), (1.20, 0.10, 1.03), (1.20, 0.17, 1.02)], 0.011, M["brass"])
cyl("Розетка", 0.03, 0.01, (1.20, 0.005, 1.03), M["brass"], axis="Y")
cyl("Кран", 0.025, 0.03, (1.20, 0.015, 1.13), M["brass"], axis="Y")
# arched mirror
bm = bmesh.new()
pts = [(-0.23, 0), (0.23, 0)]
for i in range(25):
    a = math.pi * i / 24
    pts.append((0.23 * math.cos(a), 0.70 + 0.23 * math.sin(a)))
vs = [bm.verts.new((x, 0, z)) for x, z in [(0.23, 0)] + pts[2:] + [(-0.23, 0)]]
bm.faces.new(vs)
ext = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
for v in [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]:
    v.co.y += 0.006
mesh_obj("Огледало арка", bm, M["mirror"], loc=(1.20, 0.012, 1.08))
outline = [(1.20 + x, 0.02, 1.08 + z) for x, z in [(0.23, 0)] + pts[2:] + [(-0.23, 0), (0.23, 0)]]
poly_tube("Рамка арка", outline, 0.008, M["brass"])
sphere("Аплик баня", 0.07, (1.20, 0.10, 2.16), M["shade_on"])
cyl("Аплик баня", 0.04, 0.012, (1.20, 0.006, 2.16), M["brass"], axis="Y")
cyl("Аплик рамо", 0.008, 0.08, (1.20, 0.05, 2.16), M["brass"], axis="Y")
# shower 124 x 80 walk-in
box("Душ корито", 0.0, 1.24, 1.04, 1.84, 0.0, 0.03, M["ceramic_matte"], bevel=0.003)
box("Сифон линеен", 0.06, 1.18, 1.76, 1.79, 0.03, 0.032, M["steel"])
box("Душ стъкло", 0.0, 0.70, 1.036, 1.044, 0.03, 2.00, M["glass"])
box("Профил", 0.68, 0.705, 1.03, 1.05, 0.03, 2.0, M["black_matte"])
box("Профил", 0.0, 0.70, 1.03, 1.05, 0.03, 0.045, M["black_matte"])
box("Стабилизатор", 0.685, 0.70, 1.04, 1.84, 1.95, 1.965, M["black_matte"])
cyl("Душ пита", 0.125, 0.01, (0.55, 1.42, 2.17), M["black_matte"], segs=64)
box("Душ рамо", 0.54, 0.56, 1.42, 1.84, 2.18, 2.20, M["black_matte"])
cyl("Смесител", 0.035, 0.015, (0.55, 1.833, 1.10), M["black_matte"], axis="Y")
box("Смесител лост", 0.545, 0.555, 1.75, 1.83, 1.095, 1.105, M["black_matte"])
for i, (h, r, c) in enumerate(((0.18, 0.03, "#F1EEE7"), (0.15, 0.028, "#C9A27A"), (0.2, 0.025, "#DDB2A9"))):
    cyl("Шише", r, h, (0.06 + i * 0.07, 1.10, 1.125 + h / 2), simple(f"Шише{i}", c, 0.3, Coat_Weight=0.5))
# towel rail on niche wall
for x in (1.45, 1.95):
    cyl("Сушилка", 0.012, 0.92, (x, 0.995, 1.00), M["brass"])
for z in (0.62, 0.84, 1.06, 1.28, 1.44):
    cyl("Сушилка", 0.009, 0.50, (1.70, 0.995, z), M["brass"], axis="X")
tw = box("Хавлия", 1.49, 1.91, 0.96, 0.985, 0.95, 1.40, M["towel"])
soft(tw, 0.01, 2, 1)
cyl("Плафон баня", 0.13, 0.03, (0.95, 0.90, H - 0.015), M["shade_on"])
cyl("Плафон коридор", 0.13, 0.03, (2.85, 1.00, H - 0.015), M["shade_on"])

# ---------------------------------------------------------------- work corner (west, py 6.83..7.93)
DK = empty("Бюро", 0.0, 7.38, FACE["E"])
box("Бюро плот", -0.55, 0.55, -0.55, 0, 0.72, 0.75, M["white_satin"], DK, bevel=0.004)
box("Бюро царга", -0.50, 0.50, -0.50, -0.03, 0.62, 0.72, M["white_satin"], DK)
shaker(DK, -0.46, -0.02, 0.625, 0.715, -0.50, M["white_satin"], handle="knob", hpos=(-0.24, 0.67), frame=0.025)
shaker(DK, 0.02, 0.46, 0.625, 0.715, -0.50, M["white_satin"], handle="knob", hpos=(0.24, 0.67), frame=0.025)
for x in (-0.50, 0.50):
    for y in (-0.50, -0.05):
        turned_leg("Крак", 0.72, (x, y, 0), M["white_satin"], DK, 0.85)
# bentwood cane chair
DC = empty("Стол бюро", 1.02, 7.30, FACE["W"])
seat = box("Седалка", -0.21, 0.21, -0.42, -0.02, 0.44, 0.47, M["cane"], DC)
soft(seat, 0.02, 2, 1)
for x in (-0.19, 0.19):
    for y in (-0.40, -0.05):
        cyl("Крак", 0.014, 0.45, (x, y, 0.22), M["dark_wood"], DC, r2=0.016)
pts = [(-0.20, -0.04, 0.47)] + [(0.20 * math.cos(a), -0.04 + 0.04 * math.sin(a), 0.80 - 0.0 * a) for a in
                                 [math.pi * (1 - i / 10) for i in range(11)]] + [(0.20, -0.04, 0.47)]
tube("Облегалка", [(-0.20, -0.04, 0.47), (-0.21, -0.03, 0.70), (-0.12, 0.0, 0.85), (0.12, 0.0, 0.85), (0.21, -0.03, 0.70), (0.20, -0.04, 0.47)],
     0.014, M["dark_wood"], DC)
box("Облегалка плетка", -0.17, 0.17, -0.03, -0.02, 0.58, 0.80, M["cane"], DC)
# shelves above desk
for z in (1.30, 1.68):
    box("Рафт", 0, 0.24, 6.95, 7.90, z, z + 0.03, M["oak"], bevel=0.002, wuv=True)
    for py in (7.05, 7.80):
        box("Конзола рафт", 0.0, 0.18, py - 0.01, py + 0.01, z - 0.08, z, M["brass"])
books(None, 6.98, 0.22, 1.33, 0.40, along="Y", depth=0.2, seed=21)
books(None, 7.50, 0.22, 1.71, 0.30, along="Y", depth=0.2, seed=22)
lathe("Саксия", [(0, 0), (0.05, 0), (0.065, 0.1), (0, 0.1)], (0.12, 7.65, 1.33), M["terracotta"])
plant_leaves(None, (0.12, 7.65, 1.47), 0.09, 140, M["green_leaf"], (0.045, 0.02), 31, 0.8, 0.9)
lathe("Ваза", [(0, 0), (0.04, 0), (0.06, 0.08), (0.03, 0.16), (0.035, 0.18), (0, 0.18)], (0.12, 7.05, 1.71), M["lampcream"])
box("Рамка снимка", 0.03, 0.05, 7.20, 7.40, 1.71, 1.97, M["oak"], bevel=0.003)
box("Снимка", 0.051, 0.053, 7.22, 7.38, 1.73, 1.95, M["art1"], wuv=True)
# mushroom lamp
cyl("Лампа стойка", 0.035, 0.24, (0.20, 7.78, 0.87), M["lampcream"])
cyl("Лампа основа", 0.065, 0.02, (0.20, 7.78, 0.76), M["lampcream"])
lathe("Лампа шапка", [(0.0, 0.11), (0.06, 0.105), (0.10, 0.08), (0.125, 0.04), (0.13, 0.0), (0.0, 0.0)], (0.20, 7.78, 0.98), M["shade_lamp"])
box("Тетрадка", 0.20, 0.42, 7.10, 7.40, 0.75, 0.765, M["paper"], bevel=0.002)
box("Лаптоп", 0.20, 0.44, 7.45, 7.78, 0.75, 0.765, simple("Алуминий", "#C7C9CB", 0.3, 1.0), bevel=0.004)

# ---------------------------------------------------------------- reading corner (north-east)
rr = bpy.data.meshes.new("Кръгъл килим")
cyl("Кръгъл килим", 0.78, 0.012, (2.50, 7.30, 0.006), M["boucle"], segs=96)
AC = empty("Кресло", 2.92, 7.56, math.atan2(-1.1, 1.3))
b = box("Кресло основа", -0.42, 0.42, -0.40, 0.40, 0.05, 0.40, M["boucle"], AC)
soft(b, 0.12, 4, 2)
b = box("Кресло седалка", -0.30, 0.30, -0.40, 0.22, 0.38, 0.50, M["boucle"], AC)
soft(b, 0.06, 3, 2)
b = box("Кресло гръб", -0.42, 0.42, 0.16, 0.40, 0.38, 0.80, M["boucle"], AC)
soft(b, 0.10, 4, 2)
for s in (-1, 1):
    b = box("Кресло подлакътник", min(s * 0.42, s * 0.27), max(s * 0.42, s * 0.27), -0.38, 0.38, 0.38, 0.64, M["boucle"], AC)
    soft(b, 0.07, 3, 2)
cushion(AC, 0.0, 0.62, 0.40, 0.32, 0.12, M["linen_sage"], 0.25, 0.0, 0.10)
# side table
cyl("Масичка плот", 0.21, 0.03, (3.66, 7.42, 0.52), M["oak"], segs=64, wuv=True)
lathe("Масичка крак", [(0, 0), (0.14, 0), (0.14, 0.02), (0.05, 0.06), (0.035, 0.30), (0.05, 0.505), (0, 0.505)], (3.66, 7.42, 0), M["oak"])
lathe("Чаша", [(0, 0), (0.035, 0), (0.042, 0.09), (0, 0.09)], (3.70, 7.36, 0.535), M["ceramic"])
box("Книга", 3.55, 3.75, 7.44, 7.58, 0.535, 0.56, M["book"][4], bevel=0.002)
# pleated floor lamp
cyl("Лампион основа", 0.14, 0.02, (3.60, 7.82, 0.01), M["brass"], segs=48)
cyl("Лампион тръба", 0.009, 1.36, (3.60, 7.82, 0.70), M["brass"])
bm = bmesh.new()
segs = 120
for zi, (z, r) in enumerate(((0.0, 0.21), (0.32, 0.14))):
    for i in range(segs):
        a = 2 * math.pi * i / segs
        rr_ = r + 0.008 * math.cos(a * 30)
        bm.verts.new((rr_ * math.cos(a), rr_ * math.sin(a), z))
bm.verts.ensure_lookup_table()
for i in range(segs):
    bm.faces.new((bm.verts[i], bm.verts[(i + 1) % segs], bm.verts[segs + (i + 1) % segs], bm.verts[segs + i]))
for f in bm.faces:
    f.smooth = True
mesh_obj("Лампион абажур", bm, M["shade_lamp"], loc=(3.60, 7.82, 1.30))
sphere("Крушка лампион", 0.03, (3.60, 7.82, 1.42), M["shade_lamp"])
# olive tree
lathe("Саксия маслина", [(0, 0), (0.17, 0), (0.22, 0.42), (0.235, 0.44), (0.0, 0.44)], (1.70, 7.80, 0), M["terracotta"])
cyl("Почва", 0.21, 0.01, (1.70, 7.80, 0.425), M["soil"])
tube("Ствол", [(1.70, 7.80, 0.40), (1.72, 7.79, 0.90), (1.68, 7.81, 1.20), (1.71, 7.78, 1.45)], 0.025, M["bark"])
for dx, dy, dz in ((-0.15, 0.02, 1.35), (0.16, -0.03, 1.42), (0.0, 0.05, 1.70), (-0.08, -0.08, 1.55), (0.1, 0.1, 1.58)):
    tube("Клон", [(1.70, 7.80, 1.25), (1.70 + dx * 0.6, 7.80 + dy * 0.6, dz - 0.1), (1.70 + dx, 7.80 + dy, dz)], 0.01, M["bark"])
for i, (dx, dy, dz, r) in enumerate(((-0.17, 0.0, 1.40, 0.2), (0.18, -0.02, 1.47, 0.2), (0.0, 0.04, 1.76, 0.22),
                                      (-0.09, -0.1, 1.60, 0.18), (0.11, 0.12, 1.62, 0.18))):
    plant_leaves(None, (1.70 + dx, 7.80 + dy, dz), r, 520, M["olive_leaf"], (0.07, 0.013), 100 + i, 0.75)

# ---------------------------------------------------------------- textiles at windows
def curtain(x0, x1, y, amp, wl, z0, z1, mat, name, thick=0.0):
    bm = bmesh.new()
    nx = max(2, int((x1 - x0) / 0.008))
    rows = []
    for zi, z in enumerate((z0, (z0 + z1) / 2, z1)):
        row = []
        for i in range(nx + 1):
            x = x0 + (x1 - x0) * i / nx
            yy = y + amp * math.sin(2 * math.pi * (x - x0) / wl) * (1.0 - 0.15 * zi)
            row.append(bm.verts.new((x, yy, z)))
        rows.append(row)
    for j in range(len(rows) - 1):
        for i in range(nx):
            bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
    for f in bm.faces:
        f.smooth = True
    ob = mesh_obj(name, bm, mat)
    if thick:
        so = ob.modifiers.new("sol", "SOLIDIFY")
        so.thickness = thick
    return ob


cyl("Корниз", 0.012, 3.90, (1.95, 7.99, 2.50), M["brass"], axis="X")
for x in (0.0, 3.90):
    sphere("Накрайник", 0.022, (x, 7.99, 2.50), M["brass"])
curtain(0.30, 3.60, 8.045, 0.015, 0.14, 0.02, 2.48, M["sheer"], "Перде")
curtain(0.02, 0.52, 7.985, 0.03, 0.10, 0.015, 2.49, M["curtain_pink"], "Завеса", 0.003)
curtain(3.38, 3.88, 7.985, 0.03, 0.10, 0.015, 2.49, M["curtain_pink"], "Завеса", 0.003)
for a, b in ((4.70, 5.45), (5.55, 6.30)):
    for k in range(3):
        z = 2.08 + k * 0.06
        f = box("Римска щора", 3.84, 3.89, a, b, z, z + 0.075, M["linen_cream"])
        soft(f, 0.02, 2, 1)
    box("Щора плат", 3.875, 3.885, a, b, 2.06, 2.27, M["linen_cream"])

# ---------------------------------------------------------------- exterior context
box("Земя", -60, 65, 8.35, 90, -7.2, -7.0, M["ground"])
box("Трева", -60, 65, 9.5, 74, -7.0, -6.98, M["grass"])
box("Сграда отсреща", -40, 50, 75, 85, -7, 12, M["plaster_ext"])
for row in range(7):
    for col_ in range(18):
        x = -22 + col_ * 3.0
        z = -5.5 + row * 3.0
        box("Прозорец", x * 2, x * 2 + 1.4, 74.9, 75.0, z, z + 1.5, M["ext_glass"])
box("Сграда вляво", -30, -6, 8.35, 26, -7, 9, M["plaster_ext"])
M["tree_leaf"] = leafmat("Листа дървета", "#56703F", "#86A05C")
for i, (tx, ty, tz, r) in enumerate(((-1.5, 15, -1.5, 4.5), (5.5, 19, -0.5, 5.0), (12, 16, -2, 4.0), (-8, 20, -1, 4.5), (2.0, 28, 0.5, 5.5))):
    cyl("Ствол дърво", 0.28, 9, (tx, ty, -2.5), M["bark"], segs=12)
    rt = random.Random(i)
    for k in range(7):
        cx, cy, cz = tx + rt.uniform(-r, r) * 0.6, ty + rt.uniform(-r, r) * 0.5, tz + 3 + rt.uniform(-r, r) * 0.45
        tube("Клон", [(tx, ty, tz + 0.5), ((tx + cx) / 2, (ty + cy) / 2, (tz + 0.5 + cz) / 2 + 0.6), (cx, cy, cz)], 0.08, M["bark"])
        plant_leaves(None, (cx, cy, cz), r * 0.55, 900, M["tree_leaf"], (0.28, 0.13), 500 + i * 10 + k, 0.8, 0.4)
# light well behind the inner (east) windows
box("Светлинна шахта", 5.6, 5.8, 3.5, 7.5, -3, 6, M["plaster_ext"])
box("Светлинна шахта под", 4.15, 5.6, 3.5, 7.5, -0.4, -0.2, M["plaster_ext"])

world_uvs()

# ---------------------------------------------------------------- lights
def area(name, loc, rot, size, size_y=None, energy=50, color=(1, 1, 1), portal=False, shape=None):
    ld = D.lights.new(name, "AREA")
    ld.shape = shape or ("RECTANGLE" if size_y else "SQUARE")
    ld.size = size
    if size_y:
        ld.size_y = size_y
    ld.energy = energy
    ld.color = color
    if portal:
        ld.cycles.is_portal = True
    ob = D.objects.new(name, ld)
    ob.location = loc
    ob.rotation_euler = rot
    return link(ob)


def point(name, loc, energy, color=(1.0, 0.78, 0.55), radius=0.03):
    ld = D.lights.new(name, "POINT")
    ld.energy = energy
    ld.color = color
    ld.shadow_soft_size = radius
    ob = D.objects.new(name, ld)
    ob.location = loc
    return link(ob)


def spot(name, loc, target, energy, angle=0.7, blend=0.5, color=(1.0, 0.8, 0.6), radius=0.02):
    ld = D.lights.new(name, "SPOT")
    ld.energy = energy
    ld.spot_size = angle
    ld.spot_blend = blend
    ld.color = color
    ld.shadow_soft_size = radius
    ob = D.objects.new(name, ld)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = Vector((0, 0, -1)).rotation_difference(d).to_euler()
    return link(ob)


WARM = (1.0, 0.76, 0.52)
LIGHTS = {}
# daylight portals
LIGHTS["portal"] = [
    area("Портал север", (1.95, 8.30, 1.60), (math.radians(90), 0, 0), 3.30, 1.50, portal=True),
    area("Портал изток 1", (4.10, 5.075, 1.60), (math.radians(90), 0, math.radians(90)), 0.65, 1.30, portal=True),
    area("Портал изток 2", (4.10, 5.925, 1.60), (math.radians(90), 0, math.radians(90)), 0.65, 1.30, portal=True),
]
sun_d = D.lights.new("Слънце", "SUN")
sun_d.energy = 4.5
sun_d.angle = math.radians(1.2)
sun_d.color = (1.0, 0.95, 0.88)
SUN = link(D.objects.new("Слънце", sun_d))
SUN.rotation_euler = Vector((0, 0, -1)).rotation_difference(Vector((-0.30, -0.80, -0.52))).to_euler()

LIGHTS["pendant"] = [point("Пендел", (PX, PY, 1.585), 45, WARM, 0.03)]
LIGHTS["led"] = [area("LED рамо А", (1.43, 2.13, 1.44), (0, 0, 0), 1.20, 0.03, 16, (1.0, 0.85, 0.68)),
                 area("LED рамо Б", (0.17, 2.41, 1.44), (0, 0, math.radians(90)), 0.26, 0.03, 4, (1.0, 0.85, 0.68)),
                 area("LED рамо Б", (0.17, 3.36, 1.44), (0, 0, math.radians(90)), 0.36, 0.03, 5, (1.0, 0.85, 0.68))]
LIGHTS["spots"] = [spot("Спот", p, q, 30, math.radians(50), 0.6, WARM) for p, q in SPOTS]
LIGHTS["vitrine"] = [area("LED витрина", (3.70, 3.65, 1.94), (0, 0, 0), 0.75, 0.03, 6, (1.0, 0.85, 0.68))]
LIGHTS["floor"] = [point("Лампион", (3.60, 7.82, 1.42), 60, WARM, 0.05)]
LIGHTS["desk"] = [point("Лампа бюро", (0.20, 7.78, 1.02), 12, WARM, 0.03)]
LIGHTS["sconce"] = [point("Аплик", (3.74, py, 1.58), 14, WARM, 0.03) for py in (4.55, 6.45)]
LIGHTS["bath"] = [area("Баня таван", (0.95, 0.90, H - 0.035), (0, 0, 0), 0.24, energy=55, color=(1.0, 0.88, 0.72), shape="DISK"),
                  point("Аплик баня", (1.20, 0.10, 2.16), 12, WARM, 0.05)]
LIGHTS["hall"] = [area("Коридор таван", (2.85, 1.00, H - 0.035), (0, 0, 0), 0.24, energy=45, color=(1.0, 0.86, 0.70), shape="DISK")]
for k, ls in LIGHTS.items():
    for l in ls:
        l["group"] = k

# ---------------------------------------------------------------- world, render settings
world = D.worlds.new("Небе")
scene.world = world
world.use_nodes = True
wn = world.node_tree
wn.nodes.clear()
sky = wn.nodes.new("ShaderNodeTexSky")
sky.sky_type = "MULTIPLE_SCATTERING"
sky.sun_disc = False
sky.sun_elevation = math.radians(32)
sky.sun_rotation = math.radians(200)
bg = wn.nodes.new("ShaderNodeBackground")
bg.inputs["Strength"].default_value = 1.0
bg.name = "sky_bg"
wo = wn.nodes.new("ShaderNodeOutputWorld")
wn.links.new(sky.outputs[0], bg.inputs[0])
wn.links.new(bg.outputs[0], wo.inputs[0])

scene.render.engine = "CYCLES"
cy = scene.cycles
cy.device = "CPU"
cy.samples = 256
cy.use_adaptive_sampling = True
cy.adaptive_threshold = 0.012
cy.use_denoising = True
cy.denoiser = "OPENIMAGEDENOISE"
cy.max_bounces = 10
cy.diffuse_bounces = 5
cy.glossy_bounces = 4
cy.transmission_bounces = 8
cy.transparent_max_bounces = 16
cy.caustics_reflective = False
cy.caustics_refractive = False
cy.blur_glossy = 1.0
cy.sample_clamp_indirect = 8.0
scene.view_settings.view_transform = "AgX"
try:
    scene.view_settings.look = "AgX - Medium High Contrast"
except Exception:
    pass
scene.render.film_transparent = False
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("saved", OUT_BLEND, len(D.objects), "objects")
