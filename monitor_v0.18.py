#  Monitoring buy, sell, oco orders binance.
#  V0.18
#  Files:
#   monitor_vX.XX.py - program
#   bin_api_keys.py - for api keys
#   monitor.log - for logs


from binance.client import Client  # for connections binance
from binance.websockets import BinanceSocketManager  # for websocket binance
# from twisted.internet import reactor  # for exit program reactor.stop() dont work
from bin_api_keys import *  # import api keys
from datetime import datetime  # for date & time
import tkinter as tk  # for gui popup
import sys  # for logfile
import time  # for time.sleep
import subprocess  # for ping
import platform  # for ping


client = Client(api_key=PUBLIC, api_secret=SECRET)  # keys are in file bin_api_keys.py
is_oco = False


def ping_ip(current_ip_address):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
        ) == "windows" else 'c', current_ip_address), shell=True, universal_newlines=True)
        if 'unreachable' in output:
            return False
        else:
            return True
    except Exception:
        return False


def countdown(t):  # Countdown for next socket alive pings
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        #        print(timeformat, end='\r')  # Don't work
        sys.stdout.write('\r' + timeformat + ' countdown ')
        time.sleep(1)
        t -= 1


def f_mon_popup():  # popup a message to screen that there was a action on binance
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


def f_date_time():  # datetime object containing current date and time
    now = datetime.now()
    _date_time = (now.strftime('%Y-%m-%d %H:%M:%S'))
    return _date_time


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
#                p_is_msg('-' * 20)
                f_mon_popup()  # later send to notification - telegram - ...
            #  (short version) is_oco = False if is_oco else p_is_msg('-' * 20); mon_popup()


while True:
    if ping_ip('1.1.1.1'):  # Do we have internet?
        print('Internet connected')
        bm = BinanceSocketManager(client)
        conn_key = bm.start_user_socket(process_message)  # start user sockets
        bm.start()  # Start the socket manager
        stream_key = client.stream_get_listen_key()

        #  If there is internet send keepalive signal
        try:
            while True:
                countdown(900)
                if ping_ip('1.1.1.1'):  # Do we still have internet?
                    stream_key_sec = client.stream_get_listen_key()
                    if stream_key != stream_key_sec:
                        print('Something gone wrong. Reconnecting the stream ' + f_date_time())
                        bm.stop_socket(conn_key)
                        bm.close()
                        bm = BinanceSocketManager(client)
                        conn_key = bm.start_user_socket(process_message)  # start user sockets
                        bm.start()
                        stream_key = client.stream_get_listen_key()
                    else:
                        print('Send Stay alive signal after count down ' + f_date_time())
                        client.stream_keepalive(stream_key)
                else:
                    print('No internet. Wait for internet connection ' + f_date_time() )
                    countdown(15)  # No internet, wait x sec and try again
        except KeyboardInterrupt:  # Only needed while coding
            print(f_date_time() + ' Exit the script')
            bm.stop_socket(conn_key)
            bm.close()
#            reactor.stop()
            break
        except TimeoutError as is_err:
            print(is_err)
            bm.stop_socket(conn_key)
            bm.close()
    else:
        print('No internet. Wait 15 sec abd try again ' + f_date_time())
        countdown(15)  # No internet, wait x sec and try again
