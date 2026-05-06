# Hatch Pet Autowake

这是一个 Codex skill，用来从参考图生成 Codex 自定义桌面小宠物，安装宠物包，并在 macOS 上设置为每次启动 Codex 自动唤醒。

这个 skill 来自“小椰”的完整制作流程：生成宠物、打包、整理导出图片、重命名、设置为当前宠物，以及修复 Codex 重启后宠物不会自动出现的问题。

## 它能做什么

- 提醒用户上传合适的宠物参考图。
- 通过已有的 Codex `$hatch-pet` 流程生成宠物。
- 把最终宠物安装到 `$CODEX_HOME/pets/<id>`。
- 修改宠物显示名和描述。
- 设置该宠物为当前选中的 Codex 自定义宠物。
- 在 macOS 上安装 LaunchAgent，让宠物在 Codex 重启后自动显示。
- 在用户需要时，把生成图片和宠物包整理导出到一个文件夹。

## 安装方式

把下面这句话发给 Codex：

```text
$skill-installer install from https://github.com/Mmmmarvin/DFQ/tree/main/hatch-pet-autowake
```

安装完成后，重启 Codex，让新 skill 生效。

## 使用流程

注意：安装 skill 不等于已经生成宠物，也不等于已经开启自动唤醒。

完整流程是：

1. 安装这个 skill。
2. 重启 Codex。
3. 上传 3-6 张宠物参考图。
4. 对 Codex 发送类似这句话：

```text
$hatch-pet-autowake 请根据我上传的参考图生成一个 Codex 小宠物，安装它，并设置为每次启动 Codex 自动唤醒
```

自动唤醒会在宠物包生成并安装完成后配置，因为脚本需要知道最终宠物的 `pet-id`。

## 推荐上传哪些参考图

建议提供 3-6 张参考图：

- 正面或三分之四角度的清晰图。
- 如果宠物有不对称花纹、饰品、尾巴形状，最好提供侧面图。
- 眼睛、耳朵、毛色、花纹、道具等细节图。
- 一张能体现宠物性格或常见姿态的图。

参考图很重要，因为宠物不是单张图片。Codex 需要一个基础形象，再生成 9 组动作/表情。参考图越好，脸型、毛色、轮廓、花纹和道具越容易在所有动作里保持一致。

没有参考图也可以只用文字生成，但角色一致性可能更弱，后续可能需要更多修复。

## 9 个动作/表情

Codex 宠物使用固定 `8 x 9` 精灵图，每个格子是 `192 x 208` 像素。9 行分别是：

| 行 | 状态 | 帧数 | 触发条件或用途 |
| ---: | --- | ---: | --- |
| 0 | `idle` | 6 | 默认待机状态，也作为减少动画时的静态兜底。 |
| 1 | `running-right` | 8 | 拖动悬浮宠物向右移动时触发。 |
| 2 | `running-left` | 8 | 拖动悬浮宠物向左移动时触发。 |
| 3 | `waving` | 4 | 预留的打招呼/吸引注意动作；当前检查到的 Codex 版本里暂未发现自动触发，但图集仍需要这一行。 |
| 4 | `jumping` | 5 | 鼠标悬停或直接互动宠物时触发。 |
| 5 | `failed` | 8 | Codex 遇到阻塞或失败通知时触发。 |
| 6 | `waiting` | 6 | Codex 需要用户输入时触发。 |
| 7 | `running` | 6 | Codex 正在运行、思考或调用工具时触发。 |
| 8 | `review` | 6 | Codex 完成输出，等待用户查看时触发。 |

所有 9 行都应该生成，因为 Codex 读取的是固定图集布局。

## 文件说明

- `SKILL.md`：Codex skill 的主说明。
- `agents/openai.yaml`：skill 在 Codex 里的展示信息。
- `scripts/set-pet-name.py`：重命名/规范化宠物并设置为当前宠物。
- `scripts/install-autowake.py`：安装 macOS 自动唤醒助手。
- `scripts/export-pet-images.py`：整理导出生成图片和已安装宠物文件。
- `references/animation-states.md`：动作行、帧数、时长和触发条件说明。
- `references/xiaoye-case-study.md`：小椰这次实际制作过程中的记录。

## 说明

自动唤醒目前是 macOS 方案，因为它使用 LaunchAgent。宠物生成流程依赖 Codex 已有的 `$hatch-pet` 和 `$imagegen` 能力。
