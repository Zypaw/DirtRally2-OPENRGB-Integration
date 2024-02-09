from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, ZoneType

cli = OpenRGBClient()

# finding a linear zone
zone = next(z for dev in cli.ee_devices for z in dev.zones if z.type == ZoneType.LINEAR)
# dividing the color spectrum by number of LEDs in the zone
step = int(360/len(zone.colors))
# Setting the zones colors to the entire spectrum of the rainbow
for i, hue in enumerate(range(0, 360, step)):
    zone.colors[i] = RGBColor.fromHSV(hue, 100, 100)
zone.show()