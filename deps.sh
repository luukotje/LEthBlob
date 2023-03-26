#! /bin/sh.
pip install typer
pip install web3
pip install pytz
pip install colorama
pip install pyfiglet
yes | sudo apt-get install mtd-utils gzip bzip2 tar arj lhasa p7zip p7zip-full cabextract cramfsswap squashfs-tools sleuthkit default-jdk lzop srecord
git clone https://github.com/ReFirmLabs/binwalk.git
cd binwalk
yes | sudo ./deps.sh
sudo python3 setup.py install
cd ../
rm -R binwalk
