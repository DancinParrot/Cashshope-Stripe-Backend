# Cashshope Stripe Webserver

Source code for Cashshope's Stripe Apache Webserver that runs on Python Flask, including a setup guide.

## Pre-requisites
This guide will use the following to configure a webserver:
- Ubuntu 20.04 Virtual Machine
- Microsoft Azure to Host the Webserver

<br/>

Packages required:
- Python and PIP
- Stripe Dependency
- Apache2 with mod_wsgi
- certbot
- snapd

## Setup

### Update and Installation of Required Packages and Dependencies
1) Setup a Ubuntu 20.04 VM on Azure, and a Standard B1s instance with 1GB RAM and 1 vCPU should suffice. 
2) SSH or Login to the Webserver via its public IP Address, and do a update + upgrade the server.
3) Install the latest version of Python and PIP to your Ubuntu VM.
4) Install the latest Stripe API as well on the server through ```pip3 install --upgrade stripe```
5) Install Apache2 webserver as well as the following module: mod_wsgi to enable Apache2 to serve the Flask webapp.

### Code and Configuration
6) Create a folder, "stripeweb" in the location, /var/www, of your VM.
7) Copy the files given in the repo to the folder located at, /var/www/stripeweb.
8) You may choose to create a webpage, e.g. index.html, in the folder, /var/www/stripeweb/templates to serve webpage content to the user.
9) Copy the config file named, "app.conf" to the following location, /etc/apache2/sites-available.

### Enable the Apache2 Modules
10) Do check that Apache2 is running by doing a ```systemctl status Apache2.service```. Otherwise, start and enable the service.
11) You need to run this with root privelleges, ```a2enmod wsgi```, as well as ```a2ensite app.conf``` in /etc/apache2/sites-available.
12) Now you may restart Apache2 by doing a ```systemctl restart Apache2.service```, and visit the public ip address of your webserver.

### Enabling HTTPS
13) In the Azure portal, configure a DNS name for your webserver, which is required for a HTTPS cert.
14) Follow [certbot's guide](https://certbot.eff.org/instructions?ws=apache&os=ubuntufocal) on installing the required dependencies, as well as obtaining a HTTPS cert.
15) You may now communicate with the webserver through the Android client, without allowing cleartext HTTP communcation.

## IMPORATNT
By copying and pasting the source code and config file without changing the DNS name may result in issues, especially during the process of enabling HTTPS, as seen in app.conf:
```
<VirtualHost *>
    ServerName cashshope.japaneast.cloudapp.azure.com
```
Do change the DNS name to the one that you've configured before attempting to connect to the server, or enabling HTTPS.


## References
https://stripe.com/docs/connect/collect-then-transfer-guide?platform=android&ui=custom <br/>
https://www.bogotobogo.com/python/Flask/Python_Flask_HelloWorld_App_with_Apache_WSGI_Ubuntu14.php <br/>
https://letsencrypt.org/getting-started/ <br/>
https://certbot.eff.org/instructions?ws=apache&os=ubuntufocal <br/>
https://www.thegeeksearch.com/setup-flask-with-apache-and-wsgi/ <br/>
