# Monitoring buy, sell, oco, ... orders binance
# V0.15

from binance.client import Client  # for connections binance
from binance.websockets import BinanceSocketManager  # for websocket binance
from twisted.internet import reactor  # for exit program
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
    root.after(5000, lambda: root.destroy())  # time in ms
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
            is_msg = f_timestamp(msg['T']) + ' ' + msg['s'] + ' ' + msg['c'] + ' ' + msg['l'] + ' ' + msg['L'] + ' ' + \
                     msg['r']
            p_is_msg(is_msg)

        if msg['e'] == 'executionReport':
            base_exchanged = str(round(float(msg['p']) * float(msg['q']), 8))
            is_msg = f_timestamp(msg['T']) + ' ' + msg['s'] + ' ' + msg['S'] + ' ' + msg['o'] + ' ' + msg[
                'x'] + ' quantity:' + msg['q'] + ' price:' + msg['p'] + ' stop:' + msg[
                         'P'] + ' ' + 'Base:' + base_exchanged
            p_is_msg(is_msg)

            if is_oco:
                is_oco = False
            else:
                p_is_msg('-' * 20)
                mon_popup()  # later send to notification - telegram - ...
            #  (short version) is_oco = False if is_oco else p_is_msg('-' * 20); mon_popup()


bm = BinanceSocketManager(client)
conn_key = bm.start_user_socket(process_message)  # start user sockets
bm.start()  # Start the socket manager


'''
try:
    is_counter = 96  # Run x * countdown and then exit program
    while is_counter > 0:
        countdown(300)  # countdown x seconds 1800 = 30 minutes
        is_counter -= 1
        if bm.is_alive():
            print(bm.is_alive())
            #  send keepalive
#            bm._keepalive_account_socket
        else:
            #  Connect to user socket
            print(bm.is_alive())
            bm.close()
            conn_key = bm.start_user_socket(process_message)
            #  then start the socket manager
            bm.start()
except KeyboardInterrupt:
    print(bm.is_alive())
    print('Exiting the script')
'''


try:
    while True:
        #        time.sleep(60 * 60 * 24)
#        time.sleep(10)
#        print(bm.is_alive())

#        bm.stop_socket(conn_key)

#        print(bm.is_alive())
#        conn_key = bm.start_user_socket(process_message)  # start user sockets
#        bm.start()  # Start the socket manager
        client.ping()
        print(conn_key)
        info = client.get_exchange_info()
        print(info)
        countdown(5)
except KeyboardInterrupt:
    print(bm.is_alive())
    print('Exiting the script')


#  Stop sockets
#  bm.stop_socket(conn_key)
bm.close()
reactor.callFromThread(reactor.stop)
