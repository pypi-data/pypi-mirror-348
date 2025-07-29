from setuptools import setup, find_packages

setup(
    name='leetbuddy',
    version='0.1.1',
    py_modules=['leetbuddy'],
    install_requires=[
        'click',
        'requests',
        'urllib3',
    ],
    entry_points={
        'console_scripts': [
            'leetbuddy=leetbuddy:cli',
        ],
    },
    author='Pradeep Elamurugu',
    author_email='your.email@example.com',
    description='A CLI tool for LeetCode daily problems and submissions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/leetbuddy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
