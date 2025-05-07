import os
from urllib.parse import urlparse
import re

def get_last_part(rtsp_url):
    parsed_url = urlparse(rtsp_url)

    # if parsed_url.scheme in ["http", "https"]:
    #     # It's a normal URL
    #     last_part = parsed_url.path.strip("/").split("/")[-1]
    #     return os.path.splitext(last_part)[0]

    # if parsed_url.scheme == "rtsp":
    #     ip = parsed_url.hostname  # Extracts '10.10.18.21'
    #     path = parsed_url.path    # Extracts '/Streaming/Channels/101'
        
    #     if ip and path:
    #         ip_ = ip.replace(".", "")  
    #         # last_octet = ip.strip().split(".")[-1]
    #         channel_id = path.strip("/").split("/")[-1]
    #         return f"camera_ip{ip_}_ch{channel_id}"

    # Fallback for local file paths or unhandled schemes
    last_part = re.sub(r'[^a-zA-Z0-9]', '', rtsp_url)
    return last_part