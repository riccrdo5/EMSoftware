# Essential Machine
Essential Machine is an attempt at solving the problem of reducing contact in School places by manufacturing vending machines (referred to as Essential Machine) that dispense masks, gloves, sanitizers in a safer, more convenient manner compared to physical stores. The Essential Machine is more advanced & safer than the typical vending machine allowing NFC payments & gesture-based product selections.

### Connecting to Raspberry Pi Zero

```shell
# See IP
ping raspberrypi.local 
ssh pi@<IP>
```

### Installation 

1. Install the following [1] :

```shell
# Install Apache
sudo apt-get update
sudo apt-get install apache2
# Install & enable mod_wsgi
sudo apt-get install libapache2-mod-wsgi-py3
sudo a2enmod wsgi
# Install flask
sudo apt-get -y install python3-pip
sudo virtualenv venv
source venv/bin/activate 
sudo pip3 install Flask 
sudo pip3 install braintree
deactivate
# Install git
sudo apt install git
```

2. Clone the repo to the mentioned directory

```shell
cd /var/www
git clone git@github.com:rbhatmanjunath/Essential-Machine.git
```

3. Configure and enable a new virtual host

```shell
sudo nano /etc/apache2/sites-available/Essential-Machine.conf
```

​	Copy the following snippet to the file (replace PORT_NUM to a use-able one  set in 	**/etc/apache2/ports.conf** )

​	To see IP_ADDRESS :

```shell
ip a 
```

```html
<VirtualHost *:[PORT_NUM]>
		ServerName  [IP_ADDRESS]
		WSGIScriptAlias / /var/www/Essential-Machine/essential-machine.wsgi
		<Directory /var/www/Essential-Machine/EssentialMachine/>
			Options Indexes FollowSymLinks
        	AllowOverride None
        	Require all granted
		</Directory>
		Alias /static /var/www/Essential-Machine/EssentialMachine/static
		<Directory /var/www/Essential-Machine/EssentialMachine/static/>
			Options Indexes FollowSymLinks
        	AllowOverride None
        	Require all granted
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

​	Enable virtual host:

```shell
sudo a2ensite Essential-Machine
```

4. Restart Apache

```shell
sudo service apache2 restart
```

5. You can access the site at <IP_ADDRESS>:<PORT_NUM>/ (set in the above conf file)
6. You can use the below command to debug any sever errors. 

```shell
sudo tail /var/log/apache2/error.log
```



### Seeding the Vending Machine

Seeding of new values is done using the **seed.json** file. Change values in seed.json on refilling the vending machine. Restarting apache will recreate new database from the see file automatically. 

```shell
chmod 777 essential_machine.db  #To give write permissions to the application.
```

### Links

1. Requirements Doc : https://docs.google.com/document/d/1pL1OQKAG_y0TedEhb8_uJ0G1WjsEsvN7fQND7V4Hz8A/edit?usp=sharing \

2. Tech Doc : https://docs.google.com/document/d/1OZ1lKpC63EFUXhxcRaagmha4MLM1sPBBZfm1O3grkcg/edit?usp=sharing \

3. Project Plan : https://docs.google.com/spreadsheets/d/15ySL5LcNYjrFK7YZlGYBOm3f4PcyWODQpZH9RQTysSM/edit?usp=sharing

### References

[1] https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
