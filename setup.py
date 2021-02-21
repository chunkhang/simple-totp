import setuptools

setuptools.setup(
    name='simple-totp',
    version='1.0.0',
    author='Marcus Mu',
    author_email='chunkhang@gmail.com',
    description='A simple TOTP CLI',
    url='https://github.com/chunkhang/simple-totp',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
    packages=[
        'src'
    ],
    install_requires=[
        'pyotp>=2.6.0',
        'PyYAML>=5.4.1',
    ],
    entry_points={
        'console_scripts': [
            'otp=src.main:main'
        ]
    }
)
