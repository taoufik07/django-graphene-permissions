import os

import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

about = {}

with open(os.path.join("django_graphene_permissions", "__version__.py")) as f:
    exec(f.read(), about)

setuptools.setup(
	name="django_graphene_permissions",
	version=about["__version__"],
	author="Taoufik Abbassid",
	author_email="abacidtaoufik@gmail.com",
	description="DRF like permission system",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/taoufik07/django-graphene-permissions",
	packages=setuptools.find_packages(),
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Framework :: Django",
		"Operating System :: OS Independent",
	],
)
