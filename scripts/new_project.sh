#!/bin/bash
set -e

OWNER=$1
PROJECT=$2

if [ -z "$OWNER" ] || [ -z "$PROJECT" ]; then
    echo "用法: $0 <owner> <project-name>"
    echo "示例: $0 zhangsan kuaishou-live"
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$REPO_ROOT/projects/$OWNER/$PROJECT"

if [ -d "$TARGET" ]; then
    echo "错误: $TARGET 已存在"
    exit 1
fi

mkdir -p "$REPO_ROOT/projects/$OWNER"
cp -r "$REPO_ROOT/projects/_template" "$TARGET"

if [[ "$OSTYPE" == "darwin"* ]]; then
    find "$TARGET" -type f -exec sed -i '' "s/{{OWNER}}/$OWNER/g" {} +
    find "$TARGET" -type f -exec sed -i '' "s/{{PROJECT}}/$PROJECT/g" {} +
else
    find "$TARGET" -type f -exec sed -i "s/{{OWNER}}/$OWNER/g" {} +
    find "$TARGET" -type f -exec sed -i "s/{{PROJECT}}/$PROJECT/g" {} +
fi

if [ -f "$TARGET/config.yaml.example" ]; then
    mv "$TARGET/config.yaml.example" "$TARGET/config.yaml"
fi

echo "项目已创建: $TARGET"
echo ""
echo "下一步:"
echo "  1. 编辑 $TARGET/config.yaml"
echo "  2. 编辑 $TARGET/README.md"
echo "  3. 编写 $TARGET/scraper.py"
