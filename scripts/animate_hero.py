import re

with open("assets/readme/hero.svg", "r", encoding="utf-8") as f:
    svg_content = f.read()

# We need to add clip paths to the <defs> section.
# We have 9 lines of code. We will create 9 clipPaths, each revealing sequentially, and then erasing in reverse.
total_dur = 15  # seconds
num_lines = 9

# We allocate 40% of the time for typing down (0 to 0.4)
# 20% waiting at full (0.4 to 0.6)
# 40% of the time for erasing up (0.6 to 1.0)
# So each line gets 0.4 / 9 = 0.044 fraction of time for typing
# And same for erasing.

defs_addition = ""
for i in range(num_lines):
    # Typing phase: starts at i * time_per_line, ends at (i+1) * time_per_line
    type_start = (i / num_lines) * 0.4
    type_end = ((i + 1) / num_lines) * 0.4
    
    # Erasing phase: starts at 0.6 + (num_lines - i - 1) * time_per_line, ends at 0.6 + (num_lines - i) * time_per_line
    erase_start = 0.6 + ((num_lines - i - 1) / num_lines) * 0.4
    erase_end = 0.6 + ((num_lines - i) / num_lines) * 0.4
    
    # Values: 0 -> 0 -> 340 -> 340 -> 0 -> 0
    # keyTimes: 0 -> type_start -> type_end -> erase_start -> erase_end -> 1.0
    values = "0; 0; 340; 340; 0; 0"
    keyTimes = f"0; {type_start:.3f}; {type_end:.3f}; {erase_start:.3f}; {erase_end:.3f}; 1"
    
    y_pos = (i * 30) - 15
    clip_path = f'''
    <clipPath id="clip-line-{i}">
      <rect x="-10" y="{y_pos}" width="0" height="30">
        <animate attributeName="width" values="{values}" keyTimes="{keyTimes}" dur="{total_dur}s" repeatCount="indefinite" />
      </rect>
    </clipPath>'''
    defs_addition += clip_path

# Insert defs addition into the SVG
if "clip-line-0" not in svg_content:
    svg_content = svg_content.replace('</defs>', defs_addition + '\n  </defs>')

# Now we need to apply these clip paths to the individual text elements in the code block.
# We will find the <g> that contains the code lines and apply clip-path attributes.
# The code block looks like:
# <g transform="translate(30, 40)" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" fill="#a3a3a3">
#   <text x="0" y="0">...</text>
#   ...
# </g>

# Let's extract the code block lines
text_matches = re.finditer(r'<text x="\d+" y="(\d+)">(.*?)</text>', svg_content)
line_idx = 0
for match in text_matches:
    full_tag = match.group(0)
    y_val = match.group(1)
    # the code block text lines have y values 0, 30, 60, ..., 240
    if y_val in [str(i*30) for i in range(num_lines)]:
        # replace the text tag with one having clip-path
        # only if it doesn't already have one
        if "clip-path" not in full_tag:
            new_tag = full_tag.replace('<text', f'<text clip-path="url(#clip-line-{line_idx})"')
            svg_content = svg_content.replace(full_tag, new_tag)
            line_idx += 1

# Let's also animate the blinking cursor!
# It should follow the text. This is hard to do with pure SVG without complex math.
# But we can just make the blinking cursor animate its 'x' and 'y' properties to follow the typing, OR 
# we can just hide the cursor and let the typing effect be the star, or keep the cursor fixed at the end.
# If we want a realistic cursor, it's easier to just let the clip-path do the work.

with open("assets/readme/hero.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("SVG animation updated!")
