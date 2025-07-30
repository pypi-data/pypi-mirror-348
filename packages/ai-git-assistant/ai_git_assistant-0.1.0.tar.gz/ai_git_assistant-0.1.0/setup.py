from setuptools import setup, find_packages

setup(
    name="ai-git-assistant",
    version="0.1.0",
    author="Luis Gonzalez",
    author_email="luisgnzhdz@gmail.com",
    description="Asistente inteligente para atuomatizar tareas de Git y GitHub",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LuisGH28/git_assitant",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=[
        "scikit-learn",
        "numpy",
        "joblib",
    ],
    entry_points={
        "console_scripts": [
            "ai-git-assistant=git_assistant.__main__:main",
        ],
    },
)

