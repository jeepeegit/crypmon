#  Monitoring buy, sell, oco orders binance.
#  V0.16
#  Files:
#   monitor_vX.XX.py - program
#   bin_api_keys.py - for api keys
#   monitor.log - for logs


from binance.client import Client  # for connections binance
from binance.websockets import BinanceSocketManager  # for websocket binance
from twisted.internet import reactor  # for exit program
from bin_api_keys import *  # import api keys
from datetime import datetime
import tkinter as tk  # for gui popup
import sys
import time


client = Client(api_key=PUBLIC, api_secret=SECRET)  # keys are in file bin_api_keys.py
is_oco = False


def countdown(t):  # Countdown for next socket alive pings
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        #        print(timeformat, end='\r')
        sys.stdout.write('\r' + timeformat + ' countdown until next socket update cycle ')
        time.sleep(1)
        t -= 1


def mon_popup():  # popup a message to screen that there was a action on binance
    root = tk.Tk()
    root.title("Monitor Popup")
    tk.Label(root, text="  There was a action on binance  ").pack()
    root.after(5000, lambda: root.destroy())  # time in ms
    root.mainloop()


def p_is_msg(pr_msg):  # print is_msg to terminal, write to file)
    print(pr_msg)
    #  write to monitor.log
    file = open("monitor.log", "a")
    file.write(pr_msg + '\n')
    file.close()


def f_timestamp(nr):  # make date time nice
    timestamp = int(nr) / 1000
    timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp


def process_message(msg):  # run when binance user_socket sends user message
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


try:
    is_counter = 96  # Run x * countdown and then exit program
    while is_counter > 0:
        countdown(60 * 14)  # countdown x seconds 1800 = 30 minutes
        is_counter -= 1
        if bm.is_alive():
            print(bm.is_alive())
            #  send keepalive
            client.ping()
        else:
            #  Connect to user socket
            print(bm.is_alive())
            conn_key = bm.start_user_socket(process_message)
            #  then start the socket manager
            bm.start()
except KeyboardInterrupt:
    print(bm.is_alive())
    print('Exiting the script')


#  Stop sockets
bm.stop_socket(conn_key)
bm.close()
reactor.stop()
