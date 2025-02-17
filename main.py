import socket, network, time, mma8451, machine, math, _thread, random

# Constants
NON_COMBATANT = 0
COMBATANT = 1
UNDETERMINED_N = 2
UNDETERMINED_C = 3

# Bool Vars
PAIRED = False
HIT = False

# Device Vars
ROLE = COMBATANT
ID = -1
CANCEL = False

# Board Vars
LED = machine.Pin('LED', machine.Pin.OUT)
RED = machine.Pin(13, machine.Pin.OUT)
BLU = machine.Pin(15, machine.Pin.OUT)
GRN = machine.Pin(14, machine.Pin.OUT)

def SetLight(r=0, g=0, b=0):
    RED.value(r)
    GRN.value(g)
    BLU.value(b)

# Network Vars & Setup
net = network.WLAN(network.STA_IF)
net.active(True)
net.disconnect()
time.sleep(0.5)
net.connect('QUICOMM_Lnk', 'flomoco29')
while net.status() != network.STAT_GOT_IP:
    if net.status() == network.STAT_IDLE or net.status() == network.STAT_CONNECT_FAIL:
        net.connect('QUICOMM_Lnk', 'flomoco29')
    SetLight(1, 1, 1)
    time.sleep(1)
    SetLight()
    time.sleep(1)
SetLight(0, 1, 0)
LOCAL_IP = net.ifconfig()[0]
print(network.STAT_GOT_IP)
print(LOCAL_IP)
print(net.isconnected())

SERVER_IP = '0.0.0.0' # Socket Stuff
UDP_PORT = 32444
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LOCAL_IP, UDP_PORT))

# Role Functions
def GetRole():
    sock.sendto(bytes(f'ROLE:{ROLE}', 'utf-8'), (SERVER_IP, UDP_PORT))

def SetRole(role):
    global ROLE
    if role > UNDETERMINED_C or role < NON_COMBATANT:
        return
    ROLE = role

# Device Functions
def Identify():
    for i in range(3):
        SetLight(1, 1, 1)
        time.sleep(0.5)
        SetLight()
        time.sleep(0.5)

def Disconnect():
    global SERVER_IP
    global PAIRED
    global ROLE
    global ID

    SetLight(0, 1, 0)
    ROLE = COMBATANT
    ID = -1
    SERVER_IP = '0.0.0.0'
    PAIRED = False

def Cancel():
    global CANCEL

    while not CANCEL:
        data, addr = sock.recvfrom(4096)
        if data == b'Cancel':
            CANCEL = True
            break
    return

# Active Mode - Sets its role and waits for a hit
def Active():
    global acl
    global ROLE
    global HIT
    global sock
    global CANCEL

    prevTick = 0
    threshold = 0.25
    flashing = False
    try:
        _thread.start_new_thread(Cancel, (), {})
    except OSError:
        pass
    if ROLE == COMBATANT:
        SetLight(1, 0, 0)
    elif ROLE == NON_COMBATANT:
        SetLight(0, 0, 1)
    elif ROLE == UNDETERMINED_N:
        flashing = True
        threshold = 0.75
    elif ROLE == UNDETERMINED_C:
        flashing = True
    else:
        SetLight(1, 0, 0)
    x, y, z = acl.acceleration()
    a = math.sqrt(x**2+y**2+z**2)
    while a < 15:
        x, y, z = acl.acceleration()
        a = math.sqrt(x**2+y**2+z**2)
        if CANCEL:
            break
        if flashing:
            if ((round(time.ticks_ms()/1000, 2)) - prevTick) >= threshold*2.0:
                SetLight()
                prevTick = round(time.ticks_ms()/1000, 2)
            elif ((round(time.ticks_ms()/1000, 2)) - prevTick) >= threshold:
                SetLight(1, 1, 1)
    if not CANCEL:
        HIT = True
        sock.sendto(bytes(f'HIT:{ID}', 'utf-8'), (SERVER_IP, UDP_PORT))
    SetLight()
    time.sleep(1)
    HIT = False
    CANCEL = False

# Listening on the UDP Socket
def Listen():
    global PAIRED
    global SERVER_IP
    global ID

    data, addr = sock.recvfrom(4096)
    print(data)
    if data == b'ID' and not PAIRED:
        SetLight()
        SERVER_IP = addr[0]
        sock.sendto(bytes(f'MYID:{LOCAL_IP}:{ROLE}', 'utf-8'), (SERVER_IP, UDP_PORT))
        print(f'Sent {LOCAL_IP} to Active OnPoint Server')
        PAIRED = True
        data, addr = sock.recvfrom(4096)
        ID = data.decode('utf-8').split(':')[1]
    elif not PAIRED:
        return
    elif data == b'Disconnect':
        Disconnect()
    elif data == b'Identify':
        Identify()
    elif data == b'GetRole':
        GetRole()
    elif data.decode('utf-8').find('SetRole') != -1:
        set = data.decode('utf-8').split(':')
        SetRole(int(set[1]))
    elif data == b'Activate':
        Active()

# I2C & Acceleration setup
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
acl = mma8451.MMA8451(i2c)

# The main loop
while True:
    Listen()
