with open('spy_term_structure_alert.py', 'r') as f:
    content = f.read()

old_block = """                lines.append('Forward ratio ' + label + ': ' + str(val) + ' - notable divergence from 1.0, per ORATS this has historically foreshadowed larger moves')
            else:
                lines.append('Forward ratio ' + label + ': ' + str(val) + ' - close to 1.0, no anomaly flagged')"""

new_block = """                lines.append('Forward ratio ' + label + ': ' + str(val) + ' - notable divergence from 1.0, per ORATS this has historically foreshadowed larger moves')
            else:
                lines.append('Forward ratio ' + label + ': ' + str(val) + ' - close to 1.0, no anomaly flagged')
            if val > 1.0:
                lines.append('  fbfwd ratio above 1.0: consistent with low-vol regime, historically associated with buying volatility strategies')
            else:
                lines.append('  fbfwd ratio below 1.0: consistent with high-vol regime, historically associated with selling volatility strategies')"""

if old_block not in content:
    print("ERROR: old block not found, no changes made")
else:
    content = content.replace(old_block, new_block)
    with open('spy_term_structure_alert.py', 'w') as f:
        f.write(content)
    print("Regime commentary added successfully")
