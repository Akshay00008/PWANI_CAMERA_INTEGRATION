import configparser
import os

def get_rtsp_url(status: str, view: str) -> str:
    config = configparser.ConfigParser()
    config_path = os.path.join(os.getcwd(), 'config', 'cam_config.ini')
    print(config_path)
    config.read(config_path)
    print("config")
    try:
        return config[status][view]
    except KeyError:
        raise ValueError(f"Invalid combination of status='{status}' and view='{view}'")
