.PHONY: install

install:
	python3 setup.py $@

clean:
	python3 setup.py clean
	rm -rf build
	rm -rf dist
	rm -rf softphone.egg-info

uninstall:
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/EGG-INFO/PKG-INFO
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/EGG-INFO/SOURCES.txt
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/EGG-INFO/dependency_links.txt
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/EGG-INFO/not-zip-safe
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/EGG-INFO/top_level.txt
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone.egg-link
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/AccountHandler.py
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/AudioCallbacks.py
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/CallHandler.py
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/Exceptions.py
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/Softphone.py
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/__init__.py
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/__pycache__/AccountHandler.cpython-36.pyc
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/__pycache__/AudioCallbacks.cpython-36.pyc
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/__pycache__/CallHandler.cpython-36.pyc
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/__pycache__/Exceptions.cpython-36.pyc
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/__pycache__/Softphone.cpython-36.pyc
	rm /usr/local/lib/python3.6/dist-packages/softphone-0.1-py3.6.egg/softphone/__pycache__/__init__.cpython-36.pyc

dep doc:
