# Azure Authentication Setup Guide

This guide helps you set up Azure authentication for the HR Interview Outcome Viewer application.

## Prerequisites

- Python 3.8 or higher
- Azure subscription with access to the Cosmos DB account

## Authentication Methods

### Method 1: Azure CLI (Recommended for Development)

1. Install Azure CLI:
   ```bash
   # Windows (using Chocolatey)
   choco install azure-cli
   
   # Or download from: https://aka.ms/installazurecliwindows
   ```

2. Login to Azure:
   ```bash
   az login
   ```

3. Set the correct subscription (if you have multiple):
   ```bash
   az account set --subscription "your-subscription-id"
   ```

### Method 2: Managed Identity (For Azure VMs/App Services)

If running on Azure infrastructure, Managed Identity is automatically configured. No additional setup required.

### Method 3: Service Principal (For Production)

1. Create a service principal:
   ```bash
   az ad sp create-for-rbac --name "interview-viewer-app" --role contributor
   ```

2. Set environment variables:
   ```bash
   # Windows PowerShell
   $env:AZURE_CLIENT_ID="your-client-id"
   $env:AZURE_CLIENT_SECRET="your-client-secret"
   $env:AZURE_TENANT_ID="your-tenant-id"
   
   # Windows Command Prompt
   set AZURE_CLIENT_ID=your-client-id
   set AZURE_CLIENT_SECRET=your-client-secret
   set AZURE_TENANT_ID=your-tenant-id
   ```

## Required Azure Permissions

Ensure your account/service principal has the following permissions on the Cosmos DB account:

- **Cosmos DB Account Reader Role** (minimum)
- **DocumentDB Account Contributor** (recommended)

To assign permissions:

```bash
# Get your Cosmos DB account resource ID
COSMOS_RESOURCE_ID="/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.DocumentDB/databaseAccounts/common-nosql-db"

# Assign role (replace with your user/service principal object ID)
az role assignment create \
  --assignee "your-user-or-sp-object-id" \
  --role "DocumentDB Account Contributor" \
  --scope $COSMOS_RESOURCE_ID
```

## Troubleshooting

### Common Issues

1. **"DefaultAzureCredential failed to retrieve a token"**
   - Ensure you're logged in with `az login`
   - Check your Azure subscription access
   - Verify Cosmos DB permissions

2. **"Failed to initialize Cosmos DB client"**
   - Check network connectivity
   - Verify the Cosmos DB endpoint URL
   - Ensure the database and container exist

3. **Permission Denied Errors**
   - Verify your account has access to the Cosmos DB
   - Check if the database/container names are correct
   - Ensure you have at least Reader role on the Cosmos DB account

### Testing Connection

You can test your Azure connection by running:

```bash
az cosmosdb show --name common-nosql-db --resource-group your-resource-group
```

## Security Best Practices

1. **Never commit credentials to version control**
2. **Use Managed Identity when possible**
3. **Rotate Service Principal secrets regularly**
4. **Apply principle of least privilege for permissions**
5. **Use Azure Key Vault for storing secrets in production**