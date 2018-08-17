from setuptools import setup, find_packages

install_requires = [
    'Flask==1.0.2'
    ]

setup(
    name			= 'kakaobot.py',
    version			= '__version__',
    description		= 'API wrapper for Kakaotalk written in Python.',
    author			= 'Katinor',
    author_email	= 'katinor@4ears.net',
	license			= 'MIT',
    packages		= find_packages(),
	url				= 'https://github.com/Katinor/kakaobot.py',
	download_url	= 'https://github.com/Katinor/kakaobot.py',
	install_requires= install_requires,
	keywords		= ['kakaotalk','chatbot'],
	python_requires = '>=3.6',
	classifiers		= [
		'Programming Language :: Python :: 3.6'
	]
)