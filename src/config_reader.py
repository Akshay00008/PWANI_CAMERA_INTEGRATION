import configparser
import os

def get_rtsp_url(stage: str, status: str, view: str) -> str:
    config = configparser.ConfigParser()
    config_path = os.path.join(os.getcwd(), 'config', 'cam_config.ini')
    config.read(config_path)

    section_key = f"{stage}_{view}_{status}"

    try:
        return config[section_key]["path"]
    except KeyError as e:
        # Log which part failed: section or key
        if section_key not in config:
            print(f"Config section '{section_key}' not found. Falling back to default.")
        elif "path" not in config[section_key]:
            print(f"'path' key not found in section '{section_key}'. Falling back to default.")
        
        # Fallback to default
        try:
            return config["default"]["path"]
        except KeyError:
            raise ValueError(f"No valid config found for key='{section_key}', and no [default] path specified.")
