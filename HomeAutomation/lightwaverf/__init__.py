import socket

class LightwaveMediator:
    """Provides interaction with the LightwaveRF home automation suite"""
    
    def __init__(self, ip = None, port = None, debug_mode = None):   
        # Define class constants
        DEFAULT_LIGHTWAVE_UDP_IP = "255.255.255.255"
        DEFAULT_LIGHTWAVE_UDP_PORT = 9760

        if ip == None:
            ip = DEFAULT_LIGHTWAVE_UDP_IP
        self.ip = ip
        
        if port == None:
            port = DEFAULT_LIGHTWAVE_UDP_PORT         
        self.port = port

        if debug_mode == None:
            self.debug_mode = debug_mode
        else:
            self.debug_mode = True
    
    
    def execute_plug(self, room_number, device_number, on):
        """Executes a command against the LightwaveRF Wifi link to turn a plug socket on/off"""

        on_as_int = 0
        if on == 'on':
            on_as_int = 1
                
        message = '000,!R' + str(room_number) + 'D' + str(device_number) + 'F' + str(on_as_int) + '|'

        if self.debug_mode:
            print 'DEBUG: Sending: ' + message + ' to ' + str(self.ip) + ':' + str(self.port) 
        else:
            # Original samples based on http://blog.networkedsolutions.co.uk/?p=149

            # set up the socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Indicate to the socket that we're doing a broadcast.

            # important - the first time that this is ran, if we don't get the device turned on, then we end up with a 'Not yet Registered see Wifi link' response
            # so re-run the command then authorise the device on the Wifi link
            sock.sendto(message, (self.ip, self.port))

class LightwaveDeviceList:
    """Maintains a list of devices that can be controlled by the LightwaveRF Wifi link"""
   
    def __init__(self):
        self.devices = []

    def append(self, room_name, room_number, device_name, device_number):
        """Adds a new device to the list of devices available"""

        d = LightwaveDevice(room_name, room_number, device_name, device_number)
        self.devices.append(d)

    def find(self, room_name, device_name):
        """Returns the device matching the specified room/device name"""
    
        return next((d for d in self.devices if d.room_name == room_name and d.device_name == device_name), None)


class LightwaveDevice:
    """Simple DTO to allow easy referencing of the LightwaveRF devices"""
    
    def __init__(self, room_name, room_number, device_name, device_number):
        self.room_name = room_name
        self.room_number = room_number
        self.device_name = device_name
        self.device_number = device_number