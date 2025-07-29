import os
from setuptools import setup, find_packages

setup(
    name="fs_comfyui_frontend_package",
    version=os.getenv("COMFYUI_FRONTEND_VERSION") or "1.20.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.9",
    description="ComfyUI Frontend Package for web interface",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
