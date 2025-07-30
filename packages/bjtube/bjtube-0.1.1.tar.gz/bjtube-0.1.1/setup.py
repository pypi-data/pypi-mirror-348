from setuptools import setup, find_packages

setup(
    name='bjtube',
    version='0.1.1',
    description='A YouTube downloader with faster speed, ffmpeg is essential to use before installation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Babar Ali Jamali',
    author_email='babar995@gmail.com',
    url='https://github.com/babaralijamali/bjtube',
    packages=find_packages(),
    install_requires=[
        'yt-dlp'
    ],
    entry_points={
        'console_scripts': [
            'bjtube=bjtube:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
