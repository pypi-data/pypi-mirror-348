from setuptools import setup, find_packages

setup(
    name="pdf2imgCrop",
    version="0.1.0",
    packages=find_packages(),
    url="https://github.com/muxkin/pdf2imgCrop",
    project_urls={
        "Bug Tracker": "https://github.com/muxkin/pdf2imgCrop/issues",
        "Source Code": "https://github.com/muxkin/pdf2imgCrop",
    },
    install_requires=[
        "PyMuPDF",
        "Pillow",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "pdf2imgcrop=pdf2imgCrop.__main__:main",
        ],
    },
    author="Muxkin",
    description="将PDF文件转换为图片并自动裁剪空白边距",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="pdf, image, convert, crop",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
