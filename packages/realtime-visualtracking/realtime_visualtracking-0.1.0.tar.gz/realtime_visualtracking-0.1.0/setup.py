from setuptools import setup, find_packages

setup(
    name='realtime_visualtracking',
    version='0.1.0',
    author='Marcelo Viana Almeida',
    author_email='marcelovianademaria@gmail.com',
    description='Visual Tracking Platform Client',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/marceloviana/visualtracking-client',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.25.1'
    ],    
)
