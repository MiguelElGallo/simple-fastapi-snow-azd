using './main.bicep'

param name = readEnvironmentVariable('AZURE_ENV_NAME') // The environment name, for example dev
param location = readEnvironmentVariable('AZURE_LOCATION') // Azure region to deploy resources to
param skuplanname = 'Y1' // The name of the App Service plan
