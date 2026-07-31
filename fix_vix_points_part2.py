with open('vix_live_monitor.py', 'r') as f:
    content = f.read()

old_down = """DOWN_MESSAGES = {
    10: "VIX -10% from open - vol cooling, monitor long premium positions",
    15: "VIX -15% from open - review long premium/hedge positions",
    20: "VIX -20% from open - consider whether long hedge still needed",
    25: "VIX -25% from open - significant vol collapse, reassess hedge",
    30: "VIX -30% from open - major vol collapse, review hedge urgently",
}"""

new_down = """DOWN_MESSAGES = {
    3: "VIX -3 points from close - approx 1 standard deviation move, vol cooling, monitor long premium positions",
    5: "VIX -5 points from close - approx 2 standard deviation move, review long premium/hedge positions",
    8: "VIX -8 points from close - significant vol collapse, reassess hedge",
    15: "VIX -15 points from close - approx 3 standard deviation move, major vol collapse, review hedge urgently",
}"""

if old_down not in content:
    print("ERROR: DOWN_MESSAGES block not found")
else:
    content = content.replace(old_down, new_down)
    with open('vix_live_monitor.py', 'w') as f:
        f.write(content)
    print("DOWN_MESSAGES updated")
