import socket, struct, time
# port & ip
HOST='localhost'
PORT=10001

# gear map
GEAR={0.:'N', 1.:'1', 2.:'2', 3.:'3', 4.:'4', 5.:'5', 6.:'6', 7.:'7', 8.:'8', 9.:'9', -1.:'R'}
POS_GEAR=33
POS_RPM_MAX=63
POS_RPM_CURR=37
POS_V=7

RETRY_MAX=15
BUFF_SIZE=512


from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, ZoneType

cli = OpenRGBClient()
cli.clear()
cli.load_profile("DR2")

# cli.clear()
led = cli.get_devices_by_name("WLED")[0]
totals_led = 30

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind((HOST, PORT))


def calculate_colors(rpms, max_rpms):
    ratio = 6.6 / 8
    if rpms >= ratio * max_rpms and rpms > 0.:
        count = (rpms - ratio * max_rpms) / (max_rpms - ratio * max_rpms) * (totals_led/2)
        if count >= 0.85*(totals_led/2):
            return [RGBColor(140, 0, 0)]*totals_led
        else:
            count = min(float(count), totals_led/2+0.1)
            green = [RGBColor(0, 255, 0)] * min(int(count), 2)
            yellow = [RGBColor(190, 190, 0)] * min(int(count) - 2, 5)
            red = [RGBColor(255, 0, 0)] * max(int(count) - 7, 0)
            remaining_leds = int(totals_led/2) - len(red) - len(yellow) - len(green)
            return green + yellow + red + [RGBColor(0, 0, 0)] * (remaining_leds * 2) + red + yellow + green
    else:
        return [RGBColor(0, 0, 0)]*totals_led

while True:
    sock.settimeout(1.0)
    try:
        while True:
            b = sock.recv(BUFF_SIZE)
            if b:
                info = struct.unpack('64f', b[:256])
                rpms = info[POS_RPM_CURR]
                max_rpms = info[POS_RPM_MAX]
                colors = calculate_colors(rpms, max_rpms)
                if info[60]> 1.:
                    if info[1] == 0.:
                        colors = [RGBColor(255,0,0)]*totals_led
                    elif info[1] < 1.:
                        colors = [RGBColor(0,255,0)]*totals_led
                led.zones[0].set_colors(colors, fast=True)
            else:
                raise Exception('broken sock')
    except Exception as e :
        cli.load_profile("DR2")
        time.sleep(1)