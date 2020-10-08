# Installation instructions for softphone.
Until [this issue](https://github.com/pjsip/pjproject/issues/2352) is implemented in the official project, follow the instructions below to set up an instance of softphone.

**1a. Install PJSIP (patch by: malarinv)**
```bash
sudo apt install python3 python3-dev build-essential libasound2-dev
wget https://github.com/DiscordPhone/pjproject/archive/py37.zip
unzip py37.zip
cd pjproject-py37
chmod +x configure aconfigure
./configure CXXFLAGS=-fPIC CFLAGS=-fPIC LDFLAGS=-fPIC CPPFLAGS=-fPIC
make dep
make
sudo make install
```

**1b. Install PJSUA Python bindings for PJSIP**
```bash
cd pjproject-py37/pjsip-apps/src/python
python3 setup.py build
sudo python3 setup.py install
```

**2. Install softphone python package**
```bash
git clone git@github.com:DiscordPhone/softphone.git
python3 -m pip install -e softphone
python3 -m pip install -r softphone/requirements.txt
```
Or:
```bash
python3 -m pip install https://github.com/DiscordPhone/softphone/archive/master.zip --user
```
