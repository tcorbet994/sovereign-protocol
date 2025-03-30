from setuptools import setup, find_packages

setup(
    name="sovereign-control",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "websockets>=12.0",
        "aiohttp>=3.9.1",
        "cryptography>=41.0.7",
        "numpy>=1.26.2",
        "pandas>=2.1.3",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "flake8>=6.1.0",
            "black>=23.11.0",
            "mypy>=1.7.1",
        ],
    },
    python_requires=">=3.8",
    author="Sovereign Control Protocol Team",
    author_email="security@sovereign-protocol.org",
    description="A secure, consciousness-aware interface for autonomous LLM interaction",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sovereign-protocol",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 