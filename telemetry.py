'''
    This script test if your Diry Rally UDP Server has been started properly.
    the steam post of the UDP data format in detail : https://steamcommunity.com/app/310560/discussions/0/481115363869500839/

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    for extradata = 3: output = 64 floats
    byteformat: little endian

    Position Info | Content Info
    No. Byte | Format Value

    0. 0 float Time
    1. 4 float Time of Current Lap
    2. 8 float Distance Driven on Current Lap
    3. 12 float Distance Driven Overall
    4. 16 float Position X
    5. 20 float Position Y
    6. 24 float Position Z
    7. 28 float Velocity (Speed) [m/s]
    8. 32 float Velocity X
    9. 36 float Velocity Y
    10. 40 float Velocity Z
    11. 44 float Roll Vector X
    12. 48 float Roll Vector Y
    13. 52 float Roll Vector Z
    14. 56 float Pitch Vector X
    15. 60 float Pitch Vector Y
    16. 64 float Pitch Vector Z
    17. 68 float Position of Suspension Rear Left
    18. 72 float Position of Suspension Rear Right
    19. 76 float Position of Suspension Front Left
    20. 80 float Position of Suspension Front Right
    21. 84 float Velocity of Suspension Rear Left
    22. 88 float Velocity of Suspension Rear Right
    23. 92 float Velocity of Suspension Front Left
    24. 96 float Velocity of Suspension Front Right
    25. 100 float Velocity of Wheel Rear Left
    26. 104 float Velocity of Wheel Rear Right
    27. 108 float Velocity of Wheel Front Left
    28. 112 float Velocity of Wheel Front Right
    29. 116 float Position Throttle
    30. 120 float Position Steer
    31. 124 float Position Brake
    32. 128 float Position Clutch
    33. 132 float Gear [0 = Neutral, 1 = 1, 2 = 2, ..., 10 = Reverse]
    34. 136 float G-Force Lateral
    35. 140 float G-Force Longitudinal
    36. 144 float Current Lap
    37. 148 float Speed of Engine [rpm / 10]
    38. 152 float ?
    39. 156 float ?
    40. 160 float ?
    41. 164 float ?
    42. 168 float ?
    43. 172 float ?
    44. 176 float ?
    45. 180 float ?
    46. 184 float ?
    47. 188 float ?
    48. 192 float ?
    49. 196 float ?
    50. 200 float ?
    51. 204 float Temperature Brake Rear Left ?
    52. 208 float Temperature Brake Rear Right ?
    53. 212 float Temperature Brake Front Left ?
    54. 216 float Temperature Brake Front Right ?
    55. 220 float ?
    56. 224 float ?
    57. 228 float ?
    58. 232 float ?
    59. 236 float ?
    60. 240 float Number of Laps in Total ?
    61. 244 float Length of Track in Total
    62. 248 float ?
    63. 252 float Maximum rpm / 10

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
0	Time                   float32 `json:"time"`
1	LapTime                float32 `json:"lapTime"`
2	LapDistance            float32 `json:"lapDistance"`
3	TotalDistance          float32 `json:"distance"`
4	X                      float32 `json:"-"` // World space position
5	Y                      float32 `json:"-"` // World space position
6	Z                      float32 `json:"-"` // World space position
7	Speed                  float32 `json:"speed"` in [m/s]
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
33	Gear                   float32 `json:"gear"` [0 = Neutral, 1 = 1, 2 = 2, ..., 10 = Reverse]
34	Gforce_lat             float32 `json:"-"`
35	Gforce_lon             float32 `json:"-"`
36	Lap                    float32 `json:"-"` Current Lap
37	EngineRate             float32 `json:"rpm"` [rpm / 10]
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
51-54	Brakes_temp            float32 `json:"-"` // brakes temperature (centigrade)
55-58	Wheels_pressure        float32 `json:"-"` // wheels pressure PSI
59	Teainfo                float32 `json:"-"` // team ID
60	Total_laps             float32 `json:"-"` // total number of laps in this race
61	Track_size             float32 `json:"-"` // track size meters
62	Last_lap_time          float32 `json:"-"` // last lap time
63	Max_rpm                float32 `json:"-"` // cars max RPM, at which point the rev limiter will kick in \ Maximum rpm / 10
64	Idle_rpm               float32 `json:"-"` // cars idle RPM
65	Max_gears              float32 `json:"-"` // maximum number of gears
66	SessionType            float32 `json:"-"` // 0 = unknown, 1 = practice, 2 = qualifying, 3 = race
67	DrsAllowed             float32 `json:"trackLength"` // 0 = not allowed, 1 = allowed, -1 = invalid / unknown
68	Track_number           float32 `json:"-"` // -1 for unknown, 0-21 for tracks
69	VehicleFIAFlags        float32 `json:"maxRpm"` // -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red

    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
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
