# Orca Security MCP Server

This integration connects Orca Security's AI Sonar and data serving capabilities to MCP (Model Control Protocol), allowing you to ask natural language questions about your cloud infrastructure security posture directly in Cursor, Claude or other AI tools.

## Configure Claude Desktop

1. Install `uv` if you don't have it already:

   ```bash
   pip install uv
   ```

2. Open Claude Desktop, Go to Settings->Developers->Edit Config
3. Change the configuration file to the following (replacing `<TOKEN>` with your actual Orca token):

   ```json
   {
     "mcpServers": {
       "orca": {
         "command": "uvx",
         "args": ["orca-mcp-server"],
         "env": {
           "ORCA_AUTH_TOKEN": "<TOKEN>"
         }
       }
     }
   }
   ```

4. Restart Claude Desktop for the changes to take effect

## Environment Variables

| Variable               | Description                        | Default                       |
| ---------------------- | ---------------------------------- | ----------------------------- |
| `ORCA_API_HOST`        | Orca Security API host             | <https://api.orcasecurity.io> |
| `ORCA_AUTH_TOKEN`      | Your Orca API authentication token | TOKEN (Required)              |
| `ORCA_REQUEST_TIMEOUT` | API request timeout in seconds     | 30.0                          |

## Using the Integration

Once running, you can query the Orca Security data using natural language:

Example queries:

- "Show me all critical vulnerabilities in my AWS environment"
- "What EC2 instances are missing security patches?"
- "Which S3 buckets are publicly accessible?"

## Troubleshooting

If you encounter issues:

1. Check the log output for error messages
2. Verify your Orca authentication token is valid
3. Ensure your network allows connections to the Orca API endpoint
