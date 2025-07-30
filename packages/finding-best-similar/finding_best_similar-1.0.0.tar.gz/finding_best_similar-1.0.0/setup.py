from setuptools import setup, find_packages

setup(
    name='finding_best_similar',
    version='1.0.0',
    description='Finding Best Similar (FBS) Method',
    author='Ali Forouzan, Hadi Sadoghi Yazdi',
    author_email='ali.forouzan7@gmail.com',
    packages=find_packages(include=['finding_best_similar', 'finding_best_similar.*']),
    install_requires=[
        "scipy",
        "numpy",
        "pandas",
        "matplotlib",
        "tqdm",
    ],
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    keywords='Time Series Similarity, Pattern Matching, Information Theory , Elastic Matching, Finding Best Similar',
    include_package_data=True,
    project_urls={
        'Bug Reports': 'https://github.com/phoorooz/FBS/issues',
        'Source': 'https://github.com/phoorooz/FBS',
    }
)
