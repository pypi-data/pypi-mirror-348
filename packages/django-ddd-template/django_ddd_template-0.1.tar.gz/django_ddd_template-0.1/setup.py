from setuptools import setup, find_packages

setup(
    name="django-ddd-template",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2"
    ],
    entry_points={
        'console_scripts': [
            'django-ddd=django_ddd_template.management.commands.startapp_ddd:Command.handle',
        ],
    },
    author="Osmel Mojena Dubet",
    description="Comando personalizado para crear apps Django con arquitectura DDD",
    zip_safe=False,
)