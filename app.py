from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

@app.route('/')

def dashboard():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent 
    disk = psutil.disk_usage('/').percent
    return render_template('dashboard.html', cpu=cpu, ram=ram, disk=disk)

@app.route('/api/stats')

def api_stats(): 
    
    data = {
             'cpu': psutil.cpu_percent(),
             'ram': psutil.virtual_memory().percent,
             'disk': psutil.disk_usage('/').percent 
    }

    return jsonify(data)
    

if __name__ == "__main__" :     
    app.run(debug=True)
    
    
    
    
