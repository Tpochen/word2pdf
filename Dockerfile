# 使用基于Linux的Docker镜像
FROM ubuntu:latest

# 设置工作目录
WORKDIR /app

# 更换软件源
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && apt-get install -y pandoc && apt-get clean
RUN apt-get install -y python3 python3-pip

#使用Unoconv
RUN apt-get install -y unoconv

# 安装 LibreOffice
RUN apt-get install -y libreoffice

# 启动 LibreOffice 侦听器
RUN unoconv --listener &

# 中文字体
COPY fonts/ /usr/share/fonts/truetype/
RUN fc-cache -f -v

# 复制项目文件到镜像中
COPY . /app

# 安装依赖
RUN pip3 install -r requirements.txt

# 暴露Django
EXPOSE 8000

# 启动Django服务器
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]