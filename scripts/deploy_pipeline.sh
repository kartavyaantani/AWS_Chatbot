#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <stack-name> <artifact-bucket> <region>"
  exit 1
fi

STACK_NAME="$1"
ARTIFACT_BUCKET="$2"
REGION="$3"

aws cloudformation deploy \
  --template-file infra/cloudformation/chatbot-stack.yaml \
  --stack-name "$STACK_NAME" \
  --parameter-overrides ArtifactBucketName="$ARTIFACT_BUCKET" \
  --capabilities CAPABILITY_NAMED_IAM \
  --region "$REGION"
