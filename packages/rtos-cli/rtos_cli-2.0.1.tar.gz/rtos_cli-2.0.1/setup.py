from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rtos_cli',
    version='2.0.1',
    packages=find_packages(include=['rtos_cli', 'rtos_cli.*']),
    include_package_data=True,
    package_data={
        'rtos_cli': ['templates/**/*']
    },
    install_requires=[
        'pyyaml>=6.0',
        'pydot>=4.0.0',
        'networkx>=3.1',
        'graphviz>=0.20.1'
    ],
    entry_points={
        'console_scripts': [
            'rtos_cli = rtos_cli.rtos_cli:main',
        ],
    },
    author='Efrain Reyes Araujo',
    author_email='dev@reyes-araujo.com',
    description='CLI para automatizar proyectos PlatformIO con FreeRTOS en base a Framework Arduino y un ESP32',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/efrainra7/rtos_cli',  # ajustar si hay repo público
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Utilities'
    ],
    python_requires='>=3.7',
)