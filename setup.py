from setuptools import setup

setup(name='softphone',
      version='0.1',
      description='Python library for performing phone calls using PJSIP/PJSUA, with audio streaming. Inspired by "soft_phone" by gfarrow.',
      url='https://github.com/DiscordPhone/softphone',
      author='Nicolai Prebensen',
      author_email='nicolaiprebensen93@gmail.com',
      license='MIT',
      packages=[
            'softphone',
      ],
      python_requires='>=3.6',
      keywords='phone call sip softphone python',
      classifiers=[
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
      ],
      zip_safe=False)
