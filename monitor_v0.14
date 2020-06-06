# Monitoring buy, sell, oco, ... orders binance
# V0.14

from binance.client import Client  # for connections binance
from binance.websockets import BinanceSocketManager  # for websocket binance
from twisted.internet import reactor  # for exit programs
from bin_api_keys import *  # import api keys
from datetime import datetime
import tkinter as tk  # for gui popup
import sys
import time

# keys are in file bin_api_keys.py
client = Client(api_key=PUBLIC, api_secret=SECRET)
is_oco = False
user_listen_key = ''

#  Countdown for next socket alive pings
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
#        print(timeformat, end='\r')
        sys.stdout.write('\r' + timeformat + ' countdown until next socket update cycle ')
        time.sleep(1)
        t -= 1

# popup a message to screen that there was a action on binance
def mon_popup():
    root = tk.Tk()
    root.title("Monitor Popup")
    tk.Label(root, text="  There was a action on binance  ").pack()
    root.after(15000, lambda: root.destroy())  # time in ms
    root.mainloop()


#  print is_msg to terminal. (later to write to a file).
def p_is_msg(pr_msg):
    print(pr_msg)

# make date time nice
def f_timestamp(nr):
    timestamp = int(nr) / 1000
    timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

# run when binance user_socket sends user message
def process_message(msg):
    if msg['e'] == 'error':
        p_is_msg(msg['m'])
    else:
        global is_oco
        if msg['e'] == 'listStatus':
            is_oco = True
            is_msg = f_timestamp(msg['T']) + ' ' + msg['s'] + ' ' + msg['c'] + ' ' + msg['l'] + ' ' + msg['L'] + ' ' + msg['r']
            p_is_msg(is_msg)

        if msg['e'] == 'executionReport':
            base_exchanged = str(round(float(msg['p']) * float(msg['q']), 8))
            is_msg = f_timestamp(msg['T']) + ' ' + msg['s'] + ' ' + msg['S'] + ' ' + msg['o'] + ' ' + msg['x'] + ' quantity:' + msg['q'] +' price:' + msg['p'] +' stop:' + msg['P'] + ' ' + 'Base:' + base_exchanged
            p_is_msg(is_msg)

            if is_oco:
                is_oco = False
            else:
                p_is_msg('-' * 20)
                mon_popup()  # later send to notification - telegram - ...
            #  (short version) is_oco = False if is_oco else p_is_msg('-' * 20); mon_popup()


bm = BinanceSocketManager(client)
#  bm = BinanceSocketManager(client, user_timeout=60)

# start user sockets
conn_key = bm.start_user_socket(process_message)

#  Start the socket manager
bm.start()


#  get user_listenkey
user_listen_key = client.stream_get_listen_key()
# print('listenkey', user_listen_key)


#  Just for testing .....
#  for testing program stop after enter
#  input("For testing temp exit trough key: Press Enter to stop monitoring ...\n\n")
#  time.sleep(3600)  # Countdown seconds 3600 = 1h


is_counter = 60 #  Run x * countdown and then exit program
while is_counter > 0:
    countdown(1800) #  countdown x seconds 1800 = 30 minutes
    is_counter -= 1
#   Put here the next socket update part
    bm._keepalive_account_socket
    print('send keep alive signal')


#  Stop sockets
bm.stop_socket(conn_key)
bm.close()
reactor.stop()
