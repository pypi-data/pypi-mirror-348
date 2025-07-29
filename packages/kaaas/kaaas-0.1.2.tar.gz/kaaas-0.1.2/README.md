KAAS - Kubernetes AI-powered Cluster Analysis and Solution
KAAS is a tool that leverages AI to analyze Kubernetes clusters, identify issues, and provide solutions using tools like k8sgpt and LLMs (e.g., Ollama, Bedrock).
Installation

Install KAAS via pip:pip install kaas



Configuration
Edit config.yaml or kaas/config.py to set your backend LLM and AWS settings:

backend_llm: The LLM backend for k8sgpt (e.g., ollama, bedrock).
aws_region: AWS region for SNS and CloudWatch.
sns_topic_arn: SNS Topic ARN for notifications.
log_group and log_stream: CloudWatch Log Group and Stream names.
pricing_url: URL for multi-cluster pricing information.

To find the installed config.yaml:
python -c "import kaas; print(kaas.__path__[0])"

Then edit config.yaml in that directory, or create a config.yaml in your working directory to override the defaults.
Usage
Run KAAS to analyze your Kubernetes cluster:
kaas

Prerequisites

k8sgpt and kubectl must be installed and available in your PATH.
AWS credentials must be configured for SNS and CloudWatch access.


All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying, modification, distribution, or use is strictly prohibited without the author's explicit written permission.

© 2025 Kashif Rafi. All rights reserved.

