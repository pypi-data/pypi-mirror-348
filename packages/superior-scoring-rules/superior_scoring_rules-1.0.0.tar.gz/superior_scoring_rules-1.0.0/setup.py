from setuptools import setup, find_packages

setup(
    name="superior-scoring-rules",  # Ensure this is unique on PyPI
    version="1.0.0",                 # Follow semantic versioning
    packages=find_packages(),
    install_requires=[               # List dependencies
        'tensorflow>=2.0.0',
    ],
    author="Rouhollah Ahmadian",
    author_email="ruhallah.ahmadian@gmail.com",
    description="PBS and PLL are superior evaluation metrics for probabilistic classifiers, fixing flaws in Brier Score (MSE) and Log Loss (Cross-Entropy). Strictly proper, consistent, and better for model selection, early stopping, and checkpointing.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Ruhallah93/superior-scoring-rules",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0.0',         # Specify compatible Python versions
)