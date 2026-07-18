import urllib.request
import re
import os

url = "https://github-readme-stats.shion.dev/api?username=mujtabazadaii&theme=radical&hide_border=false&include_all_commits=true&count_private=true&show_icons=true"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as response:
        svg_content = response.read().decode('utf-8')
        
        # Replace grades with A+
        svg_content = svg_content.replace('C+', 'A+')
        svg_content = svg_content.replace('>C<', '>A+<')
        svg_content = svg_content.replace('>B+<', '>A+<')
        svg_content = svg_content.replace('>B<', '>A+<')
        svg_content = svg_content.replace('>A<', '>A+<')
        
        # Override the rank color to a glowing cyan/blue to match our premium theme
        style_override = """
        <style>
            .rank-circle-rim { stroke: #0ea5e9 !important; }
            .rank-circle { stroke: #0ea5e9 !important; stroke-dasharray: 240, 251.3 !important; }
            .rank-text { fill: #0ea5e9 !important; font-weight: bold !important; text-shadow: 0 0 5px rgba(14, 165, 233, 0.5) !important; }
        </style>
        """
        if '</style>' in svg_content:
            svg_content = svg_content.replace('</style>', '</style>' + style_override)
        else:
            svg_content = svg_content.replace('</svg>', style_override + '</svg>')
            
        # We can also add a subtle glow filter to the rank circle for that "buhut ziyada professional" look!
        glow_filter = """
        <filter id="rankGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        """
        svg_content = svg_content.replace('<defs>', '<defs>' + glow_filter)
        svg_content = svg_content.replace('class="rank-circle-rim"', 'class="rank-circle-rim" filter="url(#rankGlow)"')

        os.makedirs("assets/readme", exist_ok=True)
        with open("assets/readme/stats.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        print("Successfully spoofed stats to A+ and saved to assets/readme/stats.svg")
except Exception as e:
    print(f"Error fetching stats: {e}")
