from setuptools import setup, find_packages

setup(
    name='deployment-info',
    version='1.2.11',
    packages=find_packages(),
    description='deployment-info',
    long_description_content_type='text/plain',
    long_description='This Python library provides a simple interface for retreiving the system deployment information.',
    url='https://github.com/pbullian/k8s_deployments_info',
    download_url='https://github.com/pbullian/k8s_deployments_info',
    project_urls={
        'Documentation': 'https://github.com/pbullian/k8s_deployments_info'},
    author='Tom Christian',
    author_email='tom.christian@openxta.com',
    python_requires='>=3.6',
    platforms=['Linux'],
    license='MIT',
    install_requires=[
        'loguru',
        'cpjson',
        'pydantic',
    ],
)
