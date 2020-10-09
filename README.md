# Essential Machine
Essential Machine is an attempt at solving the problem of reducing contact in School places by manufacturing vending machines (referred to as Essential Machine) that dispense masks, gloves, sanitizers in a safer, more convenient manner compared to physical stores. The Essential Machine is more advanced & safer than the typical vending machine allowing NFC payments & gesture-based product selections.



### Installation

1. Install the following:

```shell
# Install Apache
sudo apt-get update
sudo apt-get install apache2
# Install & enable mod_wsgi
sudo apt-get install libapache2-mod-wsgi python-dev
sudo a2enmod wsgi
# Install flask
sudo apt-get install python-pip 
sudo pip install Flask 
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

​	Copy the following snippet to the file (replace PORT_NUM to a use-able one  set in 	**/etc/apache2/ports.conf**)

```html
<VirtualHost *:PORT_NUM>
		ServerName  IP_ADDRESS
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

### Seeding the Vending Machine

## Links
Requirements Doc : https://docs.google.com/document/d/1pL1OQKAG_y0TedEhb8_uJ0G1WjsEsvN7fQND7V4Hz8A/edit?usp=sharing \
Tech Doc : https://docs.google.com/document/d/1OZ1lKpC63EFUXhxcRaagmha4MLM1sPBBZfm1O3grkcg/edit?usp=sharing \
Project Plan : https://docs.google.com/spreadsheets/d/15ySL5LcNYjrFK7YZlGYBOm3f4PcyWODQpZH9RQTysSM/edit?usp=sharing
