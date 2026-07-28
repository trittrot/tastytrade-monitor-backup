with open('etf_iv_percentile_alert.py', 'r') as f:
    content = f.read()

old_block = """        except Exception as e:
            print('Check error: ' + str(e))
            send_alert('Tastytrade monitor: ETF IV percentile check FAILED - ' + str(e))"""

new_block = """        except Exception as e:
            print('Check error: ' + str(e))
            if not failure_alerted_today:
                send_alert('Tastytrade monitor: ETF IV percentile check FAILED - ' + str(e))
                failure_alerted_today = True
            else:
                print('Suppressing repeat failure alert - already notified today')"""

if old_block not in content:
    print("ERROR: block not found")
else:
    content = content.replace(old_block, new_block)
    with open('etf_iv_percentile_alert.py', 'w') as f:
        f.write(content)
    print("Failure alert suppression added")
