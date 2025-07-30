from setuptools import setup, find_packages
def parse_requirements(filename):
    """读取 requirements.txt 文件并返回依赖列表"""
    with open(filename, 'r') as f:
        # 去除空行、注释和多余的空格
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]
setup(
    name="spinqit_task_manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'spinqit-task-manager=spinqit_task_env.qasm_submitter:run_server',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A task manager for submitting QASM tasks to SpinQ Cloud via MCP",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/spinqit_task_manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)