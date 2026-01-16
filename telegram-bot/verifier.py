"""
Unified Verifier Interface for Telegram Bot
Wraps all verification tools into a single interface

Author: ThanhNguyxn (Telegram Bot Extension)
"""

import sys
import asyncio
import importlib.util
from pathlib import Path
from typing import Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class ToolType(Enum):
    """Verification tool types"""
    SPOTIFY = "spotify"
    YOUTUBE = "youtube"
    ONE = "one"
    BOLTNEW = "boltnew"
    K12 = "k12"
    VETERANS = "veterans"
    PERPLEXITY = "perplexity"
    CANVA = "canva"


@dataclass
class ToolInfo:
    """Tool metadata"""
    name: str
    display_name: str
    emoji: str
    description: str
    dir_name: str
    verifier_class: str


# Tool configurations
TOOLS: Dict[ToolType, ToolInfo] = {
    ToolType.SPOTIFY: ToolInfo(
        name="spotify",
        display_name="Spotify Premium",
        emoji="🎵",
        description="Spotify Premium Student Verification",
        dir_name="spotify-verify-tool",
        verifier_class="SpotifyVerifier"
    ),
    ToolType.YOUTUBE: ToolInfo(
        name="youtube",
        display_name="YouTube Premium",
        emoji="📺",
        description="YouTube Premium Student Verification",
        dir_name="youtube-verify-tool",
        verifier_class="YouTubeVerifier"
    ),
    ToolType.ONE: ToolInfo(
        name="one",
        display_name="Google One (Gemini)",
        emoji="🤖",
        description="Google One AI Premium Student Verification",
        dir_name="one-verify-tool",
        verifier_class="GeminiVerifier"
    ),
    ToolType.BOLTNEW: ToolInfo(
        name="boltnew",
        display_name="Bolt.new Pro",
        emoji="⚡",
        description="Bolt.new Teacher Verification",
        dir_name="boltnew-verify-tool",
        verifier_class="BoltVerifier"
    ),
    ToolType.K12: ToolInfo(
        name="k12",
        display_name="ChatGPT Plus (K12)",
        emoji="👩‍🏫",
        description="ChatGPT Plus K-12 Teacher Verification",
        dir_name="k12-verify-tool",
        verifier_class="K12Verifier"
    ),
    ToolType.VETERANS: ToolInfo(
        name="veterans",
        display_name="ChatGPT Plus (Military)",
        emoji="🎖️",
        description="ChatGPT Plus Military Verification",
        dir_name="veterans-verify-tool",
        verifier_class="VeteransVerifier"
    ),
    ToolType.PERPLEXITY: ToolInfo(
        name="perplexity",
        display_name="Perplexity Pro",
        emoji="🔍",
        description="Perplexity Pro Student Verification",
        dir_name="perplexity-verify-tool",
        verifier_class="PerplexityVerifier"
    ),
    ToolType.CANVA: ToolInfo(
        name="canva",
        display_name="Canva Education",
        emoji="🎨",
        description="Canva Education Teacher Verification",
        dir_name="canva-teacher-tool",
        verifier_class="CanvaVerifier"
    ),
}


class VerificationResult:
    """Unified verification result"""

    def __init__(self, success: bool, message: str, details: Dict = None):
        self.success = success
        self.message = message
        self.details = details or {}

    def to_telegram_message(self, tool_info: ToolInfo) -> str:
        """Format result for Telegram"""
        if self.success:
            lines = [
                f"{tool_info.emoji} *{tool_info.display_name}*",
                "",
                "✅ *验证提交成功！*",
                "",
            ]
            if self.details.get("student"):
                lines.append(f"👤 姓名: `{self.details['student']}`")
            if self.details.get("email"):
                lines.append(f"📧 邮箱: `{self.details['email']}`")
            if self.details.get("school"):
                lines.append(f"🏫 学校: `{self.details['school']}`")
            lines.extend([
                "",
                "⏳ 请等待 24-48 小时进行人工审核",
            ])
        else:
            lines = [
                f"{tool_info.emoji} *{tool_info.display_name}*",
                "",
                f"❌ *验证失败*",
                "",
                f"原因: {self.message}",
            ]

        return "\n".join(lines)


class UnifiedVerifier:
    """Unified interface for all verification tools"""

    def __init__(self, proxy: str = None):
        self.proxy = proxy
        self.base_path = Path(__file__).parent.parent
        self._verifier_cache = {}

    def _load_verifier_class(self, tool_type: ToolType):
        """Dynamically load verifier class from tool module"""
        if tool_type in self._verifier_cache:
            return self._verifier_cache[tool_type]

        tool_info = TOOLS[tool_type]
        tool_path = self.base_path / tool_info.dir_name / "main.py"

        if not tool_path.exists():
            raise FileNotFoundError(f"Tool not found: {tool_path}")

        # Add parent to path for anti_detect import
        if str(self.base_path) not in sys.path:
            sys.path.insert(0, str(self.base_path))

        # Load module dynamically
        spec = importlib.util.spec_from_file_location(
            f"{tool_info.name}_verifier",
            tool_path
        )
        module = importlib.util.module_from_spec(spec)

        # Suppress print during import
        original_print = print
        try:
            import builtins
            builtins.print = lambda *args, **kwargs: None
            spec.loader.exec_module(module)
        finally:
            builtins.print = original_print

        # Get verifier class
        verifier_class = getattr(module, tool_info.verifier_class, None)
        if not verifier_class:
            # Try common class names
            for name in ["Verifier", f"{tool_info.name.title()}Verifier"]:
                verifier_class = getattr(module, name, None)
                if verifier_class:
                    break

        if not verifier_class:
            raise AttributeError(f"Verifier class not found in {tool_path}")

        self._verifier_cache[tool_type] = verifier_class
        return verifier_class

    def validate_url(self, url: str) -> bool:
        """Validate SheerID URL format"""
        return "sheerid.com" in url.lower() and "verificationId=" in url

    async def verify(
        self,
        tool_type: ToolType,
        url: str,
        progress_callback: Callable[[str], None] = None
    ) -> VerificationResult:
        """Run verification asynchronously"""

        tool_info = TOOLS[tool_type]

        if not self.validate_url(url):
            return VerificationResult(
                success=False,
                message="无效的 URL，必须包含 sheerid.com 和 verificationId"
            )

        try:
            if progress_callback:
                await progress_callback(f"🔄 正在加载 {tool_info.display_name} 验证器...")

            # Load verifier class
            verifier_class = self._load_verifier_class(tool_type)

            if progress_callback:
                await progress_callback("🔄 正在初始化验证...")

            # Create verifier instance
            verifier = verifier_class(url, proxy=self.proxy)

            # Check link validity
            if hasattr(verifier, "check_link"):
                check = verifier.check_link()
                if not check.get("valid"):
                    return VerificationResult(
                        success=False,
                        message=check.get("error", "链接无效")
                    )

            if progress_callback:
                await progress_callback("🔄 正在提交验证信息...")

            # Run verification in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, verifier.verify)

            return VerificationResult(
                success=result.get("success", False),
                message=result.get("error", result.get("message", "")),
                details=result
            )

        except FileNotFoundError as e:
            return VerificationResult(
                success=False,
                message=f"工具未找到: {str(e)}"
            )
        except Exception as e:
            return VerificationResult(
                success=False,
                message=f"验证出错: {str(e)}"
            )
        finally:
            # Cleanup
            if 'verifier' in locals() and hasattr(verifier, 'client'):
                try:
                    verifier.client.close()
                except:
                    pass


def get_tool_by_name(name: str) -> Optional[ToolType]:
    """Get tool type by name (case-insensitive)"""
    name_lower = name.lower().strip()

    # Aliases
    aliases = {
        "gemini": ToolType.ONE,
        "google": ToolType.ONE,
        "googleone": ToolType.ONE,
        "military": ToolType.VETERANS,
        "chatgpt": ToolType.K12,
        "bolt": ToolType.BOLTNEW,
    }

    if name_lower in aliases:
        return aliases[name_lower]

    for tool_type in ToolType:
        if tool_type.value == name_lower:
            return tool_type

    return None


def get_all_tools() -> Dict[ToolType, ToolInfo]:
    """Get all available tools"""
    return TOOLS.copy()
