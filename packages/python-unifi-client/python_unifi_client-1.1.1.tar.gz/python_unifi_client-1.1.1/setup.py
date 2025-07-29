import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
		name="python_unifi_client",
		version="1.1.1",
		author="Michael Lapinski",
		author_email="michaellapinski787@gmail.com",
		descripton="A python version of a github Art-of-Wifi/Unifi-API-Client",
		long_description=long_description,
		long_description_content_type="text/markdown",
		url="https://github.com/compdat-llc/unifi-client-python",
		packages=setuptools.find_packages(),
		classifiers=(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		python_requires='>=3.8, <3.14'
	)