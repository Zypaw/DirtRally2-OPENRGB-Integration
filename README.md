# DRTelemetry

Show rpms counter of dirt rally wirelessly to a wled controler that is attached to a led strip to show RPMS

## Usage

1. Download from the releases tab

2. Edit your `C:\Users\USER\Documents\My Games\DiRT Rally\hardwaresettings\hardware_settings_config.xml` and enable UDP data:

    ```xml
    <motion_platform>
            <dbox enabled="true" />
            <udp enabled="true" extradata="3" ip="127.0.0.1" port="10001" delay="1" />
    </motion_platform>
    ```