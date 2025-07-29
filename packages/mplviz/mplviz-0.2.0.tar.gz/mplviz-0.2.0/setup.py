from setuptools import setup, find_packages

setup(
    name='mplviz',
    version='0.2.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    long_description=open('README.md', encoding='utf-8').read(),
    description='A fluent wrapper around matplotlib for easy, expressive visualizations',
    long_description_content_type='text/markdown',
    author='BBEK-Anand',
    url='https://github.com/BBEK-Anand/mplviz',  
    include_package_data=True,
    license='MIT',
    install_requires=[
        'matplotlib>=3.0.0',
        'numpy>=1.18.0',
        'ipython>=7.0.0'  
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Visualization',
        'Framework :: Matplotlib',
    ],
    python_requires='>=3.7',
)
