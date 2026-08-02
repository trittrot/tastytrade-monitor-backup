with open('vix_live_monitor.py', 'r') as f:
    content = f.read()

old_line = "THRESHOLDS = [3, 5, 8, 15]"

new_block = """THRESHOLDS = [3, 5, 8, 15]

REGIME_THRESHOLDS = {
    'low': [2, 3, 4, 6],
    'normal': [3, 5, 8, 15],
    'elevated': [5, 8, 12, 20],
    'extreme': [8, 12, 18, 25],
}

def get_regime_thresholds(reference_price):
    if reference_price < 15:
        regime = 'low'
    elif reference_price < 25:
        regime = 'normal'
    elif reference_price < 35:
        regime = 'elevated'
    else:
        regime = 'extreme'
    return REGIME_THRESHOLDS[regime], regime"""

if old_line not in content:
    print("ERROR: line not found")
else:
    content = content.replace(old_line, new_block)
    with open('vix_live_monitor.py', 'w') as f:
        f.write(content)
    print("Regime threshold framework added")
