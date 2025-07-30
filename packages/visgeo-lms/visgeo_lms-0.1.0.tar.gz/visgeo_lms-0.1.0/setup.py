from setuptools import setup, find_packages

setup(
    name="visgeo_lms",
    version="0.1.0",
    description="An interactive bivariate cartogram mapping tool with LLM support",
    author="Wang Zhe，Zhang Zuo，Zhang Rui，Jiang Yukun",
    author_email="wangzhecnc@163.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'visgeo_lms = visgeo_lms.__main__:main'
        ]
    },
    install_requires=[
        "PyQt5",
        "geopandas",
        "folium",
        "jenkspy",
        "openai",
        "numpy"
    ],
    python_requires='>=3.8',
)
