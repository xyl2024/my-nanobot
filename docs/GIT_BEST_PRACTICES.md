# Git 最佳实践

> 个人开发者适用指南

## 分支策略

```
main      ──────── 线上稳定版本
  │
  └── dev  ────── 开发主分支
        │
        ├── feature/xxx  功能分支
        └── bugfix/xxx   修复分支
```

### 分支说明

| 分支 | 用途 | 备注 |
|------|------|------|
| `main` | 线上稳定版本 | 永远保持能用的状态 |
| `dev` | 开发主分支 | 日常开发的主战场 |
| `feature/xxx` | 新功能开发 | 开发完成后合并到 dev |
| `bugfix/xxx` | bug 修复 | 修复完成后合并到 dev |

---

## 常用命令速查表

| 场景 | 命令 |
|------|------|
| 克隆仓库 | `git clone <仓库地址>` |
| 创建新分支 | `git checkout -b <分支名>` |
| 切换分支 | `git checkout <分支名>` |
| 查看当前状态 | `git status` |
| 查看提交历史 | `git log --oneline` |
| 查看差异（未暂存） | `git diff` |
| 查看差异（已暂存） | `git diff --staged` |
| 暂存所有修改 | `git add .` |
| 提交修改 | `git commit -m "描述"` |
| 推送到远程 | `git push` |
| 拉取更新 | `git pull` |
| 查看分支列表 | `git branch` |
| 删除本地分支 | `git branch -d <分支名>` |

---

## 每日工作流

### 开发新功能

```bash
# 1. 每天开始工作，先拉最新代码
git checkout dev
git pull

# 2. 创建新功能分支
git checkout -b feature/我要开发的功能

# 3. 开发中... 多次提交
git add .
git commit -m "完成了xxx功能"

# 4. 开发完成，合并回 dev
git checkout dev
git merge feature/我要开发的功能

# 5. 推送到远程
git push
```

### 修复 Bug

```bash
# 1. 从 main 创建修复分支
git checkout main
git checkout -b bugfix/问题描述

# 2. 修复并测试通过后，合并到 main 和 dev
git checkout main
git merge bugfix/问题描述
git checkout dev
git merge bugfix/问题描述

# 3. 清理分支
git branch -d bugfix/问题描述
git push
```

---

## 同步上游项目

如果你的项目是从别人那里 fork 的，想保持同步更新：

### 1. 添加上游远程仓库

```bash
git remote add upstream git@github.com:原作者/project.git
```

### 2. 拉取原项目更新

```bash
# 获取上游更新
git fetch upstream

# 合并到你的 main 分支（merge 方式）
git checkout main
git merge upstream/main

# 或者使用 rebase（线性历史）
git checkout dev
git rebase upstream/main
```

### 3. 推送到你的远程

```bash
git push origin main
```

### 常用命令

```bash
# 查看远程仓库
git remote -v

# 删除上游远程仓库
git remote remove upstream
```

---

## 实用小技巧

### 撤销操作

```bash
# 撤销未暂存的修改（恢复文件）
git checkout -- .

# 撤销已 add 但未 commit
git reset HEAD

# 撤销最近一次 commit（保留修改）
git reset --soft HEAD~1

# 撤销最近一次 commit（不保留修改）
git reset --hard HEAD~1
```

### 临时保存（Stash）

```bash
# 暂停当前工作，去做其他事
git stash

# 恢复之前的工作
git stash pop

# 查看 stash 列表
git stash list

# 删除 stash
git stash drop
```

### 查看信息

```bash
# 查看某次提交的内容
git show <commit-id>

# 查看某个文件的历史
git log -p <文件名>

# 图形化查看分支
git log --graph --oneline --all
```

---

## 提交信息规范

### 推荐格式

```
类型: 描述
```

### 常用类型

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 代码重构（不影响功能） |
| `test` | 测试相关 |
| `chore` | 构建/工具相关 |

### 示例

```
feat: 添加用户登录功能
fix: 修复了支付失败的 bug
docs: 更新了 README
refactor: 优化了代码结构
style: 格式化代码
```

---

## 注意事项

1. **永远不要在 main 分支上直接开发** ❌
2. **提交前先 `git status` 确认一下** ✅
3. **多用 `git log --oneline` 查看历史**
4. **定期同步上游，避免落后太多**
5. **多人协作时慎用 rebase**，会改写提交历史
6. **提交前检查是否有敏感信息**（密码、密钥等）

---

## 推荐工具

### 命令行工具

- **Git Bash** - Windows 自带
- **iTerm2 + Oh My Zsh** - Mac/Linux 推荐

### 可视化工具

- **GitHub Desktop** - 免费，简单易用
- **VS Code 内置 Git** - 方便集成开发
- **Sourcetree** - 功能强大，免费

---

## 常见问题

### Q: 合并冲突了怎么办？

```bash
# 1. 查看冲突文件
git status

# 2. 手动解决冲突（编辑文件）

# 3. 标记为已解决
git add <冲突文件>

# 4. 完成合并
git commit
```

### Q: 推送失败怎么办？

可能是远程有更新，先 pull 再推送：

```bash
git pull --rebase
git push
```

### Q: 误删了分支怎么办？

```bash
# 找到误删分支的最后一次提交
git reflog

# 恢复分支
git checkout -b <分支名> <commit-id>
```

---

> 文档最后更新：2026-02-22
