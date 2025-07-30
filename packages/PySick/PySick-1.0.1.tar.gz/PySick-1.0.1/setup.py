from setuptools import setup, find_packages

setup(
    name="PySick",  # Keep this exact, capital P and S
    version="1.0.1",  # Update this every time you push a new version
    author="Your Name",
    author_email="your.email@example.com",
    description="A powerful 2D game development module using Pygame.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/PySick",  # Replace with your GitHub link
    project_urls={
        "Documentation": "https://github.com/yourusername/PySick#readme",
        "Source": "https://github.com/yourusername/PySick",
        "Tracker": "https://github.com/yourusername/PySick/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  # Automatically include all modules/folders
    python_requires=">=3.6",
    install_requires=[
        "pygame>=2.6.0",
    ],
    include_package_data=True,
    zip_safe=False,
)
