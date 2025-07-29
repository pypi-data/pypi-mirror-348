# Notion Webhook Server

This is a simple python package to create a webhook server that can be used to handle Notion webhooks and trigger actions.

## Installation

```bash
pip install secnex-notion-webhook-server
```

## Usage

```python
from notion_webhook import WebhookServer, ServerHandler, NotionWebhookHandler

server = WebhookServer()
server.run(ServerHandler())

handler = NotionWebhookHandler(lambda data: print(data))
server.webhook(handler)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Contact

For questions or support, please contact us at [support@secnex.io](mailto:support@secnex.io).
