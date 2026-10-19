# Шалвия и роза — едностаен апартамент

3D интериорен проект по `plan/Apartment_Plan_A3_1-50.pdf` (вътрешно 390 × 810 см) и кухненската концепция от IKEA (`plan/concept_kitchen.jpg`).

- `scene/` — пълната Blender сцена като код (Blender 5.1, Cycles).
- `viewer/` — уеб обиколка 360°, галерия, план и спецификация.
- `renders/` — финалните фотореалистични кадри и панорами.

## Рендиране

```bash
python3 -m venv bl && bl/bin/pip install bpy==5.1.2 pillow numpy
cd scene
../bl/bin/python gen_textures.py tex       # тапет, спално бельо, килим, ТВ картина
../bl/bin/python build_scene.py            # -> apartment.blend
../bl/bin/python render.py dining ../renders/dining.jpg --res 1600x1000 --samples 128
../bl/bin/python render.py p_hall ../renders/pano/p_hall.jpg --res 4096x2048 --samples 64
../bl/bin/python render.py plan plan_raw.jpg --res 900x1800 --samples 64 && ../bl/bin/python plan_post.py plan_raw.jpg ../renders/plan.jpg
```

Гледни точки: `entrance kitchen dining tv reading work back bath bath2`; панорами: `p_hall p_kitchen p_dining p_living p_bath`; `plan`. Режим `--mode evening` включва вечерното осветление.
