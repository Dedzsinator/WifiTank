import RPi.GPIO as GPIO
import os
import time
import wiringpi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

wiringpi.wiringPiSetupGpio()
wiringpi.digitalWrite(26,0)
wiringpi.digitalWrite(17, 0)
wiringpi.digitalWrite(4, 0)
wiringpi.digitalWrite(27, 0)
wiringpi.digitalWrite(22, 0)
host_name = '192.168.86.158'    # Change this to your Raspberry Pi IP address
host_port = 9000

class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command 
            'curl -I http://server-ip-address:port' 
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        """ do_GET() can be tested using curl command 
            'curl http://server-ip-address:port' 
        """
        
        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>Wifi Tank</h1>
            <p>A videoprocessor homerseklete: {}</p>
            <p style="font-size:25px;">Elore: <a style="position:relative; font-size: 50px; right: -35px;" href="/on17">On</a> <a style="position:relative; font-size: 50px; right: -60px;" href="/off17">Off</a></p><br><br>
            <p style="font-size:25px;">Balra: <a style="position:relative; font-size: 50px; right: -35px;" href="/on27">On</a> <a style="position:relative; font-size: 50px; right: -35px;" href="/off27">Off</a></p> <br><br>
            <p style="font-size:25px;">Jobbra: <a style="position:relative; font-size: 50px; right: -35px;" href="/on22">On</a> <a style="position:relative; font-size: 50px; right: -35px;" href="/off22">Off</a></p> <br><br>
            <p style="font-size:25px;">Fek: <a style="position:relative; font-size: 50px; right: -35px;" href="/on4">On</a> <a style="position:relative; font-size: 50px; right: -35px;" href="/off4">Off</a></p> <br><br>
            <div id="led-status"></div>
            <script>
                document.getElementById("led-status").innerHTML="{}";
            </script>
            </body>
            </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        status = ''
        if self.path=='/':
            wiringpi.pinMode(26, 1) # RPI Check (26) to PWM
            wiringpi.pinMode(17, 1) # Forward (17) to output
            wiringpi.pinMode(4, 1) # Brake (4) to output
            wiringpi.pinMode(27, 1) # Left (27) to output
            wiringpi.pinMode(22, 1) # Right (22) to output

        elif self.path=='/on17':
            wiringpi.digitalWrite(26,1)
            wiringpi.digitalWrite(17, 1)
            status='17 is On'
        elif self.path=='/off17':
            wiringpi.digitalWrite(26,0)
            wiringpi.digitalWrite(17, 0)
            status='17 is Off'

        elif self.path=='/on4':
            wiringpi.digitalWrite(26,0)
            wiringpi.digitalWrite(4, 0)
            wiringpi.digitalWrite(26,1)
            wiringpi.digitalWrite(4, 1)
            status='4 is On'
        elif self.path=='/off4':
            wiringpi.digitalWrite(26,0)
            wiringpi.digitalWrite(4, 0)
            status ='4 is Off'

        elif self.path=='/on27':
            wiringpi.digitalWrite(26,0)
            wiringpi.digitalWrite(27, 0)
            wiringpi.digitalWrite(26,1)
            wiringpi.digitalWrite(27, 1)

            status='27 is On'
        elif self.path=='/off27':
            wiringpi.digitalWrite(26,0)
            wiringpi.digitalWrite(27, 0)
            status='27 is Off'

        elif self.path=='/on22':
            wiringpi.digitalWrite(26,0)
            wiringpi.digitalWrite(22, 0)
            wiringpi.digitalWrite(26,1)
            wiringpi.digitalWrite(22, 1)
            status='22 is On'
        elif self.path=='/off22':
            wiringpi.digitalWrite(26,0)
            wiringpi.digitalWrite(22, 0)
            status='22 is Off'
        self.wfile.write(html.format(temp[5:], status).encode("utf-8"))

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
