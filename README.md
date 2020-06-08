# crypmon
Binance monitor and log program

I've just started with python and I'm trying to make a monitoring program of the buy and sell orders at binance. 
So if I've programmed something really weird just smile hard and then help me in the right direction :-)


It should run in the background, popup notifications and write logs to a file.
I want to do this with websocket so it's real-time.


Suggestions are welcome of course :-)


sample output v0.16 to file

2020-06-08 15:52:56 BTCUSDT BUY LIMIT CANCELED quantity:0.00113900 price:9659.89000000 stop:0.00000000 Base:11.00261471
--------------------
2020-06-08 15:53:49 BTCUSDT BUY LIMIT NEW quantity:0.00114600 price:9597.71000000 stop:0.00000000 Base:10.99897566
--------------------
2020-06-08 15:54:30 BTCUSDT BUY LIMIT CANCELED quantity:0.00114600 price:9597.71000000 stop:0.00000000 Base:10.99897566
--------------------
2020-06-08 15:55:22 BTCUSDT OCO EXEC_STARTED EXECUTING NONE
2020-06-08 15:55:22 BTCUSDT BUY STOP_LOSS_LIMIT NEW quantity:0.00111700 price:9846.85000000 stop:9815.63000000 Base:10.99893145
2020-06-08 15:55:22 BTCUSDT BUY LIMIT_MAKER NEW quantity:0.00111700 price:9493.31000000 stop:0.00000000 Base:10.60402727
--------------------
2020-06-08 15:56:00 BTCUSDT OCO ALL_DONE ALL_DONE NONE
2020-06-08 15:56:00 BTCUSDT BUY STOP_LOSS_LIMIT CANCELED quantity:0.00111700 price:9846.85000000 stop:9815.63000000 Base:10.99893145
2020-06-08 15:56:00 BTCUSDT BUY LIMIT_MAKER CANCELED quantity:0.00111700 price:9493.31000000 stop:0.00000000 Base:10.60402727
--------------------
