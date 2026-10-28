# Kids Cartoon Starter — Laith's first scene

This starter creates a simple, original, stylized 3D lion cub scene in Blender and renders a 10-second vertical MP4 preview.

## Requirements
- Blender 4.x installed on your server or workstation.
- Enough memory for Blender. This starter uses simple geometry; it does not require an AI video API.
- Arabic voice-over is not included yet; add it after approving the character look.

## Run
From this folder, run:

```bash
blender -b -P create_scene.py
```

Output files are created in `renders/`:
- `laith_scene.blend` — editable Blender project
- `laith_scene.mp4` — 10-second preview (50% resolution for speed)

For final quality, change `scene.render.resolution_percentage=50` to `100` in `create_scene.py`.
Rendering performance depends on your server and Blender build.

## Scene beats
- 0–3 seconds: Laith walks into the shot.
- 3–6 seconds: he notices the map.
- 6–10 seconds: he pauses and reacts with curiosity.

## Important
This is a low-cost prototype made from procedural shapes, not a finished studio-quality character. It is meant to validate the pipeline first. The next iteration should improve rigged walking, facial animation, forest detail, and Egyptian Arabic voice-over.
