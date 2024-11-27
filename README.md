# PyQt5音乐播放器

## 项目简介
这是一个使用PyQt5构建的跨平台音乐播放器，集成了Pygame音频回放和eyed3元数据解析功能。
(由于各个式解析方案不同，目前仅开发支持MP3格式，后续可能会补充)

![Image](https://github.com/aki-zone/pic-repo/blob/main/img/20241127202722.png?raw=true)
![Image](https://github.com/aki-zone/pic-repo/blob/main/img/20241127202750.png?raw=true)



## 特性
- 音量调节
- 播放列表管理
- 音频目录选择
- 歌手/时长等信息展示
- 专辑封面展示
- 播放/暂停控制
- 上一首/下一首
- 有序/随机/单曲循环播放
- 重启后按配置文件恢复上一次状态

## 项目结构
```
music-player/
│
├── audio.py         # 音频处理核心逻辑
├── form.py          # 界面设计
├── main.py          # 主程序入口
├── run.py           # 启动脚本
└── resources/       # icon资源文件夹
```

## 开发环境
- Python 3.x
- PyQt5
- Pygame
- eyed3

## 运行方式
```bash
python run.py
```

## 版权声明

本项目采用 [MIT 开源许可证](https://opensource.org/licenses/MIT) 进行许可。

版权所有 © [0xAki]，2023。保留所有权利。

