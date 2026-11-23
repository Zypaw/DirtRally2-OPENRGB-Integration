# 🏁 DiRT Rally 2.0 → LED Shift Lights

**Turn any WLED LED strip into real-time rally shift lights.** This Python script reads DiRT Rally 2.0's live telemetry and drives an LED strip through OpenRGB, so you know exactly when to shift without looking at the dashboard.

---

## How it works

```
DiRT Rally 2.0 ──UDP telemetry──► telemetry.py ──OpenRGB SDK──► OpenRGB ──Wi-Fi──► WLED controller ──► LED strip
```

1. The game streams telemetry packets over **UDP** (64 floats per packet: speed, gear, RPM, max RPM…)
2. `telemetry.py` decodes each packet with `struct` and calculates how close the engine is to the rev limit
3. The result is turned into a colour pattern and sent to the strip through **OpenRGB**, which talks to a **WLED** controller over Wi-Fi

## Light behaviour

- **Shift bar:** lights up from about 82% of max RPM, filling **symmetrically from both ends toward the centre**: green → yellow → red
- **Shift now:** the whole strip flashes **red** when you hit the top of the range
- **Stage start:** red/green cue at the start of a stage
- **Auto-recovery:** if the game stops sending data, the script reloads the OpenRGB profile and waits for packets again

## Setup

**Requirements:** Windows, Python 3.11, [OpenRGB](https://openrgb.org) with its SDK server enabled, and a [WLED](https://kno.wled.ge) controller added to OpenRGB as a device named `WLED`.

1. **Enable UDP telemetry in the game.** Edit
   `C:\Users\<you>\Documents\My Games\DiRT Rally 2.0\hardwaresettings\hardware_settings_config.xml`:

   ```xml
   <motion_platform>
       <dbox enabled="true" />
       <udp enabled="true" extradata="3" ip="127.0.0.1" port="10001" delay="1" />
   </motion_platform>
   ```

2. **In OpenRGB:** add your WLED device, start the SDK server, and save a profile named `DR2`.

3. **Install and run:**

   ```bash
   pip install -r requirements.txt
   python telemetry.py        # or double-click run.bat
   ```

## Configuration

At the top of `telemetry.py`:

| Setting | Default | Meaning |
|---|---|---|
| `PORT` | `10001` | UDP port (must match the game config) |
| `totals_led` | `30` | Number of LEDs on your strip |
| `ratio` | `6.6 / 8` | Fraction of max RPM where the lights start |

## Tech

Python · UDP sockets · binary packet parsing (`struct`) · [openrgb-python](https://github.com/jath03/openrgb-python) · OpenRGB · WLED (ESP32/ESP8266)

## License

MIT

---

Built by **Matteo Dupond** · [LinkedIn](https://www.linkedin.com/in/matteo-dupond/) · [GitHub](https://github.com/Zypaw)
