from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-nepali-address-picker",
    version="0.1.0",
    author="Manish Kumar Rajak",
    author_email="manish.rajak2055@gmail.com",
    description="A Django package for Nepali address selection with dynamic form fields",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manishkumarrajak/nepali_address_picker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.2.0",
    ],
    include_package_data=True,
    package_data={
        'address_picker': [
            'templates/*',
            'templates/address_picker/*',
            'data/*',
        ],
    },
) 