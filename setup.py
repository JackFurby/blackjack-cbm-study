from setuptools import setup

setup(
    name='study_app',
    version="0.0.1",
    packages=['study_app'],
    setup_requires=['libsass >= 0.6.0'],
    sass_manifests={
        'study_app': ('static/scss/', 'static/css', '/static/css')
    },
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
