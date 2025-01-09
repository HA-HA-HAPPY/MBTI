
# MBTI 性格测试程序

## 介绍

这是一个基于命令行的 MBTI（Myers-Briggs Type Indicator）性格测试程序。用户通过回答 18 个问题，程序将根据用户的回答生成一个 MBTI 类型，并提供相应的性格分析。同时，用户可以选择通过电子邮件接收结果。

## 特性

- 使用 `Fernet` 加密对敏感信息进行保护  
- 支持通过电子邮件发送测试结果  
- 支持命令行交互，适合个人使用  
- 提供独立运行的 EXE 文件，方便在 Windows 环境下运行  

## 安装和使用

### 环境和依赖  
#### Python 环境  
- Python 3.8 或更高  

#### 依赖库  
- Flask  
- smtplib  
- cryptography  

安装依赖：  
```bash  
pip install flask cryptography  
```

### 使用方法

1. 下载或克隆此项目。  
2. 确保已经安装了 Python 和必要的依赖。  
3. 运行 `main.py` 文件。  
4. 按照提示回答问题，并选择是否输入邮箱以接收测试结果。  

### EXE 文件

本项目已打包为 EXE 程序，直接双击 EXE 文件即可运行。无需安装 Python 环境，便捷的桌面应用。  

## 注意事项

- 该程序采用了加密方式存储敏感信息，请勿公开密钥以确保安全性。  
- 测试结果仅供参考，任何决策应根据个人实际情况做出。  
- 如有问题，请通过邮箱联系我：**351082290@qq.com**。

---

# MBTI Personality Test Program

## Introduction

This is a command-line-based MBTI (Myers-Briggs Type Indicator) personality test program. Users will answer 18 questions, and the program will generate an MBTI type based on the responses and provide corresponding personality analysis. Additionally, users can choose to receive the results via email.

## Features

- Uses `Fernet` encryption to protect sensitive information  
- Supports sending test results via email  
- Supports command-line interaction, suitable for personal use  
- Provides an EXE file for standalone operation, easy to run in a Windows environment  

## Installation and Usage

### Environment and Dependencies  
#### Python Environment  
- Python 3.8 or higher  

#### Required Libraries  
- Flask  
- smtplib  
- cryptography  

To install dependencies:  
```bash  
pip install flask cryptography  
```

### Usage

1. Download or clone this project.  
2. Ensure that Python and the necessary dependencies are installed.  
3. Run the `main.py` file.  
4. Follow the prompts to answer the questions and decide whether to input your email to receive the test results.  

### EXE File

This project has been packaged into an EXE program, which can be run directly by double-clicking the EXE file. No need to install Python, making it a convenient desktop application.  

## Notes

- The program uses encryption to store sensitive information; do not expose the key to ensure security.  
- The test results are for reference only, and any decisions should be made based on individual circumstances.  
- If you encounter any issues, feel free to contact me via email: **351082290@qq.com**.  

---
