with open('vix_live_monitor.py', 'r') as f:
    content = f.read()

old_thresholds = "THRESHOLDS = [10, 15, 20, 25, 30]"
new_thresholds = "THRESHOLDS = [3, 5, 8, 15]"

if old_thresholds not in content:
    print("ERROR: THRESHOLDS line not found")
else:
    content = content.replace(old_thresholds, new_thresholds)
    print("THRESHOLDS updated to point values")

old_up = """UP_MESSAGES = {
    10: "VIX +10% from open - review existing short premium positions",
    15: "VIX +15% from open - consider adjustments to short premium positions",
    20: "VIX +20% from open - consider new short premium entries (check ORATS)",
    25: "VIX +25% from open - significant vol event, scan ORATS for opportunities",
    30: "VIX +30% from open - major vol event, review book thoroughly",
}"""

new_up = """UP_MESSAGES = {
    3: "VIX +3 points from close - approx 1 standard deviation move, review existing short premium positions",
    5: "VIX +5 points from close - approx 2 standard deviation move, consider adjustments to short premium positions",
    8: "VIX +8 points from close - significant vol event, close all watertight doors, review book thoroughly",
    15: "VIX +15 points from close - approx 3 standard deviation move, major vol event",
}"""

if old_up not in content:
    print("ERROR: UP_MESSAGES block not found")
else:
    content = content.replace(old_up, new_up)
    print("UP_MESSAGES updated")

with open('vix_live_monitor.py', 'w') as f:
    f.write(content)
