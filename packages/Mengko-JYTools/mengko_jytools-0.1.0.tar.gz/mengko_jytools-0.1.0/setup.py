from setuptools import setup, find_packages

setup(
    name="Mengko_JYTools",
    version="0.1.0",
    description="剪映草稿文件生成和处理工具",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Mengko",
    author_email="your_email@example.com",  # 记得修改为您实际的邮箱
    url="https://github.com/Mengko/JYtools",  # 可选，项目主页或代码仓库
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "Mengko_JYTools": ["draft_content_template.json", "metadata/*.json"],
    },
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 请根据您的实际许可证修改
        "Operating System :: OS Independent",
    ],
) 