import math
from PIL import Image, ImageDraw

def generate_dot_gif(input_path, output_path, grid_size=70, dot_spacing=12, max_radius=5.5, frames=30, fps=15):
    # Open image and convert to RGBA
    img = Image.open(input_path).convert("RGBA")
    
    # Crop to center square
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) / 2
    top = (h - min_dim) / 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    
    # Resize to grid
    img = img.resize((grid_size, grid_size), Image.Resampling.LANCZOS)
    pixels = img.load()
    
    gif_width = grid_size * dot_spacing
    gif_height = grid_size * dot_spacing
    
    cx, cy = grid_size / 2, grid_size / 2
    max_dist = math.sqrt(cx**2 + cy**2)
    
    output_frames = []
    
    for f_idx in range(frames):
        # Create a new frame with dark transparent or solid background
        # GitHub uses different backgrounds, but let's use a solid dark background for the gif
        # Or transparent? GIF supports 1-bit transparency, which can be jagged. 
        # Since our hero is #0a0a0a, let's use that as the background color!
        frame = Image.new("RGBA", (gif_width, gif_height), "#0a0a0a")
        draw = ImageDraw.Draw(frame)
        
        # Calculate time progress 0 to 1
        t = f_idx / frames
        
        for y in range(grid_size):
            for x in range(grid_size):
                r, g, b, a = pixels[x, y]
                if a < 10:
                    continue
                
                dist_to_center = math.sqrt((x - cx)**2 + (y - cy)**2)
                if dist_to_center > cx:
                    continue
                
                # Ripple animation logic
                # Delay based on distance
                delay = (dist_to_center / max_dist)
                
                # We want a wave that loops. 
                # phase = time - delay. Wave formula: sin(phase * 2 * pi)
                phase = t - delay
                wave = math.sin(phase * math.pi * 2) # ranges from -1 to 1
                
                # Map wave to radius multiplier: 0.6 to 1.0
                radius_mult = 0.8 + 0.2 * wave
                current_radius = max_radius * radius_mult
                
                dot_x = x * dot_spacing + 5
                dot_y = y * dot_spacing + 5
                
                left_c = dot_x - current_radius
                top_c = dot_y - current_radius
                right_c = dot_x + current_radius
                bottom_c = dot_y + current_radius
                
                draw.ellipse([left_c, top_c, right_c, bottom_c], fill=(r, g, b, 255))
        
        output_frames.append(frame)
        
    output_frames[0].save(
        output_path,
        save_all=True,
        append_images=output_frames[1:],
        duration=int(1000/fps),
        loop=0
    )

if __name__ == "__main__":
    generate_dot_gif("mujtaba.png", "assets/readme/mujtaba-animated.gif", grid_size=50, dot_spacing=12, max_radius=5.5, frames=30, fps=15)
    print("Generated mujtaba-animated.gif")
