# PM Studio MCP

PM Studio MCP is a Model Context Protocol (MCP) server for product management tasks. It provides a suite of tools and utilities to help product managers analyze user feedback, perform competitive analysis, generate data visualizations, and access structured data sources.

## Getting Started
You may find keys in the loop file: https://microsoftapc.sharepoint.com/:fl:/r/contentstorage/x8FNO-xtskuCRX2_fMTHLbjHaHnyOSBPmaEXaBgV1fA/Document%20Library/Copilot/Key%20Vault.loop?d=waa77d19c735642939322fd824ee4c5b4&csf=1&web=1&e=rgZRBa&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRng4Rk5PLXh0c2t1Q1JYMl9mTVRITGJqSGFIbnlPU0JQbWFFWGFCZ1YxZkEmZD1iJTIxOHdIV29GdEJ0VXlXbHdxcDdEb21zOEljby1sQVAzRkhralBqdV9SeUFlNzFNQ2l5T0FtWVNMV0d3RHQwSlV4dyZmPTAxQ0dPRks0NDQyRjMyVVZUVFNOQkpHSVg1UUpIT0pSTlUmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4dGFXTnliM052Wm5SaGNHTXVjMmhoY21Wd2IybHVkQzVqYjIxOFlpRTRkMGhYYjBaMFFuUlZlVmRzZDNGd04wUnZiWE00U1dOdkxXeEJVRE5HU0d0cVVHcDFYMUo1UVdVM01VMURhWGxQUVcxWlUweFhSM2RFZERCS1ZYaDNmREF4UTBkUFJrczBXVVpVUlRWV05FOUJOa05hUmtwRlZEVTNSbEkyTlZVelQwbyUzRCUyMiUyQyUyMmklMjIlM0ElMjIzNTIzZTgwMS1lYjU1LTRmODUtOTJjMi0xMWM2Y2NkYTQzNzclMjIlN0Q%3D

   ```
   {
      "mcpServers": {
         "pm-studio-mcp": {
               "command": "uvx",
               "args": [
                  "pm-studio-mcp"
               ],
               "env": {
                  "WORKING_PATH": "{PATH_TO_YOUR_WORKSPACE}/working_dir/",
                  "AZURE_KEY_VAULT_URL": "{AZURE_KEY_VAULT_URL}",
                  "AZURE_KEY_VAULT_TENANT_ID":"{AZURE_KEY_VAULT_TENANT_ID}",
                  "AZURE_KEY_VAULT_CLIENT_ID":"{AZURE_KEY_VAULT_CLIENT_ID}",
                  "AZURE_KEY_VAULT_CLIENT_SECRET":"{AZURE_KEY_VAULT_CLIENT_SECRET}",
               },
               "disabled": false
         }
      }
   }
   ```
