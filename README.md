## 以图搜图数据集建立说明

### 1.在本地建立query文件夹，存放100张query图片，分别命名为0-99.jpg

### 2.在本地建立correspondence文件夹，下面分别建立0-99号子文件夹，分别存放对应的0-99的query图片对应的相似图片

### 3.example
python establish_dataset.py --src_dir ./image/
note:最后一个斜杠是必要的

结果最后会返回一个result_时间的json文件，存储query和其对应的base的图片名称，以及上传到bucket的log日志。
