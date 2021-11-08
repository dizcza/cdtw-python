from distutils.core import setup, Extension

setup(name='cdtw',
      version='0.1.0',
      description='Dynamic Time Warping in C',
      requires=['numpy'],
      ext_modules=[Extension('lib.cdtw', sources=['cdtw/cdtw.c'])])
