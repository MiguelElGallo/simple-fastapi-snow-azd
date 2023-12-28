param location string
param resourceToken string
param tags object
param skuplanname string = 'Y1'

 

resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'function-${resourceToken}'
  location: location
  tags: union(tags, { 'azd-service-name': 'api' })
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      ftpsState: 'Disabled'
      appCommandLine: ''
    }
    httpsOnly: true
  }
  identity: {
    type: 'SystemAssigned'
  }

  resource appSettings 'config' = {
    name: 'appsettings'
    properties: {
      SCM_DO_BUILD_DURING_DEPLOYMENT: 'true'
      ENABLE_ORYX_BUILD: 'true'
    }
  }

  resource logs 'config' = {
    name: 'logs'
    properties: {
      applicationLogs: {
        fileSystem: {
          level: 'Verbose'
        }
      }
      detailedErrorMessages: {
        enabled: true
      }
      failedRequestsTracing: {
        enabled: true
      }
      httpLogs: {
        fileSystem: {
          enabled: true
          retentionInDays: 1
          retentionInMb: 35
        }
      }
    }
  }
}
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'app-${resourceToken}'
  location: location
  sku: {
    name: skuplanname
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}


output WEB_URI string = 'https://${functionApp.properties.defaultHostName}/docs'
