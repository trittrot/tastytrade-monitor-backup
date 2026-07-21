with open('spy_term_structure_alert.py', 'r') as f:
    content = f.read()

old_line = "    lines.append('ivPctile1y: ' + str(data.get('ivPctile1y','')))"

new_block = """    lines.append('ivPctile1y: ' + str(data.get('ivPctile1y','')))
    lines.append('ivRank1m: ' + str(data.get('ivRank1m','')) + '  ivPct1m: ' + str(data.get('ivPct1m','')))
    lines.append('ivRank1y: ' + str(data.get('ivRank1y','')) + '  ivPct1y: ' + str(data.get('ivPct1y','')))"""

if old_line not in content:
    print("ERROR: target line not found, no changes made")
else:
    content = content.replace(old_line, new_block)
    with open('spy_term_structure_alert.py', 'w') as f:
        f.write(content)
    print("IV Rank added to email body successfully")
