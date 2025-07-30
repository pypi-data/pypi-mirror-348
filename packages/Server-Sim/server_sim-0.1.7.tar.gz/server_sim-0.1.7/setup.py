from setuptools import find_packages, setup

# special encoding for READMA.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Server_Sim",                   
    version="0.1.7",                    
    author="Zero",
    description='A WebSocket server that handles chunked data transfer with ACK/request flow.',
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/Zero-00-00",  
    packages=find_packages(),           
    install_requires=[                   
        "requests>=2.25.1",
        "numpy",
        "websockets>=10.0"
    ],
    classifiers=[                      
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',           
)
