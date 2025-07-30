from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="django-ddd-template",
    version="0.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2"
    ],
    entry_points={
        'console_scripts': [
            'django-ddd=django_ddd_template.cli:main',
        ],
    },
    author="Tu Nombre",
    description="Crea apps Django con arquitectura DDD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    zip_safe=False,
)
