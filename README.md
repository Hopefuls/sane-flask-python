# Sane-Flask-Python

A very crude attempt at implementing sane (Scanner Access Now Easy) in Python using Flask, then dynamically loading the scanned document within the site. Using jQuery and Bootstrap to make it look pretty and dynamic.

My general idea was to hook this up to a Raspberry PI to connect to the printer, to then host a webserver on it that also allows me to manage scanned documents. Have not had time to implement yet.

I have also implemented a Job Queue for the scans, so that multiple scans can be queued up, and then be processed one after another. Just a small extra feature I thought would be nice.

## Credits
- [SANE](https://www.sane-project.org/) <small> good shit fr</small>
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [Bootstrap](https://getbootstrap.com/)
- [jQuery](https://jquery.com/)
- [Pillow (requirement for SANE apparently)](https://pillow.readthedocs.io/en/stable/)

## Information and Aftermath
- Tested on 2 used EPSON printers: `SX600FW` and `WF-2540`, which were given to me due to no longer being used.
- Successfully was able to send scan requests to the printer within Debian GNU/Linux 11 on a separate machine (see it as a "printer server :P"), over Ethernet-connected Printers. I'm taking a fair guess this would've worked over WIFI aswell.
- Experienced some issues on both printers with the scan requests (Getting sudden I/O Errors) when testing out higher resolutions (most often on larger ones, causing the printers to blink on the EOL issue), but was able to get it to work on both with lower ones (Thought that the Printers were EOL, turned out they were not upon checking with some very old Diagnostics Tools).
- General Ratio on higher Resolutions: The higher the resolution, the long the scan durations, and the more likely it is to fail too.

## Anyways
- I'm not too good of a python developer, so I'm sure there's a lot of things that could be improved upon.

---
E-Mail: aurel@hopefuls.de  
Website: https://hopefuls.de