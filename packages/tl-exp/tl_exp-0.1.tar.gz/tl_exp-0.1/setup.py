from setuptools import setup, find_packages

setup(
    name='tl-exp',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
        'numpy',
        'matplotlib',
        'seaborn',
        'pandas',
        'scikit-learn'
    ],
    author='Your Name',
    author_email='your@email.com',
    description='Transfer learning experiments package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/tl_exp',  # optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
