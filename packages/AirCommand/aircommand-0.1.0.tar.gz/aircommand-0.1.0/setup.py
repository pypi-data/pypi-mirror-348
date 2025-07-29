from setuptools import setup, find_packages

setup(
    name='AirCommand',  # Package name on PyPI
    version='0.1.0',
    description='Control media players like Youtube, VLC, and Spotify using hand gestures.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Akshit',
    author_email='akshitprajapati24@gmail.com',
    url='https://github.com/akshit0942b/AirCommand',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'mediapipe',
        'pyautogui'
    ],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS',
    'Operating System :: MacOS :: MacOS X',
    ],
    python_requires='>=3.7',
)
