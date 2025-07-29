from setuptools import setup, find_packages

setup(name='interpg',
      version='1.0.0',
      description='Fast bilinear interpolation of 2D or 3D gridded data along a line',
      author='Marcus Donnelly',
      author_email='marcus.k.donnelly@gmail.com',
      url='https://github.com/marcuskd/interpg',
      license='BSD 3-Clause',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering'
                   ],
      keywords=['Interpolation',
                'Grid'
                ],
      packages=find_packages(),
      install_requires=['numpy >= 1.26',
                        'numba >= 0.60'
                        ],
      include_package_data=True,
      )
