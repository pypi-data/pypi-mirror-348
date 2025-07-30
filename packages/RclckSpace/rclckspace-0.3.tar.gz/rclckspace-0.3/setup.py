from setuptools import setup, find_packages

setup(
    name="RclckSpace",
    version="0.3",
    packages=find_packages(),
    install_requires=["requests"],
    author="RostorVLasov",
    description="API для сокращения ссылок через rclck.space",
    url="https://github.com/your-repo/rclckspace",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)