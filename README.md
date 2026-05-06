# DFQ

My first GitHub project: a Codex skill that helps create a custom desktop pet, install it, and make it auto-wake when Codex starts.

The skill lives in [`hatch-pet-autowake/`](hatch-pet-autowake/).

## Install

Send this to Codex:

```text
$skill-installer install from https://github.com/Mmmmarvin/DFQ/tree/main/hatch-pet-autowake
```

Then restart Codex so it can load the newly installed skill.

## Important

Installing this skill only teaches Codex the workflow. It does not immediately create a pet or enable auto-wake by itself.

After restart, ask Codex something like:

```text
$hatch-pet-autowake 请根据我上传的参考图生成一个 Codex 小宠物，安装它，并设置为每次启动 Codex 自动唤醒
```

The auto-wake step runs after the pet package exists. On macOS, the skill installs a LaunchAgent that keeps the selected custom pet visible after Codex restarts.

## What Users Should Prepare

For best results, upload 3-6 reference images:

- Front or three-quarter view.
- Side view if markings or accessories are asymmetric.
- Face/detail images for eyes, ears, colors, markings, or props.
- One image that captures the pet's personality or typical pose.

Reference images matter because Codex pets are animated. The generator needs one base image plus 9 animation states, and references help keep the same face, colors, markings, silhouette, and props across every state.
