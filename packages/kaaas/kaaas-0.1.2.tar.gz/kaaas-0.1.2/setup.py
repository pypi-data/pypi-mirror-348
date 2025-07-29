from setuptools import setup, find_packages

setup(
    name="kaaas",
    version="0.1.2",
    packages=find_packages(include=["kaaas", "kaaas.*"]),
    install_requires=[
        'boto3',
        'pyyaml',
    ],
    author="Kashif Rafi",
    author_email="rafi.kashif@yahoo.com",
    description="Kubernetes AI-powered Cluster Analysis and Solution (KAAAS)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="Proprietary",
    url="https://github.com/yourusername/kaaas",
    keywords=["kubernetes", "ai", "cluster", "analysis", "k8sgpt", "llm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Monitoring",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        'console_scripts': [
            'kaaas=kaaas.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'kaaas': [
            'pyarmor_runtime_000000/*',
            'pyarmor_runtime_000000/**/*',
        ],
    },
    python_requires='>=3.6',
)

