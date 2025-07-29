from setuptools import setup

setup(name="Gaussian_Elimination_Libraries",
      version="1.1",
      packages=['uGauss'],#follows naming convention of uDesmos, as it is the small
      install_requires=['numpy>=2.2.5'],
      author="YusufA442",
      author_email="yusuf365820@gmail.com",
      license='Creative Commons Attribution-Noncommercial-Share Alike license',
      long_description=open('readme.txt').read())