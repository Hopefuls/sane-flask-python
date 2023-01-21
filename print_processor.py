import ocrmypdf
import threading
import time
import random
import string
import sane
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

class PrintJob:
    def __init__(self, filename):
        self.filename = filename
        self.state = "Pending"

    def state(self, state=None):
        if state is not None:
            self.state = state
        return self.state


class PrintProcessor:
    def __init__(self):
        self.queue = []

    def add_job(self, job):
        self.queue.append(job)

    def check_job_state(self, filename):
        for job in self.queue:
            if job.filename == filename:
                return job.state
        return None

    def process(self):
        while True:
            for job in self.queue:
                if job.state == "Complete":
                    continue
                try:
                    print("Processing job")
                    job.state = "Processing scan"

                    scanner = sane.open("epson2:net:PRINTER_IP")

                    scanner.resolution = 300
                    scanner.mode = "color"
                    print(scanner.get_options())
                    scanner.start()
                    job.state = "Scanning"
                    image = scanner.snap()

                    scanner.close()
                    timestamp = time.time()
                    filename = job.filename

                    job.state = "Saving scan"
                    image.save("prints/" + filename + ".png")

                    print("Scan saved to " + filename)

                    job.state = "Converting to PDF"

                    pdf_image = image.convert('RGB')

                    pdf_image.save("prints/" + filename + ".pdf")

                    print("Scan converted to PDF")

                    job.state = "Applying OCR"
                    print("Starting OCR")
                    ocrmypdf.ocr("prints/"+filename+".pdf", "prints/"+filename +
                                 ".pdf", deskew=True, max_image_mpixels=10000000000000000000)
                    print("OCR complete")

                    job.state = "Complete"

                    print("Job complete!")

                except Exception as e:
                    print("Error processing job")
                    print(e)
                    job.state = "Error"
                    continue

    def start_thread(self):
        print("Starting thread")
        t = threading.Thread(target=self.process)
        t.start()
