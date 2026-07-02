import os

svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="100%">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#4F46E5;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#10B981;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#059669;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#F59E0B;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#D97706;stop-opacity:1" />
        </linearGradient>
    </defs>
    
    <!-- Background -->
    <rect width="800" height="400" fill="#f8fafc" rx="8" />
    
    <!-- Title -->
    <text x="400" y="50" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#1e293b" text-anchor="middle">Candidate Ranking Pipeline Funnel</text>
    
    <!-- Step 1: 100K -->
    <rect x="50" y="100" width="700" height="60" fill="url(#grad1)" rx="8" />
    <text x="400" y="138" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">1. Initial Pool: 100,000 Candidates</text>
    
    <!-- Arrow 1 -->
    <polygon points="380,170 420,170 400,195" fill="#94a3b8" />
    
    <!-- Step 2: 1.5K -->
    <rect x="150" y="205" width="500" height="60" fill="url(#grad2)" rx="8" />
    <text x="400" y="243" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">2. Stage 1 Retrieval: 1,500 Candidates</text>
    <text x="400" y="275" font-family="Arial, sans-serif" font-size="14" fill="#475569" text-anchor="middle">Honeypots removed, fast term-matching heuristic applied</text>

    <!-- Arrow 2 -->
    <polygon points="380,285 420,285 400,310" fill="#94a3b8" />
    
    <!-- Step 3: 100 -->
    <rect x="250" y="320" width="300" height="60" fill="url(#grad3)" rx="8" />
    <text x="400" y="358" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">3. Final Top 100 Ranked</text>
    <text x="400" y="390" font-family="Arial, sans-serif" font-size="14" fill="#475569" text-anchor="middle">100-point multi-dimensional re-scoring</text>
</svg>
"""

with open("pipeline_funnel.svg", "w") as f:
    f.write(svg_content)

print("Created pipeline_funnel.svg")
