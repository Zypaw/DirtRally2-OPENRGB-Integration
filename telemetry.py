import socket, struct, time
# port & ip
HOST='0.0.0.0'
PORT=20777
# gear map

GEAR={0.:'N', 1.:'1', 2.:'2', 3.:'3', 4.:'4', 5.:'5', 6.:'6', 7.:'7', 8.:'8', 9.:'9', 10.:'R'}
# position of f64
POS_GEAR=33
POS_RPM_MAX=63
POS_RPM_CURR=37
POS_V=7

RETRY_MAX=15
BUFF_SIZE=512


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
                print(len(b))
                # receieved, process em'
                info = struct.unpack('64f', b[:256])
                try:
                    print(f"GEAR : {GEAR[info[POS_GEAR]]}, POWER : {info[POS_RPM_CURR]*100./info[POS_RPM_MAX]}, RPMS : {info[POS_RPM_CURR]} ,MAX_RPMS : {info[POS_RPM_MAX]}, SPEED : {info[POS_V]*3.6}")
                except:
                    print(f"GEAR : {GEAR[info[POS_GEAR]]}, POWER : {info[POS_RPM_CURR]*100./info[POS_RPM_MAX]}, RPMS : {info[POS_RPM_CURR]} ,MAX_RPMS : {info[POS_RPM_MAX]}, SPEED : {info[POS_V]*3.6}")
            else:
                # broken sock, fallback and reconnect
                raise Exception('broken sock')
    except Exception as E:
        print(E, ', retry %d'%i)
        time.sleep(1)
