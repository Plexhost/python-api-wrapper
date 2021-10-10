import setuptools
with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="api",
    version="0.0.1",
    description="Plexhost API Wrapper",
    author="SIMON#1386",
    license="MIT",
    install_requires=["requests"],
    package_dir={"": "api"},
    packages=setuptools.find_packages(where="api"),
    python_requires=">=3.6",
    url="https://github.com/plexhost/plexhost-api-wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
