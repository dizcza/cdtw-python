from distutils.core import setup, Extension

with open("README.md") as f:
    long_description = f.read()

setup(name='cdtw',
      version='0.1.0',
      description='Dynamic Time Warping in C with Python bindings',
      author="Danylo Ulianych",
      author_email="dizcza@gmail.com",
      install_requires=['numpy'],
      ext_modules=[Extension('lib.cdtw', sources=['cdtw/cdtw.c'])],
      license='MIT',
      long_description=long_description,
      url='https://github.com/dizcza/cdtw-python',
      classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: C',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
      ]
)

