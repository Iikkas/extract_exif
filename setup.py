from setuptools import setup

setup(
    name="extract_exif",
    version="1.0",
    py_modules=["extract_exif"],
    entry_points={
        "console_scripts": [
            "extract_exif=extract_exif:main",
        ],
    },
)
