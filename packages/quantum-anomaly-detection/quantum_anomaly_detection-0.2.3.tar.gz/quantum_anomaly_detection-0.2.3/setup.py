from setuptools import setup, find_packages


setup(

    name='quantum-anomaly-detection',
    version='0.2.3',
    author='Mohamed Malek Al Fakih & Abdellah Bichlifen',
    author_email='your.email@example.com',
    description='A Python package for quantum-based anomaly detection.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MalekAlFakih/SciPy',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.8',
    install_requires=['numpy', 'qiskit', 'matplotlib', 'jupyter'],
    include_package_data=True,
    zip_safe=False,
)
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],