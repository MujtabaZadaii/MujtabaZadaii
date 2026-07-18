import math
from PIL import Image

def generate_dot_svg(input_path, output_path, grid_size=80, dot_spacing=10, max_radius=4.5):
    # Open image and convert to RGBA
    img = Image.open(input_path).convert("RGBA")
    
    # Calculate aspect ratio and crop to center square
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) / 2
    top = (h - min_dim) / 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    
    # Resize to grid size
    img = img.resize((grid_size, grid_size), Image.Resampling.LANCZOS)
    pixels = img.load()
    
    svg_width = grid_size * dot_spacing
    svg_height = grid_size * dot_spacing
    
    # Center of the grid for distance calculation
    cx, cy = grid_size / 2, grid_size / 2
    max_dist = math.sqrt(cx**2 + cy**2)
    
    svg_content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
        '  <defs>',
        '    <style>',
        '      .dot { animation: pulse 3s infinite; transform-origin: center; }',
        '      @keyframes pulse { 0% { opacity: 0.8; transform: scale(0.9); } 50% { opacity: 1; transform: scale(1.1); } 100% { opacity: 0.8; transform: scale(0.9); } }',
        '    </style>',
        '  </defs>',
        '  <rect width="100%" height="100%" fill="transparent" />',
        '  <g transform="translate(5, 5)">'
    ]
    
    for y in range(grid_size):
        for x in range(grid_size):
            r, g, b, a = pixels[x, y]
            if a < 10:
                continue # Skip fully transparent pixels
            
            # Mask to circle
            dist_to_center = math.sqrt((x - cx)**2 + (y - cy)**2)
            if dist_to_center > cx:
                continue
                
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Calculate delay based on distance to center for a ripple effect
            delay = (dist_to_center / max_dist) * 2.0  # 0 to 2 seconds
            
            # Use SVG animate to avoid heavy CSS calculation on thousands of nodes, 
            # and it works better in GitHub markdown.
            dot_x = x * dot_spacing
            dot_y = y * dot_spacing
            
            svg_content.append(
                f'    <circle cx="{dot_x}" cy="{dot_y}" r="{max_radius}" fill="{hex_color}">'
                f'<animate attributeName="r" values="{max_radius * 0.7}; {max_radius * 1.2}; {max_radius * 0.7}" '
                f'dur="3s" begin="{delay:.2f}s" repeatCount="indefinite" />'
                f'</circle>'
            )

    svg_content.append('  </g>')
    svg_content.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_content))

if __name__ == "__main__":
    generate_dot_svg("mujtaba.png", "assets/readme/mujtaba-dots.svg", grid_size=70, dot_spacing=12, max_radius=5.5)
    print("Generated mujtaba-dots.svg")
