from opensimplex import OpenSimplex
from PIL import Image
import random
import time

# -------------------------
# Map parameters
# -------------------------
WIDTH, HEIGHT = 32, 32     # size of the tilemap
ZOOM = 10                  # how much to scale up for viewing

# -------------------------
# Random seed setup
# -------------------------
SEED = int(time.time() * 1000) % 1000000  # current time in ms, makes a new map each run
noise_gen = OpenSimplex(seed=SEED)
print(f"Seed used for this map: {SEED}")

# -------------------------
# Create a new image
# -------------------------
img = Image.new("RGB", (WIDTH, HEIGHT))

for y in range(HEIGHT):
    for x in range(WIDTH):
        # Base terrain noise
        height_noise = noise_gen.noise2(x / 5.0, y / 5.0)
        normalized_height = (height_noise + 1) / 2  # normalize to 0..1

        # Simple rivers
        river_noise = noise_gen.noise2(x / 10.0, y / 10.0)
        is_river = abs(river_noise) < 0.08

        # Determine tile color based on terrain
        if is_river:
            tile_color = (0, 120, 255)            # blue river
        elif normalized_height < 0.3:
            tile_color = (0, 0, 150 + int(normalized_height * 50))  # deep water
        elif normalized_height < 0.5:
            tile_color = (0, int(normalized_height * 255), 0)       # grass
        elif normalized_height < 0.7:
            tile_color = (100, 50, 0)             # hills
        elif normalized_height < 0.85:
            tile_color = (200, 200, 0)            # sand/plateau
        else:
            tile_color = (255, 255, 255)          # snowy peaks

        # Tiny random lava spots
        if random.random() < 0.01:
            tile_color = (255, 50, 0)

        img.putpixel((x, y), tile_color)

# -------------------------
# Scale up for easier viewing
# -------------------------
img = img.resize((WIDTH * ZOOM, HEIGHT * ZOOM), resample=Image.NEAREST)

# -------------------------
# Save output
# -------------------------
img.save("fun_tilemap.png")
print("Map generated: fun_tilemap.png")