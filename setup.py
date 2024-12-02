from distutils.core import setup

setup(
    name='FiniteElement',
    version='0.2',
    author='Robert Brown',
    description='Simple Finite Element Solver',
    url='https://github.com/robertbrown2/FiniteElement',
    python_requires='>=3.8',
    install_requires=['numpy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    py_modules=[],
    test_suite='tests',
)
