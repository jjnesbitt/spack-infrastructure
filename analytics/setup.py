from pathlib import Path

from setuptools import find_packages, setup

readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    with readme_file.open() as f:
        long_description = f.read()
else:
    # When this is first installed in development Docker, README.md is not available
    long_description = ""

setup(
    name="analytics",
    version="0.1.0",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    author="Kitware, Inc.",
    author_email="kitware@kitware.com",
    keywords="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django :: 5.1",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python",
    ],
    python_requires=">=3.13",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cachetools",
        "celery[redis]",
        "dj-database-url",
        "dj-email-url",
        "django-click",
        "django-configurations[database,email]",
        "django-cors-headers",
        "django-extensions",
        "django-girder-utils",
        "django-ninja",
        "django-s3-file-field[minio]",
        "django~=5.1",
        "gunicorn",
        "opensearch-dsl",
        "kubernetes",
        "sentry-sdk[django,pure_eval]",
        "rich",
        "psycopg2-binary",
        "python-gitlab>=5.2.0",
        "pyyaml",
        "requests",
        "tqdm",
        "whitenoise[brotli]",
    ],
    extras_require={
        "dev": [
            "types-cachetools",
            "django-debug-toolbar",
            "ipython",
            "tox",
        ]
    },
)
