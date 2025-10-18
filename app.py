from flask import Flask, render_template, jsonify
import psutil, time, datetime, platform
from ping3 import ping, verbose_ping


def plugged_status():
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

prev_net = psutil.net_io_counters()
prev_time = time.time()

def get_network_speeds():
    """
    Calculates both upload and download speeds using one timing snapshot
    to ensure consistency and avoid overlapping updates.
    Returns speeds in MB/s (rounded to 2 decimals).
    """
    global prev_net, prev_time
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



app = Flask(__name__)


@app.route('/')
def dashboard():
    upload, download = get_network_speeds()
    packetloss = packet_loss()
    num_cpu_physicall_core = psutil.cpu_count(logical=False)
    cpu = psutil.cpu_percent()
    cpu_info = platform.processor()
    cpu_current_freq = psutil.cpu_freq().current
    ram = psutil.virtual_memory().percent 
    disk = psutil.disk_usage('/').percent
    processes = len(psutil.pids())
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    uptime = uptime_calculator() 
    total_RAM = round(psutil.virtual_memory().total / (1024**3))
    ava_RAM = psutil.virtual_memory().available
    battery_percent= psutil.sensors_battery().percent
    plugged_status = plugged_status()
    
    
    
    

    return render_template('dashboard.html',
                           cpu=cpu,
                           ram=ram,
                           disk=disk,
                           processes=processes,
                           download=download,
                           upload=upload,
                           boot_time=boot_time,
                           numberofcores=num_cpu_physicall_core,
                           uptime=uptime,
                           cpu_info=cpu_info,
                           cpu_current_freq=cpu_current_freq,
                           total_RAM=total_RAM,
                           ava_RAM=ava_RAM,
                           packetloss=packetloss,
                           battery_percent=battery_percent,
                           plugged_status=plugged_status
                           )


@app.route('/api/stats')

def api_stats(): 
    upload, download = get_network_speeds()
    
    data = {
             'cpu': psutil.cpu_percent(),
             'ram': psutil.virtual_memory().percent,
             'disk': psutil.disk_usage('/').percent, 
             'processes': len(psutil.pids()),
             'upload':  upload,
             'download': download,
             'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d , %H:%M:%S"),
             'numberofphysicallcores': psutil.cpu_count(logical=False),
             'uptime': uptime_calculator(),
             'cpu_info': platform.processor(),
             'cpu_current_freq': psutil.cpu_freq().current,
             'total_RAM': round(psutil.virtual_memory().total / (1024**3)),
             'ava_RAM': psutil.virtual_memory().available,
             'packetloss': packet_loss(),
             'battery_percent': psutil.sensors_battery().percent

    }

    return jsonify(data)
    

if __name__ == "__main__" :     
    app.run(debug=True)
    
    
    
"""
System Metrics to Monitor:

Disk:
- Read/Write Speeds
- Total and Free Space
- Number of Partions


Processes:
- Top CPU-Usage Processes (maybe later)
- Top Memory-Usage Processes (maybe later)


Battery (if applicable):
- Time Remaining (maybe later)

"""
    