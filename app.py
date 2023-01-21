from flask import Flask, redirect, send_file, render_template, jsonify, request
import sane
import time
import string
import random
import print_processor

app = Flask(__name__)
processor = print_processor.PrintProcessor()
# create 

def process_scan():
    print("Processing scan")
    scanner = sane.open("epson2:net:PRINTER_IP")

    scanner.resolution = 600
    scanner.mode = "color"

    scanner.start()
    image = scanner.snap()

    scanner.close()
    timestamp = time.time()
    filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    filename = str(timestamp) + "_" + filename + ".png"

    # save the image to the filesystem
    image.save("prints/" + filename)

    print("Scan saved to " + filename)
    
    return filename

    




@app.route('/')
def index():
    return render_template("index.html")

@app.route("/startscan")
def start_scan():
    timestamp = time.time()
    filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    filename = str(timestamp) + "_" + filename

    job = print_processor.PrintJob(filename)

    processor.add_job(job)
    request_host = request.host_url
    return jsonify({"url": request_host+"/process/" + filename})



@app.route("/scans/<filename>")
def get_scan(filename):
    # check the state of the job
    state = processor.check_job_state(filename)
    if state is None:
        return "Theres no job with that filename"

    return render_template("base.html", filename=filename, state=state)


@app.route("/files/<filename>")
def get_file(filename):
    return send_file("prints/" + filename)

@app.route("/process/<filename>")
def process(filename):
    state = processor.check_job_state(filename)

    if state is None:
        return "Theres no job with that filename"

    if state == "Complete":
        return jsonify({"state": "Complete", "url": request.host_url + "/files/" + filename + ".pdf"})
    
    return jsonify({"state": state})

if __name__ == '__main__':
    print("Starting Queue thread")
    processor.start_thread()
    app.run(host="0.0.0.0", port=5000)