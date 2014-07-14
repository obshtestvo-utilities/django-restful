import os
from distutils.core import setup
from setuptools import find_packages
VERSION = __import__("restful").__version__
CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
]
install_requires = [
    'django>=1.4.1',
]
# taken from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)
for dirpath, dirnames, filenames in os.walk('restful'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[12:] # Strip "restful/" or "restful\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))
setup(
    name="django-restful",
    description="Django application to add features to the original admin",
    version=VERSION,
    author="Obshtestvo.bg",
    author_email="info@obshtestvo.bg",
    url="https://github.com/obshtestvo-utilities/django-restful",
    download_url="https://github.com/obshtestvo-utilities/django-restful/.../tgz",
    package_dir={'restful': 'restful'},
    packages=packages,
    package_data={'restful': data_files},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
)