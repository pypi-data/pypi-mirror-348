from setuptools import setup, find_packages

setup(
    name='Vantora',
    version='1.0.3',
    description='A powerful cryptographic and utility library for advanced encryption and decryption techniques',
    long_description=open('README.txt').read(),
    long_description_content_type='text/plain',
    author='Nexia',
    author_email='nasrpy88@gmail.com',
    url='https://t.me/NexiaHelpers',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    install_requires=[],
    python_requires='>=3.8',
)