from setuptools import setup, find_packages

setup(
    name="gozero-signature-python",
    version="0.1.0",
    py_modules=["gozero_signature"],
    install_requires=[
        "pycryptodome>=3.15.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Python implementation of go-zero framework signature functionality",
    keywords="go-zero, security, signature, encryption",
    python_requires=">=3.6",
)