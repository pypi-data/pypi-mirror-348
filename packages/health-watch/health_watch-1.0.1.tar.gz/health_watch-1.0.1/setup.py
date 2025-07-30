from setuptools import setup, find_packages

setup(
    name='health-watch',
    version='1.0.1',
    description='Cross-platform system monitoring utility',
    author='Yashwant Jain',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'sysmon=system_monitor.client.agent:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)