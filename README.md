# arxiver: arxiv 论文下载工具

## arxiv 功能

- [ ] 搜索论文
- [x] 单个链接下载论文
- [x] Markdown 文件(夹)自动识别链接并批量下载论文, 同步更新 Markdown 文件内容

## 安装方法

```
git clone git@github.com:huxycn/arxiver.git
pip install arxiver
```

## 使用方法

1. 单个链接下载论文
```
arxiver url <ARXIV_URL> [<DIRECTORY>]
```
示例:
```
arxiver url https://arxiv.org/abs/1706.03762
```

2. Markdown 文件(夹)下载论文

```
arxiver md <MD_FILE_OR_DIR> [<DIRECTORY>]
```
Markdown 文件内 arxiv 链接需遵循正则表达式: `{{https://arxiv.org/abs/\d{4}.\d{5}}}`, 才会被自动识别并替换

示例:
```
arxiver md ./tests/mds/test.md
```
