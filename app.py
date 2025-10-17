from flask import Flask, render_template, jsonify
import psutil, time, datetime

app = Flask(__name__)



def uptime_calclulator():
    # Calculate uptime in seconds
    uptime_seconds = time.time() - psutil.boot_time()

    # Convert to hours and minutes
    hours = int(uptime_seconds // 3600)  # Total hours
    minutes = int((uptime_seconds % 3600) // 60)  # Remaining minutes

    return (f"{hours} hours and {minutes} minutes")


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








# def upload_speed_calculator():
#     global prev_net, prev_time

#     current_time = time.time() 
#     interval = current_time - prev_time
#     current_net = psutil.net_io_counters()    
#     upload_speed = (current_net.bytes_sent - prev_net.bytes_sent) / interval

#     prev_net = current_net
#     prev_time = current_time 
    
#     return round(upload_speed / 1024 / 1024, 2)


    
    
# def download_speed_calculator():
#     global prev_net, prev_time

#     current_time = time.time() 
#     interval = current_time - prev_time
#     current_net = psutil.net_io_counters()    
#     download_speed = (current_net.bytes_recv - prev_net.bytes_recv) / interval
    
#     prev_net = current_net
#     prev_time = current_time 
    
#     return round(download_speed/1024/1024,2)



@app.route('/')
def dashboard():
    upload, download = get_network_speeds()
    num_cpu_physicall_core = psutil.cpu_count(logical=False)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent 
    disk = psutil.disk_usage('/').percent
    processes = len(psutil.pids())
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    uptime = uptime_calclulator() 
    

    return render_template('dashboard.html', cpu=cpu, ram=ram, disk=disk,processes=processes, download=download, upload=upload,boot_time=boot_time, numberofcores=num_cpu_physicall_core, uptime=uptime)


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
             'uptime': uptime_calclulator()
             
    }

    return jsonify(data)
    

if __name__ == "__main__" :     
    app.run(debug=True)