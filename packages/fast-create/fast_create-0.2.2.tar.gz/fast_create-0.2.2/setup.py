from setuptools import setup, find_packages

setup(
    name="fast-create",
    version="0.2.2",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["temp/**/*", "temp/*"]},  # Include all files in temp
    py_modules=["fast_create"],
    install_requires=[
        'fastapi[all]', 'alembic', 'uvicorn', 'python-dotenv', 'psycopg2-binary', 
        'sqlmodel', 'fastapi_mail', 'pydantic', 'python-jose[cryptography]', 
        'oauth2', 'passlib', 'sqlalchemy'
    ],
    entry_points={
        "console_scripts": [
            "fast-create=fast_create:main",
        ],
    },
)
