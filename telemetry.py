import socket, struct, time
# port & ip
HOST='localhost'
PORT=10001
# gear map

GEAR={0.:'N', 1.:'1', 2.:'2', 3.:'3', 4.:'4', 5.:'5', 6.:'6', 7.:'7', 8.:'8', 9.:'9', 10.:'R'}
# position of f64
POS_GEAR=33
POS_RPM_MAX=63
POS_RPM_CURR=37
POS_V=7

RETRY_MAX=15
BUFF_SIZE=264


from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, ZoneType

cli = OpenRGBClient()
cli.clear()
led = cli.get_devices_by_name("WLED")[0]


for i in range(RETRY_MAX):
    # the fallback loop
    try:
        # start to subscribe telemetry
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((HOST, PORT))
        # read loop
        while True:
            b = sock.recv(BUFF_SIZE)
            if b:
                # receieved, process em'
                info = struct.unpack('64f', b[:256])
                try:
                    ratio = (6.5/8)
                    if info[POS_RPM_CURR] >= ratio*(info[POS_RPM_MAX]-50) and POS_RPM_CURR != 0:
                        count = (info[POS_RPM_CURR]-ratio*info[POS_RPM_MAX])/(info[POS_RPM_MAX]-ratio*info[POS_RPM_MAX])*17
                        led.zones[0].set_color(RGBColor(0,0,0),fast=True)
                        if int(count) > 15:
                            count = 15.01
                        if int(count) > 2:
                            green = [RGBColor(0, 255, 0)] * 2
                        else:
                            green = [RGBColor(0, 0, 0)]
                        if int(count) > 5:
                            yellow = [RGBColor(180, 180, 0)] * 5
                        else:
                            if int(count) > 2:
                                yellow = [RGBColor(180, 180, 0)] * int(count)
                            else:
                                yellow = [RGBColor(0, 0, 0)]
                        if int(count) > 7:
                            red = [RGBColor(255, 0, 0)] * (int(count)-7)
                        else:
                            red = [RGBColor(0, 0, 0)]
                        remaining_leds = 15 - len(red) - len(yellow) - len(green)
                        led.zones[0].set_colors(green + yellow + red + [RGBColor(0, 0, 0)] * (remaining_leds*2)+ red + yellow + green,fast=True)
                    else:
                        led.zones[0].set_color(RGBColor(0,0,0),fast=True)
                    print(f"GEAR : {GEAR[info[POS_GEAR]]}, POWER : {int(info[POS_RPM_CURR]*100./info[POS_RPM_MAX])}, RPMS : {int(info[POS_RPM_CURR])} ,MAX_RPMS : {int(info[POS_RPM_MAX])}, SPEED : {info[POS_V]*3.6}")
                except Exception as E:
                    print(E)
            else:
                # broken sock, fallback and reconnect
                raise Exception('broken sock')
            # time.sleep(0.1)
    except Exception as E:
        print(E, ', retry %d'%i)
        time.sleep(1)
