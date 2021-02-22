import setuptools

from otp import cli

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='simple-totp',
    version=cli.VERSION,
    author='Marcus Mu',
    author_email='chunkhang@gmail.com',
    description=cli.DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chunkhang/simple-totp',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
    packages=[
        'otp'
    ],
    install_requires=[
        'pyotp>=2.6.0',
        'PyYAML>=5.4.1',
    ],
    entry_points={
        'console_scripts': [
            'otp=otp.cli:main'
        ]
    }
)
