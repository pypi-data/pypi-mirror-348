from setuptools import setup, find_packages

setup(
    name="apptronik-autopilot",
    version="0.1.0",
    description="AI-powered autopilot protocol for Web3 and DeFi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Apptronik AI",
    author_email="support@apptronik-ai.org",
    url="https://github.com/Apptronik-AI/autopilot",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "web3",
        "requests",
        "python-dotenv",
        "cryptography",
        "fastapi",
        "uvicorn",
        "prometheus_client"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 