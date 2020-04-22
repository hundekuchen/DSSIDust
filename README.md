# DSSIDust
Webserver that shows the airquality

Consists mainly of
1.)  "scrapeFDS.py" Webscraping via beautifulsoup+selenium (chromedriver has to be installed)
2.) "mainFlaskFDS" Webserving via flask

Both scripts have to be called by hand (or via a tool like daemon-tools - which will restart them automatically if the chromdriver crashes (which seems to happen every 3 or so weeks)).

