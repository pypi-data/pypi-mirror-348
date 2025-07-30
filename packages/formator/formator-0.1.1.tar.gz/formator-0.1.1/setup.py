from setuptools import setup, find_packages

setup(
    name='formator',                    
    version='0.1.1',                      
    description='A package for formatting dict, list, tuple, etc.',        
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Oracle Yuan',
    author_email='youremail@example.com',
    url='https://github.com/yourname/mygreatpkg',  # 项目主页（GitHub 地址等）
    packages=find_packages(),              # 自动找到所有子包
    classifiers=[                          # 元信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
