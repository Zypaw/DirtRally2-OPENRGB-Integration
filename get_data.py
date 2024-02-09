'''
    This script test if your Diry Rally UDP Server has been started properly.
    the steam post of the UDP data format in detail : https://steamcommunity.com/app/310560/discussions/0/481115363869500839/

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    for extradata = 3: output = 64 floats
    byteformat: little endian

    Position Info | Content Info
    No. Byte | Format Value

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
0	Time                   float32 `json:"time"`
1	LapTime                float32 `json:"lapTime"`
2	LapDistance            float32 `json:"lapDistance"`
3	TotalDistance          float32 `json:"distance"`
4	X                      float32 `json:"-"` // World space position
5	Y                      float32 `json:"-"` // World space position
6	Z                      float32 `json:"-"` // World space position
7	Speed                  float32 `json:"speed"`
8	Xv                     float32 `json:"-"` // Velocity in world space
9	Yv                     float32 `json:"-"` // Velocity in world space
10	Zv                     float32 `json:"-"` // Velocity in world space
11	Xr                     float32 `json:"-"` // World space right direction
12	Yr                     float32 `json:"-"` // World space right direction
13	Zr                     float32 `json:"-"` // World space right direction
14	Xd                     float32 `json:"-"` // World space forward direction
15	Yd                     float32 `json:"-"` // World space forward direction
16	Zd                     float32 `json:"-"` // World space forward direction
17	Susp_pos_bl            float32 `json:"-"`
18	Susp_pos_br            float32 `json:"-"`
19	Susp_pos_fl            float32 `json:"-"`
20	Susp_pos_fr            float32 `json:"-"`
21	Susp_vel_bl            float32 `json:"-"`
22	Susp_vel_br            float32 `json:"-"`
23	Susp_vel_fl            float32 `json:"-"`
24	Susp_vel_fr            float32 `json:"-"`
25	Wheel_speed_bl         float32 `json:"-"`
26	Wheel_speed_br         float32 `json:"-"`
27	Wheel_speed_fl         float32 `json:"-"`
28	Wheel_speed_fr         float32 `json:"-"`
29	Throttle               float32 `json:"throttlePosition"`
30	Steer                  float32 `json:"steerPosition"`
31	Brake                  float32 `json:"brakePosition"`
32	Clutch                 float32 `json:"clutchPosition"`
33	Gear                   float32 `json:"gear"`
34	Gforce_lat             float32 `json:"-"`
35	Gforce_lon             float32 `json:"-"`
36	Lap                    float32 `json:"-"`
37	EngineRate             float32 `json:"rpm"`
38	Sli_pro_native_support float32 `json:"-"` // SLI Pro support
39	Car_position           float32 `json:"-"` // car race position
40	Kers_level             float32 `json:"-"` // kers energy left
41	Kers_max_level         float32 `json:"-"` // kers maximum energy
42	Drs                    float32 `json:"-"` // 0 = off, 1 = on
43	Traction_control       float32 `json:"-"` // 0 (off) - 2 (high)
44	Anti_lock_brakes       float32 `json:"-"` // 0 (off) - 1 (on)
45	Fuel_in_tank           float32 `json:"-"` // current fuel mass
46	Fuel_capacity          float32 `json:"-"` // fuel capacity
47	In_pits                float32 `json:"-"` // 0 = none, 1 = pitting, 2 = in pit area
48	Sector                 float32 `json:"-"` // 0 = sector1, 1 = sector2 float32 `json:"-"` 2 = sector3
49	Sector1_time           float32 `json:"-"` // time of sector1 (or 0)
50	Sector2_time           float32 `json:"-"` // time of sector2 (or 0)
51	Brakes_temp            float32 `json:"-"` // brakes temperature (centigrade)
52	Wheels_pressure        float32 `json:"-"` // wheels pressure PSI
53	Teainfo                float32 `json:"-"` // team ID
54	Total_laps             float32 `json:"-"` // total number of laps in this race
55	Track_size             float32 `json:"-"` // track size meters
56	Last_lap_time          float32 `json:"-"` // last lap time
57	Max_rpm                float32 `json:"-"` // cars max RPM, at which point the rev limiter will kick in
58	Idle_rpm               float32 `json:"-"` // cars idle RPM
59	Max_gears              float32 `json:"-"` // maximum number of gears
60	SessionType            float32 `json:"-"` // 0 = unknown, 1 = practice, 2 = qualifying, 3 = race
61	DrsAllowed             float32 `json:"trackLength"` // 0 = not allowed, 1 = allowed, -1 = invalid / unknown
62	Track_number           float32 `json:"-"` // -1 for unknown, 0-21 for tracks
63	VehicleFIAFlags        float32 `json:"maxRpm"` // -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red

    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


'''
import socket, struct
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
BUFF_SIZE=256


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
                print('GEAR:%s\tPOW:%lf%%\tV:%03dkph\r'%(GEAR[info[POS_GEAR]], info[POS_RPM_CURR]*100./info[POS_RPM_MAX], int(info[POS_V]*3.6)))
            else:
                # broken sock, fallback and reconnect
                raise Exception('broken sock')
    except Exception as E:
        print(E, ', retry %d'%i)