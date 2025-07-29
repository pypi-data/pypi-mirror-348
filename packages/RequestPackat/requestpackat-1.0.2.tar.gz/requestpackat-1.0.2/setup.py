from setuptools import setup, find_packages

setup(
    name='RequestPackat',
    version='1.0.2',
    description='Run Packat',
    author='Packed',
    author_email='oelfaesraali@gmail.com',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
