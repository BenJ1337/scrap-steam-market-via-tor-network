# Scraping Steam Market via TOR
## Setup

- $ sudo apt-get install tor
- $ tor --hash-password <your-password>
- $ Warning - Bad practice: change password in source/TorManager.py
- $ sudo nano /etc/tor/torrc
	
		\# Logging is always helpful
		Log notice file /var/log/tor/notices.log
		Log debug file /var/log/tor/debug.log
	
		\# Run TOR in the background
		RunAsDaemon 1
	
		\# To controle TOR Service via stem python api 
		ControlPort 9051
	
		\# generate your own password via: $ tor --hash-password <your-password>
		HashedControlPassword 16:2DD50C65C89053EB605C19109D703CD85E823258621A2BD3BE82A258C6

- $ sudo service tor restart
- $ cd /to/project/
- $ source bin/activate
- $ pip install -r requirements.txt
- $ cd source
- $ python3 BatchMain.py


