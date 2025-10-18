from flask import Flask, render_template, jsonify, Blueprint
import psutil, time, datetime, platform
from app.metrics import get_network_speeds, packet_loss, uptime_calculator, plugged_status


bp = Blueprint('main', __name__)

@bp.route('/')

def dashboard():
    upload, download = get_network_speeds()
    packetloss = packet_loss()
    num_cpu_physical_core = psutil.cpu_count(logical=False)
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
    plugged_state = plugged_status()
    battery = psutil.sensors_battery()
    if battery:
        battery_percent = battery.percent
    else:
        battery_percent = None


    
    
    
    

    return render_template('dashboard.html',
                           cpu=cpu,
                           ram=ram,
                           disk=disk,
                           processes=processes,
                           download=download,
                           upload=upload,
                           boot_time=boot_time,
                           num_cpu_physical_core=num_cpu_physical_core,
                           uptime=uptime,
                           cpu_info=cpu_info,
                           cpu_current_freq=cpu_current_freq,
                           total_RAM=total_RAM,
                           ava_RAM=ava_RAM,
                           packetloss=packetloss,
                           battery_percent=battery_percent,
                           plugged_state=plugged_state
                           )


@bp.route('/api/stats')

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
             'num_cpu_physical_core': psutil.cpu_count(logical=False),
             'uptime': uptime_calculator(),
             'cpu_info': platform.processor(),
             'cpu_current_freq': psutil.cpu_freq().current,
             'total_RAM': round(psutil.virtual_memory().total / (1024**3)),
             'ava_RAM': psutil.virtual_memory().available,
             'packetloss': packet_loss(),
             'battery_percent': psutil.sensors_battery().percent

    }

    return jsonify(data)
    
    

    
    
    
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
    
    
    