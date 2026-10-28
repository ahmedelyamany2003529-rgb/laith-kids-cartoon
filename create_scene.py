# Blender Python script: first 10-second scene for "مغامرات ليث"
# Run in Blender: blender -b -P create_scene.py
# Output: renders/laith_scene.mp4
import bpy, math, os
from mathutils import Vector

# ---------- Reset ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    pass

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "renders")
os.makedirs(OUT, exist_ok=True)

# ---------- Helpers ----------
def mat(name, color, roughness=0.72):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*color, 1)
    bs.inputs["Roughness"].default_value = roughness
    return m

gold = mat("Lion | honey gold", (0.95, 0.43, 0.08))
light_gold = mat("Lion | face gold", (1.0, 0.62, 0.20))
cream = mat("Muzzle | cream", (1.0, 0.84, 0.61))
brown = mat("Nose | cocoa", (0.20, 0.08, 0.035))
dark = mat("Eyes | deep brown", (0.055, 0.025, 0.012), 0.25)
white = mat("Eye highlights", (1.0, 0.98, 0.87), 0.18)
teal = mat("Signature teal scarf", (0.02, 0.47, 0.55))
yellow = mat("Scarf paw emblem", (1.0, 0.72, 0.12))
green = mat("Grass", (0.18, 0.42, 0.12))
green2 = mat("Bush leaves", (0.11, 0.32, 0.09))
trunkmat = mat("Tree trunk", (0.28, 0.12, 0.045))
sky = mat("Background sky", (0.42, 0.73, 0.92))
mapmat = mat("Old map parchment", (0.78, 0.59, 0.31))
ink = mat("Map markings", (0.25, 0.12, 0.045))

def uv(name, loc, scale, material, segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.shade_smooth()
    o.data.materials.append(material)
    return o

def cone(name, loc, radius1, radius2, depth, material):
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=radius1, radius2=radius2, depth=depth, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(material)
    return o

# ---------- Ground / simple colorful forest ----------
bpy.ops.mesh.primitive_plane_add(size=200, location=(0,0,0))
ground=bpy.context.object; ground.name="Soft green forest floor"; ground.data.materials.append(green)
# rolling hills and stylized trees in background
for x,y,s in [(-5,3,1.3),(-3,5,1.0),(4,4,1.4),(6,2,1.0),(-7,1,1.1)]:
    cone("Tree trunk", (x,y,1.0*s), .22*s, .16*s, 2*s, trunkmat)
    uv("Round leafy crown", (x,y,2.2*s), (1.0*s,0.85*s,1.0*s), green2)
    uv("Leaf highlight", (x-.25*s,y-.08,2.55*s), (.52*s,.45*s,.52*s), green)
# flowers
for x,y,c in [(-2.5,-.4,yellow),(3,-.2,teal),(-4,-1,yellow),(4.2,1,yellow)]:
    uv("Flower center", (x,y,.13), (.10,.10,.10), c)
    for a in range(5):
        ang=a*2*math.pi/5
        uv("Flower petal", (x+.18*math.cos(ang),y+.18*math.sin(ang),.13),(.12,.09,.08),white)

# ---------- Lion cub character ----------
# local character centered around x=-1.2 initially
root = bpy.data.objects.new("LAITH | animated root", None)
bpy.context.collection.objects.link(root)
parts=[]
def part(o, parent=root):
    o.parent=parent
    parts.append(o)
    return o

# Body and belly
part(uv("Laith body", (0,0,1.05), (.62,.43,.70), gold))
part(uv("Laith belly", (0,-.35,1.0), (.38,.13,.48), cream))
# head / cheeks / ears
part(uv("Laith head", (0,-.02,2.05), (.70,.53,.66), light_gold))
for x in [-.53,.53]:
    part(uv("Ear outer", (x,-.02,2.55), (.25,.20,.27), gold))
    part(uv("Ear inner", (x,-.19,2.56), (.14,.07,.15), cream))
# muzzle, nose, eyes
for x in [-.20,.20]:
    part(uv("Muzzle puff", (x,-.50,1.88), (.25,.16,.19), cream))
part(uv("Tiny nose", (0,-.65,1.98), (.12,.07,.085), brown))
for x in [-.25,.25]:
    part(uv("Big friendly eye", (x,-.49,2.20), (.15,.075,.20), white))
    part(uv("Pupil", (x,-.558,2.19), (.085,.045,.125), dark))
    part(uv("Eye sparkle", (x-.025,-.60,2.24), (.035,.02,.045), white))
# smile curve
curve=bpy.data.curves.new("Happy little smile","CURVE"); curve.dimensions='3D'; curve.bevel_depth=.018; curve.bevel_resolution=3
spl=curve.splines.new('POLY'); spl.points.add(12)
for i,p in enumerate(spl.points):
    t=i/12
    p.co=(-.20+.40*t,-.64,1.78+0.10*math.sin(math.pi*t),1)
sm=bpy.data.objects.new("Laith smile",curve); bpy.context.collection.objects.link(sm); sm.data.materials.append(brown); sm.parent=root; parts.append(sm)
# legs as spheres/capsules, parented so root bob animates whole character
legs=[]
for x in [-.36,.36]:
    for y in [-.18,.22]:
        leg=uv("Little paw", (x,y,.42), (.19,.20,.34), gold)
        part(leg); legs.append(leg)
# tail curve
tailcurve=bpy.data.curves.new("Curly tail","CURVE"); tailcurve.dimensions='3D'; tailcurve.bevel_depth=.07; tailcurve.bevel_resolution=4
sp=tailcurve.splines.new('BEZIER'); sp.bezier_points.add(2)
for bp,co in zip(sp.bezier_points,[(.48,.12,1.2),(.88,.20,1.48),(1.05,.12,1.70)]):
    bp.co=co; bp.handle_left_type='AUTO'; bp.handle_right_type='AUTO'
tail=bpy.data.objects.new("Laith tail",tailcurve); bpy.context.collection.objects.link(tail); tail.data.materials.append(gold); tail.parent=root; parts.append(tail)
part(uv("Tail tuft", (1.05,.12,1.70),(.14,.13,.20),brown))
# teal scarf, visible triangular-ish scarf via scaled sphere and small emblem
part(uv("Blue teal scarf", (0,-.49,1.55),(.48,.13,.18),teal))
part(uv("Golden paw badge", (0,-.615,1.55),(.095,.035,.095),yellow))

# root starting point and orientation
root.location=(-1.2,0,0)
root.rotation_euler[2]=math.radians(-7)

# Map prop on ground ahead of character
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.05,-.25,.08))
mapobj=bpy.context.object; mapobj.name="Rolled treasure map"; mapobj.dimensions=(.72,.42,.08); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); mapobj.data.materials.append(mapmat)
mapobj.rotation_euler[2]=math.radians(-18)
# little dark map markings
for x,y in [(0.92,-.25),(1.04,-.28),(1.15,-.22)]:
    uv("Map ink mark",(x,y,.13),(.035,.018,.012),ink)

# ---------- Camera and lighting ----------
bpy.ops.object.camera_add(location=(0,-9,4.2))
cam=bpy.context.object; cam.name="Camera | storybook shot"
target=Vector((0,0,1.25))
direction=target- cam.location
cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
cam.data.lens=42
bpy.context.scene.camera=cam

bpy.ops.object.light_add(type='AREA', location=(-3,-4,7))
key=bpy.context.object; key.name="Warm softbox"; key.data.energy=850; key.data.shape='DISK'; key.data.size=5
key.rotation_euler=(math.radians(25),0,math.radians(-25))
bpy.ops.object.light_add(type='AREA', location=(4,1,5))
fill=bpy.context.object; fill.name="Sky fill"; fill.data.energy=500; fill.data.size=4
fill.rotation_euler=(math.radians(20),0,math.radians(145))

scene=bpy.context.scene
scene.render.engine='CYCLES' if 'CYCLES' in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items.keys() else 'BLENDER_EEVEE_NEXT'
scene.cycles.samples=16 if scene.render.engine=='CYCLES' else 16
scene.world.color=(0.30,0.30,0.30)
scene.render.resolution_x=1080
scene.render.resolution_y=1920
scene.render.resolution_percentage=50  # quick preview; set to 100 for final
scene.render.fps=24
scene.frame_start=1
scene.frame_end=240 # 10 seconds

# Animate walk-in, pause, look down, and little happy bounce.
def keyframe(obj, frame, loc=None, rot=None):
    if loc is not None:
        obj.location=loc; obj.keyframe_insert(data_path="location", frame=frame)
    if rot is not None:
        obj.rotation_euler=rot; obj.keyframe_insert(data_path="rotation_euler", frame=frame)

start=(-1.7,0,0)
mid=(-.65,0,0)
end=(-.52,0,0)
keyframe(root,1,start, (0,0,math.radians(-8)))
keyframe(root,72,mid,(0,0,math.radians(0)))
keyframe(root,120,mid,(0,0,math.radians(0)))
keyframe(root,160,end,(0,0,math.radians(5)))
keyframe(root,200,end,(0,0,math.radians(-3)))
keyframe(root,240,end,(0,0,math.radians(0)))
# whole character subtle bob
for f,z in [(1,0),(18,.07),(36,0),(54,.07),(72,0),(120,0),(150,.04),(180,0),(210,.05),(240,0)]:
    root.location.z=z
    root.keyframe_insert(data_path="location", frame=f, index=2)
# map glint / small lift at discovery
mapobj.keyframe_insert(data_path="location",frame=1)
mapobj.location.z=.18; mapobj.keyframe_insert(data_path="location",frame=145)
mapobj.location.z=.08; mapobj.keyframe_insert(data_path="location",frame=180)

# Set interpolation to smooth
for obj in bpy.data.objects:
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation='BEZIER'

scene.render.image_settings.file_format='FFMPEG'
scene.render.ffmpeg.format='MPEG4'
scene.render.ffmpeg.codec='H264'
scene.render.filepath=os.path.join(OUT,"laith_scene.mp4")
scene.render.image_settings.color_mode='RGB'
scene.view_settings.view_transform='Standard'
scene.render.film_transparent=False
scene.camera.data.dof.use_dof=False

# Save project and render animation
blendpath=os.path.join(OUT,"laith_scene.blend")
bpy.ops.wm.save_as_mainfile(filepath=blendpath)
bpy.ops.render.render(animation=True)
print("Done. Video:", scene.render.filepath)
