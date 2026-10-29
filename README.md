# Telegram AI Bot — Multi-Model Chat (Single File)

A single-file Telegram bot built on **python-telegram-bot** that lets users
chat with several AI models from one bot, in private chats and groups, and
switch models per user.

- Multi-model AI chat via the RanaGPT providers (TextAi, BlackBox, GeminiApi, ImageAi)
- Per-user model selection stored in memory
- Works in private chats and groups

## Run

```bash
pip install python-telegram-bot RanaGPT
BOT_TOKEN=your_token_from_BotFather python telegram_ai_bot.py
```

The token is read from the `BOT_TOKEN` environment variable — never hardcode it.

## License

MIT — see `LICENSE`.
