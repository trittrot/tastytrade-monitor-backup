with open('spy_term_structure_alert.py', 'r') as f:
    content = f.read()

old_line = "            lines.append('Slope forecast (' + str(slopeFcst) + ') is BELOW current slope (' + str(slope) + ') - ORATS model expects skew to flatten, historically favors collar strategies per University 203')"

new_addition = """            lines.append('Slope forecast (' + str(slopeFcst) + ') is BELOW current slope (' + str(slope) + ') - ORATS model expects skew to flatten, historically favors collar strategies per University 203')

    slopeInf = data.get('slopeInf')
    if slope is not None and slopeInf is not None and slope != '' and slopeInf != '':
        if slopeInf > slope:
            lines.append('Slope (near-term, ' + str(slope) + ') vs slopeInf (long-dated, ' + str(slopeInf) + '): long-dated skew is steeper. Per general options market convention (not ORATS-specific), near-term skew is normally the steeper of the two - this inverted pattern can indicate acute near-term fear has eased while longer-horizon uncertainty remains relatively elevated')
        else:
            lines.append('Slope (near-term, ' + str(slope) + ') vs slopeInf (long-dated, ' + str(slopeInf) + '): near-term skew is steeper, the normal/typical relationship per general options market convention, consistent with acute near-term risk being priced higher than longer-horizon risk')"""

if old_line not in content:
    print("ERROR: target line not found, no changes made")
else:
    content = content.replace(old_line, new_addition)
    with open('spy_term_structure_alert.py', 'w') as f:
        f.write(content)
    print("slopeInf commentary added successfully")
