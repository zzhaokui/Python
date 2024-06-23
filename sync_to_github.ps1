# sync_to_github.ps1

# 设置 Git 用户信息
git config --global user.email "zzhaokui@gmail.com"
git config --global user.name "zzhaokui"

# 导航到项目目录
$projectDir = "D:\PycharmProjects"
Set-Location -Path $projectDir

# 初始化 Git 仓库（如果尚未初始化）
if (-not (Test-Path ".git")) {
    git init
}

# 添加所有文件到 Git
git add .

# 提交更改
$currentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Auto-sync on $currentDate"

# 设置远程仓库（如果尚未设置）
$remoteUrl = "https://github.com/zzhaokui/Python"
$remoteName = "origin"
if (-not (git remote | Select-String -Pattern $remoteName)) {
    git remote add $remoteName $remoteUrl
}

# 推送到 GitHub
git push -u $remoteName master
