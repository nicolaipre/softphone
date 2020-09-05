# Softphone
A python 3 compatible softphone built on the [pjproject fork by malarinv, branch:py37](https://github.com/DiscordPhone/pjproject/tree/py37).

To use the streaming capability, use an Audio Callback class that suits your needs. 

See `AudioCallbacks.py` for examples.

For installation instructions, click [here](INSTALL.md).

---
## TODO
- [ ] Fix the slight audio lag/delay when using Audio Callbacks for relaying audio between systems.
- [x] Clean up the code.
- [ ] Write documentation for all functions.
- [x] Add proper logging.
- [ ] Add DTMF support.
- [ ] Add call transfer support.
- [ ] Fix and test incoming calls.
- [ ] Do not force registration of both incoming and outgoing accounts. Make it optional.
- [ ] Fix better error handling.
- [ ] Fix error when phone hangs up before softphone does.
- [ ] Create a [Pypi package](https://pypi.org/) to install via `pip install softphone`.
- [ ] Add support for multiple simultaneous calls.

---
## Missing something? 
You can look for functionality from other projects and create a PR to get it added to this project. 

Examples:
- [soft_phone](https://github.com/g-farrow/soft_phone) - Huge credits to g-farrow. Used some code from his project.
- [Payphone](https://github.com/NottingHack/PBX/blob/master/Payphone/PayPhone.py)
- [Openphone](https://github.com/probonopd/OpenPhone)
- [SIPCallRecordVerify](https://github.com/lukebeer/SIPCallRecordVerify)
- [alex](https://github.com/UFAL-DSG/alex/blob/master/alex/components/hub/vio.py)