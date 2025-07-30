from setuptools import setup, find_packages

setup(
    name="auto-temp-gpiod-ctrl",
    version="0.1.2",
    description="Automatic temperature-based GPIO control for any libgpiod 2.x device.",
    author="Anthony",
    author_email="anthonyma24.development@gmail.com",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "gpiod>=2.0"
    ],
    entry_points={
        "console_scripts": [
            "auto-temp-gpiod-ctrl=auto_temp_gpiod_ctrl.main:main"
            # The following alias is deprecated and will be removed in future versions
            # "auto_temp_ctrl=auto_temp_gpiod_ctrl.main:main"
        ]
    },
    python_requires=">=3.7",
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
