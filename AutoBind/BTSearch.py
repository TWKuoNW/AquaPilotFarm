import bluetooth

print("Searching for nearby Bluetooth devices...")

nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=8, flush_cache=True)

print("Found {} devices.".format(len(nearby_devices)))

for addr, name in nearby_devices:
    try:
        print("  Address: {} - Name: {}".format(addr, name))
    except UnicodeEncodeError:
        print("  Address: {} - Name: {}".format(addr, name.encode('utf-8', 'replace')))
