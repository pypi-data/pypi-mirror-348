import setuptools

setuptools.setup(
	name="plockchain",
	version="2025.05.19",
	author="nquangit",
	license="MIT",
	author_email="nquang.it.04@gmail.com",
	description="plockchain support for send request flow by write yaml config file",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=open("requirements.txt").read().split(),
	url="https://github.com/nquangit/plockchain",
	classifiers=[
		"Programming Language :: Python :: 3"
	],
	keywords=["nquangit", "plockchain"],
	packages=["plockchain"],
)