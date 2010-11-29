import os
from setuptools import setup

setup(
    name = "Personal Cluster Management",
    version = "0.0.1",
    author = "Zachary Goldberg",
    author_email = "zach@zachgoldberg.com",
    description = ("Tools and programs to manage your own unix machines"),
    license = "GPL",
    keywords = "ssh management cluster personal openssh",
    url = "http://packages.python.org/unix_pcm",
    packages=['pcm', 'pcm/models', 'pcm/common', 'pcm/commands'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPL License",
    ],
    entry_points = {
        "console_scripts": [
            "pcm_client = pcm.client:run",
            "pcm_master = pcm.master:run",
            "pcm_ui = pcm.ui:run",
            ],
        },
    
)

os.system("cp etc/pcm_client /etc/init.d")
os.system("chmod o+x /etc/init.d/pcm_client")
