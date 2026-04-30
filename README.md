# Cocktails Shared Infrastructure

This directory contains the Terraform infrastructure code for managing shared Azure resources used by the Cocktails application.

## 🏗️ Infrastructure Components

### Core Resources
- **Resource Groups**: Dedicated resource groups for different environments
- **Key Vault**: Secure storage for secrets and certificates
- **Storage Account**: Blob storage for static content
- **Container Registry**: Shared Azure Container Registry for Docker images

### Networking
- **Virtual Network**: Network infrastructure for containerized applications
- **Subnets**: Dedicated subnets for different service tiers
- **Front Door CDN**: Content delivery network with custom domain support

### Security
- **Azure B2C**: User authentication and management
- **Key Vault Secrets**: Secure storage for application secrets
- **Network Security**: Subnet-level security rules

## 🛠️ Technology Stack

- **Infrastructure as Code**: Terraform
- **Cloud Provider**: Microsoft Azure
- **Container Registry**: Azure Container Registry (ACR)
- **CDN**: Azure Front Door
- **Storage**: Azure Blob Storage
- **Security**: Azure Key Vault, Azure B2C

## 🚀 Deployment

### Prerequisites
- Azure CLI
- Terraform CLI
- GitHub access
- Appropriate Azure permissions


## 📄 License

This project is proprietary software. All rights reserved. 
