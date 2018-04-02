import socket
import struct
import os
import sys
import configparser

myconfig = {}

def wake_on_lan(host):
    global myconfig

    try:
      macaddress = myconfig[host]['mac']
    except:
      return False

    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = b''

    for i in range(0, len(data), 2):
        send_data = b''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, (myconfig['General']['broadcast'], 7))
    return True

def loadConfig():
	global mydir
	global myconfig
	Config = configparser.ConfigParser()
	Config.read(mydir+"/.wol_config.ini")
	sections = Config.sections()
	dict1 = {}
	for section in sections:
		options = Config.options(section)

		sectkey = section
		myconfig[sectkey] = {}

		for option in options:
			myconfig[sectkey][option] = Config.get(section,option)

	return myconfig

def usage():
	print('Usage: wol.py [hostname]')



if __name__ == '__main__':
        mydir = os.path.dirname(os.path.abspath(__file__))
        conf = loadConfig()
        try:
                 if sys.argv[1] == 'list':
                        print('Configured Hosts:')
                        for i in conf:
                                if i != 'General':
                                        print('\t',i)
                        print('\n')
                else:
                        if not wake_on_lan(sys.argv[1]):
                                print('Invalid Hostname specified')
                        else:
                                print('Magic packet should be winging its way')
        except:
                usage()
