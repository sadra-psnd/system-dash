import threading
from ping3 import ping, verbose_ping
import psutil
import time
import datetime
import platform



def plugged_status():
    if psutil.sensors_battery().power_plugged == None:
        return "Not a laptop"
    if psutil.sensors_battery().power_plugged:
        return "Charging"
    
    else:
        return "not plugged in"


def uptime_calculator():
    # Calculate uptime in seconds
    uptime_seconds = time.time() - psutil.boot_time()

    # Convert to hours and minutes
    hours = int(uptime_seconds // 3600)  # Total hours
    minutes = int((uptime_seconds % 3600) // 60)  # Remaining minutes

    return (f"{hours} hours and {minutes} minutes")

def packet_loss(count=10):
    lost = 0
    for _ in range(count):
        if ping("8.8.8.8") is None:
            lost += 1
    loss_percent = (lost / count) * 100
    return f"Packet loss: {loss_percent:.2f}%"

#global_var for upload and download speed calculation goes here: 

speed_lock = threading.Lock()

prev_net = psutil.net_io_counters()
prev_time = time.time()

def get_network_speeds():
    """
    Calculates both upload and download speeds using one timing snapshot
    to ensure consistency and avoid overlapping updates.
    Returns speeds in MB/s (rounded to 2 decimals).
    """
    global prev_net, prev_time
    
    with speed_lock:
    
        current_net = psutil.net_io_counters()
        current_time = time.time()

        interval = current_time - prev_time
        if interval == 0:
            return 0, 0  # avoid division by zero if called too quickly

        upload_speed = (current_net.bytes_sent - prev_net.bytes_sent) / interval
        download_speed = (current_net.bytes_recv - prev_net.bytes_recv) / interval

        # update the previous counters for next call
        prev_net = current_net
        prev_time = current_time

    # convert to MB/s and round
    return round(upload_speed / 1024 / 1024, 2), round(download_speed / 1024 / 1024, 2)