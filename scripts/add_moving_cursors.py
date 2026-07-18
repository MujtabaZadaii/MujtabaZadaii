import re

with open("assets/readme/hero.svg", "r", encoding="utf-8") as f:
    svg_content = f.read()

# First, remove the original blinking cursor
svg_content = re.sub(r'<!-- Blinking cursor -->.*?</rect>', '', svg_content, flags=re.DOTALL)

# Let's extract the text lines to guess their widths
# We can estimate width by character count * 8.5 (for font-size 14 monospace)
text_matches = list(re.finditer(r'<text x="(\d+)" y="(\d+)"(?: clip-path="[^"]*")?>(.*?)</text>', svg_content))

num_lines = 9
total_dur = 15

cursors_xml = "<!-- Animated Cursors -->\n"

for i in range(num_lines):
    # Timings
    type_start = (i / num_lines) * 0.4
    type_end = ((i + 1) / num_lines) * 0.4
    erase_start = 0.6 + ((num_lines - i - 1) / num_lines) * 0.4
    erase_end = 0.6 + ((num_lines - i) / num_lines) * 0.4
    
    if i < len(text_matches):
        match = text_matches[i]
        start_x = int(match.group(1))
        y_val = int(match.group(2))
        
        # Clean text from tags to get pure string length
        raw_text = re.sub(r'<[^>]+>', '', match.group(3))
        # Estimate end_x: start_x + (char_count * 8.5)
        end_x = int(start_x + (len(raw_text) * 8.5))
        
        # Cursor X animation
        x_values = f"{start_x}; {start_x}; {end_x}; {end_x}; {start_x}; {start_x}"
        keyTimes = f"0; {type_start:.3f}; {type_end:.3f}; {erase_start:.3f}; {erase_end:.3f}; 1"
        
        # Cursor Opacity animation
        # We only want it visible during its turn.
        # But wait, when the typing is paused (between 0.4 and 0.6), the LAST line (Line 8) should have a blinking cursor!
        # And when it's idle (before 0 or after 1), Line 0 should be visible? No, it's looping.
        # Actually, it's easier to just show the cursor for line i from `type_start` to `erase_end`?
        # If we show it from `type_start` to `type_end` (typing), and `erase_start` to `erase_end` (erasing), what about the pause?
        # During the pause (0.4 to 0.6), line 8 is fully typed. Its cursor should be visible.
        # So visibility:
        # If i < num_lines - 1: visible from `type_start` to `type_end`, and `erase_start` to `erase_end`.
        # If i == num_lines - 1: visible from `type_start` to `erase_end`.
        
        if i == num_lines - 1:
            op_values = "0; 0; 1; 1; 0; 0"
            op_keyTimes = f"0; {type_start - 0.001:.3f}; {type_start:.3f}; {erase_end:.3f}; {erase_end + 0.001:.3f}; 1"
        else:
            op_values = "0; 0; 1; 0; 0; 1; 0; 0"
            op_keyTimes = f"0; {type_start - 0.001:.3f}; {type_start:.3f}; {type_end:.3f}; {erase_start - 0.001:.3f}; {erase_start:.3f}; {erase_end:.3f}; 1"
            
        cursor_y = y_val - 12
        
        cursor_xml = f'''
    <rect x="{start_x}" y="{cursor_y}" width="8" height="16" fill="#0ea5e9" opacity="0">
      <animate attributeName="x" values="{x_values}" keyTimes="{keyTimes}" dur="{total_dur}s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="{op_values}" keyTimes="{op_keyTimes}" dur="{total_dur}s" repeatCount="indefinite" />
    </rect>'''
        cursors_xml += cursor_xml

# Insert cursors inside the group
# Find the end of the code block group
# <text x="0" y="240"...};</text>\n    </g>
svg_content = re.sub(r'(};</text>\n\s*)</g>', r'\1' + cursors_xml + '\n    </g>', svg_content)

with open("assets/readme/hero.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Added animated cursors that follow the text!")
