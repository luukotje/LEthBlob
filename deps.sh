#! /bin/sh.
pip install typer
pip install web3
pip install pytz
pip install colorama
pip install pyfiglet
git clone https://github.com/ReFirmLabs/binwalk.git
cd binwalk
yes | sudo ./deps.sh
sudo python3 setup.py install
cd ../
rm -R binwalk
