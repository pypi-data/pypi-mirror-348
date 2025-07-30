from setuptools import setup, find_packages

setup(
    name='tl_exp',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
        'matplotlib',
        'numpy',
        'seaborn',
        'pandas',
        'scikit-learn',
    ],
    author='mhmd-sameer',
    author_email='mohammedsameer20662@gmail.com',
    description='Transfer Learning Experiments (1 to 10)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/tl_exp',  # Optional: GitHub repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
