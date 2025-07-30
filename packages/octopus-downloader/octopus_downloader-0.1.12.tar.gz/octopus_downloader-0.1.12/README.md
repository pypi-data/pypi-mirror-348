# Octopus的视频下载器

## 更新发布方法
```shell
source .venv/bin/activate
python upload_pypi.py
```

## 开发环境中运行命令行
```ssh
python -m octopus_downloader.main [subcommand] [...args]
```

## 安装
```sh
pip install octopus-downloader
```

## 使用说明
### 检查是否设置TIKHUB_API_KEY
```shell
odl checkenv TIKHUB_API_KEY
```
### 设置TIKHUB_API_KEY
```shell
odl setenv TIKHUB_API_KEY [API_KEY_VALUE]
```
### 获取视频信息
```shell
odl info [视频分享地址]
```
### 下载视频文件
```shell
odl download 视频分享地址 视频保存目录 [-f 视频保存文件名]
```