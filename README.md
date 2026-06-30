<div align="center">
  <h1>BlenderBatchRenderer 🚀</h1>
  <p>
    <a href="#-简体中文-simplified-chinese">🇨🇳 简体中文</a> | 
    <a href="#-english">🇺🇸 English</a>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Platform-Windows-blue" alt="Platform">
    <img src="https://img.shields.io/badge/Python-3.8%2B-green" alt="Python">
    <img src="https://img.shields.io/badge/License-MIT-brightgreen" alt="License">
  </p>
</div>

---
## <a href="https://www.creem.io/payment/prod_7QIBzy9UMvbaxN0HDHlxOE" target="_blank">Support me on Creem </a><br>thanks<br>

## 🇨🇳 简体中文 (Simplified Chinese)

**BlenderBatchRenderer** 是一款纯本地、轻量级 Blender 批量渲染队列管理工具。基于 Python 和 PyQt6 开发，旨在解决重度 3D 渲染工作流中频繁手动切换工程、内存泄漏崩溃以及系统资源被完全挤占等痛点。

### 🖥️ 界面预览<br>
<img width="1185" height="1080" alt="Screenshot 2026-06-30 095158" src="https://github.com/user-attachments/assets/05f30b00-bc09-4e6a-989f-7758fd9567d3" />
<br><br>

### ✨ 核心特性

- **🎯 直观的多任务队列管理**<br>
  - 支持直接拖拽 `.blend` 文件导入任务队列。<br>
  - 自动后台静默提取工程参数（场景、摄像机、分辨率、输出路径、起始/结束帧等）。<br>
  - 支持快捷复制任务、重置状态，多角度/多摄像机渲染一键搞定。<br><br>

- **⚙️ 精准的资源与进程控制**<br>
  - **CPU 核心分配**：支持限制渲染进程使用 25%、50%、75% 或 100% 的 CPU 资源，让你在后台渲染的同时也能流畅进行其他工作。<br>
  - **单帧独立进程防溢出**：对于包含复杂物理结算或大量 SSS 材质的大型工程，可开启“每帧独立渲染”功能。软件会在每渲染完一帧后自动杀死进程并重启，从根本上杜绝越渲越慢和内存泄漏。<br><br>

- **🛠️ 强大的自定义渲染逻辑**<br>
  - **自定义帧渲染**：支持任意无规律帧号组合（例如：`1, 5, 10`），并具备强大的格式容错机制。<br>
  - **自动漏帧补渲**：一键扫描输出目录，自动比对并填入未成功渲染的缺失帧，断电或崩溃后无需从头再来。<br>
  - **多维度进度监控**：UI 实时解析 Blender 底层日志，精确显示至 Tile（区块）和 Sample（采样）级别的当前帧进度监控。<br><br>

- **🔌 自动化后处理**<br>
  - 队列全部完成后，支持自动执行 **关机**、**重启** 或 **睡眠** 操作，安心挂机过夜。<br><br>

### 📦 环境依赖与运行<br>
由于底层调用了特定的系统 API，本项目**目前仅支持 Windows 系统**。<br><br>

### 💬 联系作者<br>
由 舟午YueMoon 开发。<br>
如果你有任何建议、遇到了 BUG，或者单纯想催更，欢迎在B站/Youtube相关视频的评论区告诉我！<br>
博客：http://yuemoon.vip/<br>
GitHub：@YueMoon99<br>
B站：UID223633562<br>
YouTube：@YueMoon99<br><br>

---<br><br>

## 🇺🇸 English<br>
**BlenderBatchRenderer** is a purely local, lightweight Blender batch rendering queue management tool designed specifically for the Windows platform. Developed with Python and PyQt6, it aims to solve common pain points in heavy 3D rendering workflows, such as frequent manual project switching, memory leak crashes, and total system resource exhaustion.<br><br>

### 🖥️ UI Preview<br>
<img width="1185" height="1080" alt="Screenshot 2026-06-30 095212" src="https://github.com/user-attachments/assets/359e6a5a-05ae-4830-b61c-add210263f3e" />
<br><br>

### ✨ Core Features<br>
- **🎯 Intuitive Multi-Task Queue Management**<br>
  - Supports importing tasks by directly dragging and dropping `.blend` files.<br>
  - Automatically extracts project parameters in the background (scene, camera, resolution, output path, frame ranges, etc.).<br>
  - Easily duplicate tasks or reset statuses to quickly set up multi-angle/multi-camera renders.<br><br>

- **⚙️ Precise Resource & Process Control**<br>
  - **CPU Core Allocation**: Limit the rendering process to use 25%, 50%, 75%, or 100% of CPU resources, allowing you to browse the web or work smoothly while rendering in the background.<br>
  - **Per-Frame Independent Process**: For large projects with complex physics calculations or SSS materials, enable the "Independent Process" feature. The software will automatically kill and restart the Blender process after each frame, fundamentally preventing slowdowns and memory leaks.<br><br>

- **🛠️ Powerful Custom Rendering Logic**<br>
  - **Custom Frame Rendering**: Supports any irregular combination of frame numbers (e.g., `1, 5, 10`) with strong format fault tolerance.<br>
  - **Auto-Fill Missing Frames**: One-click scan of the output directory to automatically compare and fill in missing frames that failed to render. No need to start over after a power outage or crash.<br>
  - **Multi-Dimensional Progress Monitoring**: The UI parses Blender's underlying logs in real-time, displaying current frame progress accurately down to the Tile and Sample level.<br><br>

- **🔌 Automated Post-Processing**<br>
  - After the queue is fully completed, supports automatic **Shut Down**, **Restart**, or **Sleep** operations for peace of mind during overnight rendering.<br><br>

### 📦 Requirements & Execution<br>
Because it calls specific system APIs, this project **currently only supports Windows OS**.<br><br>

### 💬 Contact<br>
Blog：http://yuemoon.vip/<br>
GitHub：@YueMoon99<br>
Blibili：UID223633562<br>
YouTube：@YueMoon99<br>
