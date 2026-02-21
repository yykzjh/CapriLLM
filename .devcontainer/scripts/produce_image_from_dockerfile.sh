#!/usr/bin/env bash
set -euo pipefail

# 用法: ./produce_image_from_dockerfile.sh <Registry地址> <仓库名> <tag> <dockerfile_name>
# 示例: ./produce_image_from_dockerfile.sh crpi-xxx.cn-hangzhou.personal.cr.aliyuncs.com yykzjh1/caprillm_dev latest Dockerfile_dev

REGISTRY="${1:?用法: $0 <Registry地址> <仓库名> <tag> <dockerfile_name>}"
REPO="${2:?用法: $0 <Registry地址> <仓库名> <tag> <dockerfile_name>}"
TAG="${3:?用法: $0 <Registry地址> <仓库名> <tag> <dockerfile_name>}"
DOCKERFILE_NAME="${4:?用法: $0 <Registry地址> <仓库名> <tag> <dockerfile_name>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCKER_DIR="$PROJECT_ROOT/.devcontainer/docker"

IMAGE="${REGISTRY}/${REPO}:${TAG}"
DOCKERFILE="$DOCKER_DIR/$DOCKERFILE_NAME"

# 1. 检测登录状态，未登录则提示输入并登录
if ! grep -q "$REGISTRY" ~/.docker/config.json 2>/dev/null; then
    echo "未检测到已登录 $REGISTRY，请输入凭据："
    read -rp "用户名: " username
    read -rsp "密码: " password
    echo
    docker login -u "$username" -p "$password" "$REGISTRY"
fi

# 2. 构建镜像
echo "正在构建镜像: $IMAGE"
docker build -f "$DOCKERFILE" -t "$IMAGE" "$DOCKER_DIR"

# 3. 推送镜像
echo "正在推送镜像: $IMAGE"
docker push "$IMAGE"

echo "完成: $IMAGE"
