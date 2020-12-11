from setuptools import find_packages, setup

setup(
    name='ProjectDatabase',
    version='1.0.0',
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'alembic>=1.4.3',
        'click>=7.1.2',
        'Flask>=1.1.2',
        'Flask-Login>=0.5.0',
        'Flask-Migrate>=2.5.3',
        'Flask-Script>=2.0.6',
        'Flask-SQLAlchemy>=2.4.4',
        'itsdangerous>=1.1.0',
        'Jinja2>=2.11.2',
        'Mako>=1.1.3',
        'MarkupSafe>=1.1.1',
        'python-dateutil>=2.8.1',
        'python-editor>=1.0.4',
        'setuptools>=50.3.2',
        'six>=1.15.0',
        'SQLAlchemy>=1.3.20',
        'Werkzeug>=1.0.1'
    ],
)