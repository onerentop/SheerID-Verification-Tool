"""
SheerID Verification Telegram Bot
Multi-platform student/teacher/military verification via Telegram

Author: ThanhNguyxn
"""

import os
import sys
import logging
import asyncio
from typing import Dict, Optional
from pathlib import Path
from functools import wraps

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)
from telegram.constants import ParseMode

from verifier import (
    UnifiedVerifier,
    ToolType,
    ToolInfo,
    TOOLS,
    get_tool_by_name,
    get_all_tools,
)

# ============ CONFIG ============
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
PROXY = os.getenv("PROXY", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Conversation states
WAITING_URL = 1

# ============ LOGGING ============
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO)
)
logger = logging.getLogger(__name__)

# Reduce noise from httpx
logging.getLogger("httpx").setLevel(logging.WARNING)


# ============ USER SESSIONS ============
class UserSession:
    """Track user verification state"""

    def __init__(self):
        self.selected_tool: Optional[ToolType] = None
        self.pending_url: Optional[str] = None
        self.is_verifying: bool = False


user_sessions: Dict[int, UserSession] = {}


def get_session(user_id: int) -> UserSession:
    """Get or create user session"""
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()
    return user_sessions[user_id]


# ============ KEYBOARDS ============
def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu with all tools"""
    tools = get_all_tools()

    buttons = []
    row = []
    for i, (tool_type, info) in enumerate(tools.items()):
        row.append(InlineKeyboardButton(
            f"{info.emoji} {info.display_name}",
            callback_data=f"tool:{tool_type.value}"
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton("📊 统计", callback_data="stats")])

    return InlineKeyboardMarkup(buttons)


def get_tool_keyboard(tool_type: ToolType) -> InlineKeyboardMarkup:
    """Tool action keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 输入验证链接", callback_data=f"input_url:{tool_type.value}")],
        [InlineKeyboardButton("◀️ 返回主菜单", callback_data="main_menu")],
    ])


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Cancel keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ 取消", callback_data="cancel")],
    ])


# ============ HANDLERS ============
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user

    welcome_text = f"""
👋 *欢迎使用 SheerID 验证机器人！*

你好，{user.first_name}！

这个机器人可以帮助你自动完成多个平台的学生/教师/军人身份验证：

🎵 Spotify Premium 学生优惠
📺 YouTube Premium 学生优惠
🤖 Google One (Gemini) 学生优惠
⚡ Bolt.new Pro 教师优惠
👩‍🏫 ChatGPT Plus K-12 教师优惠
🎖️ ChatGPT Plus 军人优惠
🔍 Perplexity Pro 学生优惠
🎨 Canva Education 教师优惠

*请选择一个验证工具开始：*
"""

    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
📖 *使用帮助*

*命令列表：*
/start - 启动机器人，显示主菜单
/verify \\<工具\\> \\<URL\\> - 直接验证
/stats - 查看统计数据
/help - 显示此帮助

*快捷验证命令：*
/spotify \\<URL\\> - Spotify 学生验证
/youtube \\<URL\\> - YouTube 学生验证
/one \\<URL\\> - Google One 学生验证
/boltnew \\<URL\\> - Bolt.new 教师验证
/k12 \\<URL\\> - ChatGPT K-12 教师验证
/veterans \\<URL\\> - ChatGPT 军人验证
/perplexity \\<URL\\> - Perplexity 学生验证
/canva \\<URL\\> - Canva 教师验证

*使用示例：*
```
/one https://services.sheerid.com/verify/...?verificationId=xxx
```

*注意事项：*
• 验证链接必须包含 `sheerid.com` 和 `verificationId`
• 验证提交后需等待 24-48 小时人工审核
• 建议使用住宅代理以提高成功率
"""

    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /stats command"""
    # Collect stats from all tools
    stats_text = "📊 *验证统计*\n\n"

    base_path = Path(__file__).parent.parent

    total_success = 0
    total_failed = 0

    for tool_type, info in TOOLS.items():
        stats_file = base_path / info.dir_name / "stats.json"
        if stats_file.exists():
            try:
                import json
                data = json.loads(stats_file.read_text())
                success = data.get("success", 0)
                failed = data.get("failed", 0)
                total = success + failed
                total_success += success
                total_failed += failed

                if total > 0:
                    rate = (success / total) * 100
                    stats_text += f"{info.emoji} *{info.display_name}*\n"
                    stats_text += f"   ✅ {success} | ❌ {failed} | 📈 {rate:.1f}%\n\n"
            except Exception:
                pass

    if total_success + total_failed > 0:
        overall_rate = (total_success / (total_success + total_failed)) * 100
        stats_text += f"━━━━━━━━━━━━━━━━━\n"
        stats_text += f"*总计:* ✅ {total_success} | ❌ {total_failed} | 📈 {overall_rate:.1f}%"
    else:
        stats_text += "_暂无统计数据_"

    if update.callback_query:
        await update.callback_query.edit_message_text(
            stats_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("◀️ 返回主菜单", callback_data="main_menu")]
            ])
        )
    else:
        await update.message.reply_text(
            stats_text,
            parse_mode=ParseMode.MARKDOWN
        )

    return ConversationHandler.END


async def tool_shortcut_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle tool shortcut commands like /spotify, /youtube, etc."""
    command = update.message.text.split()[0][1:]  # Remove leading /
    tool_type = get_tool_by_name(command)

    if not tool_type:
        await update.message.reply_text("❌ 未知的工具")
        return

    tool_info = TOOLS[tool_type]

    # Check if URL is provided
    args = context.args
    if args:
        url = args[0]
        await run_verification(update, context, tool_type, url)
    else:
        # Ask for URL
        session = get_session(update.effective_user.id)
        session.selected_tool = tool_type

        await update.message.reply_text(
            f"{tool_info.emoji} *{tool_info.display_name}*\n\n"
            f"请发送 SheerID 验证链接：",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_cancel_keyboard()
        )


async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /verify command"""
    args = context.args

    if len(args) < 2:
        await update.message.reply_text(
            "❌ *用法错误*\n\n"
            "正确格式: `/verify <工具> <URL>`\n\n"
            "示例: `/verify one https://services.sheerid.com/...`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    tool_name = args[0]
    url = args[1]

    tool_type = get_tool_by_name(tool_name)
    if not tool_type:
        await update.message.reply_text(
            f"❌ 未知的工具: `{tool_name}`\n\n"
            f"可用工具: spotify, youtube, one, boltnew, k12, veterans, perplexity, canva",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await run_verification(update, context, tool_type, url)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[int]:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = update.effective_user.id
    session = get_session(user_id)

    if data == "main_menu":
        await query.edit_message_text(
            "🏠 *主菜单*\n\n请选择验证工具：",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu_keyboard()
        )
        session.selected_tool = None
        return ConversationHandler.END

    elif data == "cancel":
        session.selected_tool = None
        session.pending_url = None
        await query.edit_message_text(
            "❌ 已取消\n\n请选择验证工具：",
            reply_markup=get_main_menu_keyboard()
        )
        return ConversationHandler.END

    elif data == "stats":
        await stats_command(update, context)
        return ConversationHandler.END

    elif data.startswith("tool:"):
        tool_name = data.split(":")[1]
        tool_type = get_tool_by_name(tool_name)

        if tool_type:
            tool_info = TOOLS[tool_type]
            session.selected_tool = tool_type

            await query.edit_message_text(
                f"{tool_info.emoji} *{tool_info.display_name}*\n\n"
                f"_{tool_info.description}_\n\n"
                f"请选择操作：",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_tool_keyboard(tool_type)
            )
        return None

    elif data.startswith("input_url:"):
        tool_name = data.split(":")[1]
        tool_type = get_tool_by_name(tool_name)

        if tool_type:
            tool_info = TOOLS[tool_type]
            session.selected_tool = tool_type

            await query.edit_message_text(
                f"{tool_info.emoji} *{tool_info.display_name}*\n\n"
                f"请发送 SheerID 验证链接：\n\n"
                f"_链接格式: https://services.sheerid.com/verify/...?verificationId=xxx_",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_cancel_keyboard()
            )
            return WAITING_URL

    return None


async def handle_url_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle URL message from user"""
    user_id = update.effective_user.id
    session = get_session(user_id)

    if not session.selected_tool:
        await update.message.reply_text(
            "请先选择验证工具",
            reply_markup=get_main_menu_keyboard()
        )
        return ConversationHandler.END

    url = update.message.text.strip()
    await run_verification(update, context, session.selected_tool, url)

    session.selected_tool = None
    return ConversationHandler.END


async def run_verification(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    tool_type: ToolType,
    url: str
) -> None:
    """Execute verification"""
    user_id = update.effective_user.id
    session = get_session(user_id)
    tool_info = TOOLS[tool_type]

    # Check if already verifying
    if session.is_verifying:
        await update.message.reply_text(
            "⚠️ 你已经有一个验证正在进行中，请等待完成..."
        )
        return

    session.is_verifying = True

    # Send initial status
    if update.callback_query:
        status_message = await update.callback_query.edit_message_text(
            f"{tool_info.emoji} *{tool_info.display_name}*\n\n"
            f"🔄 正在初始化验证...",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        status_message = await update.message.reply_text(
            f"{tool_info.emoji} *{tool_info.display_name}*\n\n"
            f"🔄 正在初始化验证...",
            parse_mode=ParseMode.MARKDOWN
        )

    try:
        # Create verifier
        verifier = UnifiedVerifier(proxy=PROXY if PROXY else None)

        # Progress callback
        async def progress_callback(message: str):
            try:
                await status_message.edit_text(
                    f"{tool_info.emoji} *{tool_info.display_name}*\n\n{message}",
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception:
                pass

        # Run verification
        result = await verifier.verify(tool_type, url, progress_callback)

        # Send result
        result_text = result.to_telegram_message(tool_info)

        await status_message.edit_text(
            result_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 再次验证", callback_data=f"input_url:{tool_type.value}")],
                [InlineKeyboardButton("◀️ 返回主菜单", callback_data="main_menu")],
            ])
        )

    except Exception as e:
        logger.exception("Verification error")
        await status_message.edit_text(
            f"{tool_info.emoji} *{tool_info.display_name}*\n\n"
            f"❌ *验证出错*\n\n"
            f"错误信息: `{str(e)}`",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("◀️ 返回主菜单", callback_data="main_menu")]
            ])
        )

    finally:
        session.is_verifying = False


async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown messages"""
    session = get_session(update.effective_user.id)

    if session.selected_tool:
        # User is expected to send URL
        await handle_url_message(update, context)
    else:
        await update.message.reply_text(
            "❓ 不明白你的意思\n\n"
            "请使用 /start 查看主菜单，或使用 /help 获取帮助",
            reply_markup=get_main_menu_keyboard()
        )


async def setup_commands(application: Application) -> None:
    """Setup bot commands for menu"""
    commands = [
        BotCommand("start", "启动机器人"),
        BotCommand("help", "获取帮助"),
        BotCommand("stats", "查看统计"),
        BotCommand("verify", "验证 - /verify <工具> <URL>"),
        BotCommand("spotify", "Spotify 学生验证"),
        BotCommand("youtube", "YouTube 学生验证"),
        BotCommand("one", "Google One 学生验证"),
        BotCommand("boltnew", "Bolt.new 教师验证"),
        BotCommand("k12", "ChatGPT K12 教师验证"),
        BotCommand("veterans", "ChatGPT 军人验证"),
        BotCommand("perplexity", "Perplexity 学生验证"),
        BotCommand("canva", "Canva 教师验证"),
    ]
    await application.bot.set_my_commands(commands)


def main() -> None:
    """Main entry point"""
    if not BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set")
        print("   Set it via: export TELEGRAM_BOT_TOKEN='your-bot-token'")
        sys.exit(1)

    print()
    print("╔" + "═" * 50 + "╗")
    print("║" + " SheerID Verification Telegram Bot".center(50) + "║")
    print("║" + " github.com/ThanhNguyxn".center(50) + "║")
    print("╚" + "═" * 50 + "╝")
    print()

    if PROXY:
        print(f"🔒 Using proxy: {PROXY[:30]}...")
    else:
        print("⚠️  No proxy configured (set PROXY env var)")

    print("🚀 Starting bot...")

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Setup commands
    application.post_init = setup_commands

    # Conversation handler for URL input
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_callback)
        ],
        states={
            WAITING_URL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url_message),
                CallbackQueryHandler(button_callback),
            ],
        },
        fallbacks=[
            CommandHandler("start", start_command),
            CallbackQueryHandler(button_callback),
        ],
        per_message=False,
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("verify", verify_command))

    # Tool shortcut commands
    for tool_type in ToolType:
        application.add_handler(
            CommandHandler(tool_type.value, tool_shortcut_command)
        )

    # Conversation handler
    application.add_handler(conv_handler)

    # Unknown message handler
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown)
    )

    # Run bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
