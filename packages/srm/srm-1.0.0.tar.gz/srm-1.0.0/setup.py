from setuptools import setup, find_packages

setup(
    name='my_model_lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'torchvision',
        'Pillow',
        'numpy'
    ],
    include_package_data=True,
    author='Носкова Екатерина',
    description='Суперразрешение с использованием SRCNN',
    entry_points={
        'console_scripts': [
            'srm = srm.__main__:main',  # команда srm вызовет функцию main() из srm/__main__.py
        ],
    },
)