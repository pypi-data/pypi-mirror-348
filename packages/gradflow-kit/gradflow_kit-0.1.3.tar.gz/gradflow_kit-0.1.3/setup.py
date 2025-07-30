import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gradflow_kit",  
    version="0.1.3",
    author="N-T-Raghava",
    author_email="tanmairaghav3836@gmail.com",  
    description="A clean and modular auto-differentiation engine inspired by micrograd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/N-T-Raghava/GradFlow",
    packages=setuptools.find_packages(exclude=["tests*", "examples*", "notebooks*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "graphviz",
    ],
    include_package_data=True,
)
