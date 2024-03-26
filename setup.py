from setuptools import setup, find_packages

setup(
    name="protectedAdminMiddleware",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django app to restrict access based on internal IPs.',
    url='https://github.com/ARezaK/ProtectedAdminMiddleware',
    install_requires=[
        "Django>=2.0",  # Ensure you list all necessary dependencies
    ],
    author='ARezaK',
    author_email='Jimmyeatscrickets@blishblashbloosh.com',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)
