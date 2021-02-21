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
    packages=setuptools.find_packages(),
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'otp=main:main'
        ]
    }
)
