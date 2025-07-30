from setuptools import setup, find_packages

setup(
    name="k8s-speak",
    version="0.0.1",
    description="Natural language interface for Kubernetes and Amazon EKS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rohit Singh",
    author_email="c.ronnie.r@gmail.com",
    url="https://github.com/ImRohitSingh/k8s-speak",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["k8s_speak"],
    entry_points={
        "console_scripts": [
            "k8s-speak=k8s_speak:main",
        ],
    },
    install_requires=[
        "pyyaml",
        "colorama",
        "pyreadline3;platform_system=='Windows'",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.6",
    keywords="kubernetes, eks, kubectl, cli, natural language",
)