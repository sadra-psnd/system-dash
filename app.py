from flask import Flask, render_template, jsonify
import psutil, time

app = Flask(__name__)

#global_var for upload and download speed calculation goes here: 

prev_net = psutil.net_io_counters()
prev_time = time.time()

def upload_speed_calculator():
    global prev_net, prev_time

    current_time = time.time() 
    interval = current_time - prev_time
    current_net = psutil.net_io_counters()    
    upload_speed = (current_net.bytes_sent - prev_net.bytes_sent) / interval

    prev_net = current_net
    prev_time = current_time 
    
    return round(upload_speed / 1024 / 1024, 2)


    
    
def download_speed_calculator():
    global prev_net, prev_time

    current_time = time.time() 
    interval = current_time - prev_time
    current_net = psutil.net_io_counters()    
    download_speed = (current_net.bytes_recv - prev_net.bytes_recv) / interval
    
    prev_net = current_net
    prev_time = current_time 
    
    return round(download_speed/1024/1024,2)



@app.route('/')

def dashboard():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent 
    disk = psutil.disk_usage('/').percent
    processes = len(psutil.pids())
    download = download_speed_calculator()
    upload = upload_speed_calculator()

    return render_template('dashboard.html', cpu=cpu, ram=ram, disk=disk,processes=processes, download=download, upload=upload)


@app.route('/api/stats')

def api_stats(): 
    
    data = {
             'cpu': psutil.cpu_percent(),
             'ram': psutil.virtual_memory().percent,
             'disk': psutil.disk_usage('/').percent, 
             'processes': len(psutil.pids()),
             'upload':  upload_speed_calculator(),
             'download': download_speed_calculator()
    }

    return jsonify(data)
    

if __name__ == "__main__" :     
    app.run(debug=True)
    
    
    
    
