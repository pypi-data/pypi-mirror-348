from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='mediagesture',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'mediapipe',
        'pyautogui'
    ],
    entry_points={
        'console_scripts': [
            'mediagesture = mediagesture.main:run'
        ]
    },
    author='Akshum',
    author_email='akshum20@gmail.com',
    description='Control media players with hand gestures using OpenCV and Mediapipe',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/akshumgarg/mediacontroller',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
