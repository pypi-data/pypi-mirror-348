from setuptools import setup, find_packages

setup(
    name='ChatSelfbot',
    version='1.1.1',
    description='A fast and light selfbot made by Bjarnos for Chat (a program by Jona Zwetsloot)!',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Bjarnos',
    author_email='contact@bjarnos.dev',
    url='https://github.com/Bjarnos/SelfbotSource',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'ChatSelfbot': ['images/*.png', 'images/*.webp', 'images/*.jpg', 'images/*.jpeg', 'images/*.gif'],
    },
    include_package_data=True,
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    setup_requires=['setuptools >= 77.0.3'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
