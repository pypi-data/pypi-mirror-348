from setuptools import setup, find_packages
import subprocess
import sys

def install_playwright_browsers():
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    except subprocess.CalledProcessError:
        print("Warning: Failed to install Playwright browsers. Please run 'playwright install' manually.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="talwar",
    version="0.1.1",
    author="anon",
    author_email="anontech100@gmail.com",
    description="AI-powered web application security testing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.9",
    install_requires=[
        "anthropic>=0.47.1",
        "beautifulsoup4>=4.13.3",
        "colorama>=0.4.6",
        "openai>=1.64.0",
        "playwright>=1.49.1",
        "PyYAML>=6.0.2",
        "Requests>=2.32.3",
        "tiktoken>=0.9.0"
    ],
    entry_points={
        "console_scripts": [
            "talwar=talwar.run:main",
        ],
    },
)

# Install Playwright browsers after package installation
install_playwright_browsers() 