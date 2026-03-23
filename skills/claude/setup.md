# Claude Code CLI 环境检测与安装引导

当用户首次使用 `/claude` 时，按以下步骤检测环境：

## 1. 检测 Claude CLI

```bash
which claude 2>/dev/null && claude --version || echo "CLAUDE_NOT_FOUND"
```

- 如果输出 `CLAUDE_NOT_FOUND`，提示用户：

```
Claude Code CLI 未安装。需要先安装才能使用 /claude skill。

安装命令：
  npm install -g @anthropic-ai/claude-code

安装完成后请运行 `claude auth login` 进行认证。
```

- 如果已安装，继续检测认证状态。

## 2. 检测认证状态

```bash
claude -p --output-format json --no-session-persistence "echo test" 2>&1 | head -5
```

- 如果输出包含 `auth` 或 `unauthorized` 相关错误，提示用户：

```
Claude Code CLI 已安装但未认证。请运行：
  claude auth login
```

## 3. 检测结果处理

- **全部通过** → 正常执行 skill
- **任一失败** → 展示上述提示，不执行子进程任务
