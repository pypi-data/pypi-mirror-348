# Modern PySide UI Framework

The UI Framework for the era of experience.

一个现代化、模块化的PySide/Qt UI框架，提供丰富的自定义组件和视觉效果，帮助开发者快速构建美观且功能强大的桌面应用程序。

## 设计思路

### 模块化架构

本框架采用严格的模块化设计，将UI组件、样式和功能逻辑清晰分离：

- **核心模块** - 提供基础功能和工具类
- **组件模块** - 提供可复用的UI元素
- **窗口管理** - 提供自定义窗口框架
- **多媒体支持** - 提供媒体内容的显示和控制

### 面向对象设计

- 每个组件都封装为独立类，具有清晰的接口
- 利用继承和组合模式，便于功能扩展
- 通过信号槽机制实现组件间通信

### 主题与样式分离

- 采用样式表（StyleSheet）管理组件外观
- 支持动态主题切换（亮色/暗色模式）
- 组件外观与功能逻辑分离，便于定制

## 功能特征

### 共通功能

- **动画效果** - 提供流畅的过渡和交互动画
- **自动换行** - 智能文本处理和布局
- **颜色管理** - 统一颜色方案和调色板
- **配置系统** - 应用配置的读取和保存
- **异常处理** - 优雅捕获和处理UI异常
- **字体管理** - 自定义字体加载和渲染
- **图标系统** - 可缩放矢量图标支持
- **图像工具** - 图像处理和优化
- **页面路由** - 应用内导航和页面管理
- **平滑滚动** - 惯性滚动和平滑效果
- **多语言支持** - 国际化和本地化功能

### 现代化组件

- **日期时间** - 日历、时钟和日期选择器
- **对话框** - 模态和非模态对话框
- **布局系统** - 响应式和自适应布局
- **Material风格** - 符合Material Design规范的组件
- **导航元素** - 侧边栏、标签页和导航栏
- **设置界面** - 配置面板和偏好设置组件
- **通用组件** - 按钮、输入框、列表视图等基础组件

### 多媒体支持

- **媒体播放器** - 音频和视频播放控件
- **播放控制栏** - 播放、暂停、音量等控制
- **视频组件** - 视频内容展示和控制

### 窗口管理

- **Fluent风格窗口** - 现代Windows风格界面
- **启动屏幕** - 自定义应用启动画面
- **堆叠式组件** - 页面过渡和导航

## 使用示例

```python
from PySideUI.window.fluent_window import FluentWindow
from PySideUI.components.material.button import PrimaryButton
from PySideUI.common.theme_listener import ThemeManager

# 创建主窗口
window = FluentWindow(title="我的应用")

# 添加一个按钮
button = PrimaryButton(text="点击我")
button.clicked.connect(lambda: print("按钮被点击"))
window.centralWidget().layout().addWidget(button)

# 设置暗色主题
ThemeManager.getInstance().setTheme("dark")

# 显示窗口
window.create()
```

## 安装方法

```bash
pip install PySide6-Flex-UI
```

## 特色亮点

- **现代化美观界面** - 符合当代设计趋势
- **丰富的动画效果** - 提升用户体验
- **主题切换支持** - 亮色/暗色模式无缝切换
- **响应式设计** - 适应不同屏幕尺寸
- **高度可定制化** - 每个组件都可定制外观和行为
- **完善的文档** - 详细的API文档和使用示例

## 贡献与开发

欢迎提交Issue和Pull Request，共同改进这个框架！详细的开发指南和贡献规范请查看`CONTRIBUTING.md`文件。

## 许可证

MIT许可证 - 详见LICENSE文件