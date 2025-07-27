#!/usr/bin/env python3
"""
Telegram OSINT Bot - OSINT BY DIWAS
A comprehensive OSINT bot with 30+ features for intelligence gathering
Compatible with telebotcreator.com and nxcreate.com
"""

import os
import time
import json
import requests
import asyncio
import hashlib
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

# Telegram bot imports
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# Additional imports for OSINT features
import whois
import dns.resolver
from PIL import Image
from PIL.ExifTags import TAGS
import re
import urllib.parse

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "8399190156:AAHS-R8lCYRHyZRkWnb2rB6ipRfbFvfoxVw"
CHANNEL_USERNAME = "@team_falcone"
CHANNEL_ID = -1001234567890  # Replace with actual channel ID

class OSINTBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup all command and message handlers"""
        # Basic handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("menu", self.main_menu))
        
        # OSINT feature handlers
        self.application.add_handler(CommandHandler("username_lookup", self.username_lookup))
        self.application.add_handler(CommandHandler("email_lookup", self.email_lookup))
        self.application.add_handler(CommandHandler("phone_lookup", self.phone_lookup))
        self.application.add_handler(CommandHandler("ip_lookup", self.ip_lookup))
        self.application.add_handler(CommandHandler("domain_whois", self.domain_whois))
        self.application.add_handler(CommandHandler("dns_lookup", self.dns_lookup))
        self.application.add_handler(CommandHandler("reverse_image_search", self.reverse_image_search))
        self.application.add_handler(CommandHandler("exif_data", self.exif_data))
        self.application.add_handler(CommandHandler("website_archive", self.website_archive))
        self.application.add_handler(CommandHandler("subdomain_finder", self.subdomain_finder))
        self.application.add_handler(CommandHandler("port_scan", self.port_scan))
        self.application.add_handler(CommandHandler("pastebin_search", self.pastebin_search))
        self.application.add_handler(CommandHandler("github_search", self.github_search))
        self.application.add_handler(CommandHandler("google_dork", self.google_dork))
        self.application.add_handler(CommandHandler("shodan_lookup", self.shodan_lookup))
        self.application.add_handler(CommandHandler("translate", self.translate_text))
        self.application.add_handler(CommandHandler("url_expander", self.url_expander))
        self.application.add_handler(CommandHandler("hash_lookup", self.hash_lookup))
        self.application.add_handler(CommandHandler("telegram_channel_info", self.telegram_channel_info))
        self.application.add_handler(CommandHandler("breach_check", self.breach_check))
        self.application.add_handler(CommandHandler("osint_news", self.osint_news))
        self.application.add_handler(CommandHandler("educational_resources", self.educational_resources))
        
        # Additional advanced features
        self.application.add_handler(CommandHandler("social_media_scan", self.social_media_scan))
        self.application.add_handler(CommandHandler("document_metadata", self.document_metadata))
        self.application.add_handler(CommandHandler("video_metadata", self.video_metadata))
        self.application.add_handler(CommandHandler("image_geolocation", self.image_geolocation))
        self.application.add_handler(CommandHandler("censys_lookup", self.censys_lookup))
        self.application.add_handler(CommandHandler("report_generate", self.report_generate))
        self.application.add_handler(CommandHandler("proxy_settings", self.proxy_settings))
        self.application.add_handler(CommandHandler("whois_history", self.whois_history))
        self.application.add_handler(CommandHandler("telegram_user_info", self.telegram_user_info))
        self.application.add_handler(CommandHandler("breach_check_domain", self.breach_check_domain))
        
        # Callback query handler for inline keyboards
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handler for images and documents
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))

    async def typewriter_effect(self, update: Update, text: str, delay: float = 0.1):
        """Create typewriter animation effect"""
        message = await update.message.reply_text("_")
        
        for i in range(1, len(text) + 1):
            await message.edit_text(text[:i] + "_")
            await asyncio.sleep(delay)
        
        await message.edit_text(text)
        return message

    async def check_channel_membership(self, user_id: int) -> bool:
        """Check if user is a member of the required channel"""
        try:
            # This would require the actual channel ID
            # For demo purposes, we'll return True
            # In production, use: await self.application.bot.get_chat_member(CHANNEL_ID, user_id)
            return True
        except Exception:
            return False

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with typewriter effect and channel verification"""
        user = update.effective_user
        
        # Typewriter effect for "OSINT BY DIWAS"
        await self.typewriter_effect(update, "\U0001F50D OSINT BY DIWAS \U0001F50D")
        
        # Check channel membership
        is_member = await self.check_channel_membership(user.id)
        
        if not is_member:
            keyboard = [[InlineKeyboardButton("\U0001F4E2 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "\U0001F680 Welcome to OSINT BY DIWAS!\n\n"
                "To access all features, please join our channel first:",
                reply_markup=reply_markup
            )
            
            # Add verification button
            verify_keyboard = [[InlineKeyboardButton("✅ I Joined - Verify", callback_data="verify_membership")]]
            verify_markup = InlineKeyboardMarkup(verify_keyboard)
            
            await update.message.reply_text(
                "After joining, click the button below to verify:",
                reply_markup=verify_markup
            )
        else:
            await self.show_main_menu(update)

    async def show_main_menu(self, update: Update):
        """Display the modern main menu"""
        keyboard = [
            [InlineKeyboardButton("\U0001F464 User OSINT", callback_data="user_osint"),
             InlineKeyboardButton("\U0001F310 Web OSINT", callback_data="web_osint")],
            [InlineKeyboardButton("\U0001F4F1 Social Media", callback_data="social_osint"),
             InlineKeyboardButton("\U0001F5BC️ Image OSINT", callback_data="image_osint")],
            [InlineKeyboardButton("\U0001F50D Advanced Tools", callback_data="advanced_osint"),
             InlineKeyboardButton("\U0001F6E0️ Utilities", callback_data="utilities")],
            [InlineKeyboardButton("\U0001F4DA Education", callback_data="education"),
             InlineKeyboardButton("\U0001F4CA Generate Report", callback_data="generate_report")],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        menu_text = """\U0001F3AF **OSINT BY DIWAS - Main Menu**

Welcome to your comprehensive OSINT toolkit! 
Choose a category below to explore 30+ powerful features:

\U0001F539 **User OSINT** - Username, Email, Phone lookups
\U0001F539 **Web OSINT** - Domain, IP, Archive searches  
\U0001F539 **Social Media** - Profile analysis & monitoring
\U0001F539 **Image OSINT** - Reverse search & metadata
\U0001F539 **Advanced Tools** - Specialized investigations
\U0001F539 **Utilities** - Translation, proxies & more

\U0001F4A1 *Tip: Use /help for command list*
        """
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                menu_text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                menu_text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "verify_membership":
            user_id = query.from_user.id
            is_member = await self.check_channel_membership(user_id)
            
            if is_member:
                await query.edit_message_text("✅ Membership verified! Welcome to OSINT BY DIWAS!")
                await self.show_main_menu(update)
            else:
                await query.edit_message_text(
                    "❌ Please join the channel first, then click verify again.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("\U0001F4E2 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"),
                        InlineKeyboardButton("\U0001F504 Verify Again", callback_data="verify_membership")
                    ]])
                )
        
        elif query.data == "user_osint":
            await self.show_user_osint_menu(update)
        elif query.data == "web_osint":
            await self.show_web_osint_menu(update)
        elif query.data == "social_osint":
            await self.show_social_osint_menu(update)
        elif query.data == "image_osint":
            await self.show_image_osint_menu(update)
        elif query.data == "advanced_osint":
            await self.show_advanced_osint_menu(update)
        elif query.data == "utilities":
            await self.show_utilities_menu(update)
        elif query.data == "education":
            await self.show_education_menu(update)
        elif query.data == "generate_report":
            await self.report_generate(update, context)
        elif query.data == "help_menu":
            await self.help_command(update, context)
        elif query.data == "main_menu":
            await self.show_main_menu(update)

    async def show_user_osint_menu(self, update: Update):
        """Show User OSINT submenu"""
        keyboard = [
            [InlineKeyboardButton("\U0001F50D Username Lookup", callback_data="cmd_username_lookup")],
            [InlineKeyboardButton("\U0001F4E7 Email Lookup", callback_data="cmd_email_lookup")],
            [InlineKeyboardButton("\U0001F4F1 Phone Lookup", callback_data="cmd_phone_lookup")],
            [InlineKeyboardButton("\U0001F30D IP Lookup", callback_data="cmd_ip_lookup")],
            [InlineKeyboardButton("\U0001F3E2 Domain WHOIS", callback_data="cmd_domain_whois")],
            [InlineKeyboardButton("\U0001F519 Back to Main Menu", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = """\U0001F464 **User OSINT Commands**

• `/username_lookup <username>` - Search username across platforms
• `/email_lookup <email>` - Check email in breach databases  
• `/phone_lookup <phone>` - Get phone number information
• `/ip_lookup <ip>` - Geolocate IP address
• `/domain_whois <domain>` - Get domain registration info

\U0001F4A1 *Click buttons below or type commands directly*
        """
        
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def show_web_osint_menu(self, update: Update):
        """Show Web OSINT submenu"""
        keyboard = [
            [InlineKeyboardButton("\U0001F50D DNS Lookup", callback_data="cmd_dns_lookup")],
            [InlineKeyboardButton("\U0001F3DB️ Website Archive", callback_data="cmd_website_archive")],
            [InlineKeyboardButton("\U0001F310 Subdomain Finder", callback_data="cmd_subdomain_finder")],
            [InlineKeyboardButton("\U0001F513 Port Scan", callback_data="cmd_port_scan")],
            [InlineKeyboardButton("\U0001F4CB Pastebin Search", callback_data="cmd_pastebin_search")],
            [InlineKeyboardButton("\U0001F519 Back to Main Menu", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = """\U0001F310 **Web OSINT Commands**

• `/dns_lookup <domain>` - Get DNS records
• `/website_archive <url>` - Find archived versions
• `/subdomain_finder <domain>` - Discover subdomains  
• `/port_scan <ip>` - Check open ports (passive)
• `/pastebin_search <keyword>` - Search paste sites

\U0001F4A1 *Click buttons below or type commands directly*
        """
        
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def show_social_osint_menu(self, update: Update):
        """Show Social Media OSINT submenu"""
        keyboard = [
            [InlineKeyboardButton("\U0001F465 Social Media Scan", callback_data="cmd_social_media_scan")],
            [InlineKeyboardButton("\U0001F4BB GitHub Search", callback_data="cmd_github_search")],
            [InlineKeyboardButton("\U0001F4FA Telegram Channel Info", callback_data="cmd_telegram_channel_info")],
            [InlineKeyboardButton("\U0001F464 Telegram User Info", callback_data="cmd_telegram_user_info")],
            [InlineKeyboardButton("\U0001F519 Back to Main Menu", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = """\U0001F4F1 **Social Media OSINT Commands**

• `/social_media_scan <name>` - Find social profiles
• `/github_search <keyword>` - Search GitHub repositories
• `/telegram_channel_info <channel>` - Get channel details
• `/telegram_user_info <user_id>` - Get user information

\U0001F4A1 *Click buttons below or type commands directly*
        """
        
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def show_image_osint_menu(self, update: Update):
        """Show Image OSINT submenu"""
        keyboard = [
            [InlineKeyboardButton("\U0001F50D Reverse Image Search", callback_data="cmd_reverse_image_search")],
            [InlineKeyboardButton("\U0001F4CA EXIF Data", callback_data="cmd_exif_data")],
            [InlineKeyboardButton("\U0001F5FA️ Image Geolocation", callback_data="cmd_image_geolocation")],
            [InlineKeyboardButton("\U0001F4C4 Document Metadata", callback_data="cmd_document_metadata")],
            [InlineKeyboardButton("\U0001F519 Back to Main Menu", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = """\U0001F5BC️ **Image OSINT Commands**

• `/reverse_image_search` - Upload image for reverse search
• `/exif_data` - Upload image to extract metadata
• `/image_geolocation` - Upload image to find location
• `/document_metadata` - Upload document for analysis

\U0001F4A1 *Upload images/documents or use commands*
        """
        
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def show_advanced_osint_menu(self, update: Update):
        """Show Advanced OSINT submenu"""
        keyboard = [
            [InlineKeyboardButton("\U0001F50D Google Dork", callback_data="cmd_google_dork")],
            [InlineKeyboardButton("\U0001F6E1️ Shodan Lookup", callback_data="cmd_shodan_lookup")],
            [InlineKeyboardButton("\U0001F510 Hash Lookup", callback_data="cmd_hash_lookup")],
            [InlineKeyboardButton("\U0001F4A5 Breach Check", callback_data="cmd_breach_check")],
            [InlineKeyboardButton("\U0001F310 Censys Lookup", callback_data="cmd_censys_lookup")],
            [InlineKeyboardButton("\U0001F519 Back to Main Menu", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = """\U0001F50D **Advanced OSINT Commands**

• `/google_dork <query>` - Advanced Google searches
• `/shodan_lookup <ip>` - Shodan device information
• `/hash_lookup <hash>` - Check file hashes
• `/breach_check <email>` - Comprehensive breach check
• `/censys_lookup <ip>` - Censys scan data

\U0001F4A1 *Advanced features for experienced users*
        """
        
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def show_utilities_menu(self, update: Update):
        """Show Utilities submenu"""
        keyboard = [
            [InlineKeyboardButton("\U0001F310 Translate", callback_data="cmd_translate")],
            [InlineKeyboardButton("\U0001F517 URL Expander", callback_data="cmd_url_expander")],
            [InlineKeyboardButton("\U0001F512 Proxy Settings", callback_data="cmd_proxy_settings")],
            [InlineKeyboardButton("\U0001F4CA Video Metadata", callback_data="cmd_video_metadata")],
            [InlineKeyboardButton("\U0001F519 Back to Main Menu", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = """\U0001F6E0️ **Utility Commands**

• `/translate <text> <lang>` - Translate text
• `/url_expander <url>` - Expand shortened URLs
• `/proxy_settings` - Configure proxy settings
• `/video_metadata <url>` - Extract video metadata

\U0001F4A1 *Helpful tools for OSINT investigations*
        """
        
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def show_education_menu(self, update: Update):
        """Show Education submenu"""
        keyboard = [
            [InlineKeyboardButton("\U0001F4DA Educational Resources", callback_data="cmd_educational_resources")],
            [InlineKeyboardButton("\U0001F4F0 OSINT News", callback_data="cmd_osint_news")],
            [InlineKeyboardButton("\U0001F519 Back to Main Menu", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = """\U0001F4DA **Educational Resources**

\U0001F393 **Free Courses**:
  • OSINT Curious Webinars
  • Bellingcat Online Investigation Toolkit
  • Intel Techniques Online Course (Free sections)
  • Trace Labs OSINT Search Party

\U0001F4D6 **Books**:
  • "Open Source Intelligence Techniques" by Michael Bazzell
  • "OSINT Handbook" by i-intelligence
  • "Social Media Intelligence" by various authors

\U0001F527 **Practice Platforms**:
  • Trace Labs CTF
  • OSINT Exercise websites
  • Gralhix challenges
  • OSINT Dojo

\U0001F310 **Websites**:
  • OSINT Framework: https://osintframework.com/
  • OSINT Techniques: https://osinttechniques.com/
  • Awesome OSINT: https://github.com/jivoi/awesome-osint

\U0001F4A1 *Start with basics and gradually advance to specialized techniques*
        """
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    # OSINT Feature Implementations
    async def username_lookup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Lookup username across multiple platforms"""
        if not context.args:
            await update.message.reply_text("Usage: /username_lookup <username>")
            return
        
        username = context.args[0]
        await update.message.reply_text(f"\U0001F50D Searching for username: {username}")
        
        # Simulate username search across platforms
        platforms = {
            "Instagram": f"https://instagram.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://reddit.com/u/{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "LinkedIn": f"https://linkedin.com/in/{username}",
            "Facebook": f"https://facebook.com/{username}"
        }
        
        result_text = f"\U0001F3AF **Username Search Results for: {username}**\n\n"
        
        for platform, url in platforms.items():
            # In a real implementation, you would check if the profile exists
            result_text += f"\U0001F517 **{platform}**: {url}\n"
        
        result_text += "\n\U0001F4A1 *Click links to verify profile existence*"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def email_lookup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check email in breach databases"""
        if not context.args:
            await update.message.reply_text("Usage: /email_lookup <email>")
            return
        
        email = context.args[0]
        
        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            await update.message.reply_text("❌ Invalid email format")
            return
        
        await update.message.reply_text(f"\U0001F50D Checking breaches for: {email}")
        
        # Simulate breach check (in real implementation, use HaveIBeenPwned API)
        result_text = f"\U0001F6E1️ **Breach Check Results for: {email}**\n\n"
        result_text += "\U0001F50D Checking against known data breaches...\n\n"
        result_text += "✅ **Status**: No breaches found in public databases\n"
        result_text += "\U0001F512 **Recommendation**: Continue monitoring regularly\n\n"
        result_text += "\U0001F4A1 *This is a simulated result. Use HaveIBeenPwned API for real checks*"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def phone_lookup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Lookup phone number information"""
        if not context.args:
            await update.message.reply_text("Usage: /phone_lookup <phone_number>")
            return
        
        phone = context.args[0]
        await update.message.reply_text(f"\U0001F4F1 Analyzing phone number: {phone}")
        
        # Simulate phone lookup
        result_text = f"\U0001F4DE **Phone Number Analysis: {phone}**\n\n"
        result_text += "\U0001F30D **Country**: Unknown\n"
        result_text += "\U0001F4E1 **Carrier**: Unknown\n"
        result_text += "\U0001F4CD **Region**: Unknown\n"
        result_text += "\U0001F522 **Type**: Unknown\n\n"
        result_text += "\U0001F4A1 *This is a simulated result. Use numverify API for real lookups*"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def ip_lookup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Lookup IP address information"""
        if not context.args:
            await update.message.reply_text("Usage: /ip_lookup <ip_address>")
            return
        
        ip = context.args[0]
        await update.message.reply_text(f"\U0001F310 Analyzing IP address: {ip}")
        
        try:
            # Use a free IP geolocation service
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            
            if data['status'] == 'success':
                result_text = f"\U0001F30D **IP Address Analysis: {ip}**\n\n"
                result_text += f"\U0001F3D9️ **City**: {data.get('city', 'Unknown')}\n"
                result_text += f"\U0001F30D **Country**: {data.get('country', 'Unknown')}\n"
                result_text += f"\U0001F4CD **Region**: {data.get('regionName', 'Unknown')}\n"
                result_text += f"\U0001F3E2 **ISP**: {data.get('isp', 'Unknown')}\n"
                result_text += f"\U0001F3DB️ **Organization**: {data.get('org', 'Unknown')}\n"
                result_text += f"\U0001F550 **Timezone**: {data.get('timezone', 'Unknown')}\n"
                result_text += f"\U0001F4CD **Coordinates**: {data.get('lat', 'Unknown')}, {data.get('lon', 'Unknown')}\n"
            else:
                result_text = f"❌ Could not analyze IP address: {ip}"
                
        except Exception as e:
            result_text = f"❌ Error analyzing IP address: {str(e)}"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def domain_whois(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get domain WHOIS information"""
        if not context.args:
            await update.message.reply_text("Usage: /domain_whois <domain>")
            return
        
        domain = context.args[0]
        await update.message.reply_text(f"\U0001F50D Getting WHOIS info for: {domain}")
        
        try:
            w = whois.whois(domain)
            
            result_text = f"\U0001F3E2 **WHOIS Information for: {domain}**\n\n"
            result_text += f"\U0001F4C5 **Creation Date**: {w.creation_date}\n"
            result_text += f"\U0001F4C5 **Expiration Date**: {w.expiration_date}\n"
            result_text += f"\U0001F3E2 **Registrar**: {w.registrar}\n"
            result_text += f"\U0001F4E7 **Registrant Email**: {w.emails}\n"
            result_text += f"\U0001F310 **Name Servers**: {w.name_servers}\n"
            
        except Exception as e:
            result_text = f"❌ Error getting WHOIS info: {str(e)}"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def dns_lookup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Perform DNS lookup"""
        if not context.args:
            await update.message.reply_text("Usage: /dns_lookup <domain>")
            return
        
        domain = context.args[0]
        await update.message.reply_text(f"\U0001F50D DNS lookup for: {domain}")
        
        result_text = f"\U0001F310 **DNS Records for: {domain}**\n\n"
        
        try:
            # A Records
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                result_text += "\U0001F4CD **A Records**:\n"
                for record in a_records:
                    result_text += f"  • {record}\n"
                result_text += "\n"
            except:
                result_text += "\U0001F4CD **A Records**: None found\n\n"
            
            # MX Records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                result_text += "\U0001F4E7 **MX Records**:\n"
                for record in mx_records:
                    result_text += f"  • {record}\n"
                result_text += "\n"
            except:
                result_text += "\U0001F4E7 **MX Records**: None found\n\n"
            
            # NS Records
            try:
                ns_records = dns.resolver.resolve(domain, 'NS')
                result_text += "\U0001F310 **NS Records**:\n"
                for record in ns_records:
                    result_text += f"  • {record}\n"
                result_text += "\n"
            except:
                result_text += "\U0001F310 **NS Records**: None found\n\n"
                
        except Exception as e:
            result_text += f"❌ Error performing DNS lookup: {str(e)}"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def reverse_image_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Reverse image search instructions"""
        text = """\U0001F5BC️ **Reverse Image Search**

To perform a reverse image search:
1. Upload an image to this chat
2. I'll provide reverse search links for:
   • Google Images
   • TinEye
   • Yandex Images

\U0001F4E4 **Upload an image now to get started!**
        """
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle uploaded photos for reverse search and EXIF analysis"""
        photo = update.message.photo[-1]  # Get highest resolution
        file = await context.bot.get_file(photo.file_id)
        
        # Download the image
        file_path = f"/tmp/{photo.file_id}.jpg"
        await file.download_to_drive(file_path)
        
        # Provide reverse search options
        keyboard = [
            [InlineKeyboardButton("\U0001F50D Reverse Search Links", callback_data="reverse_search_links")],
            [InlineKeyboardButton("\U0001F4CA Extract EXIF Data", callback_data="extract_exif")],
            [InlineKeyboardButton("\U0001F5FA️ Find Geolocation", callback_data="find_geolocation")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "\U0001F4F8 **Image received!** Choose an analysis option:",
            reply_markup=reply_markup
        )
        
        # Store file path for later use
        context.user_data['last_image'] = file_path

    async def exif_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Extract EXIF data from uploaded image"""
        if 'last_image' not in context.user_data:
            await update.message.reply_text("\U0001F4F8 Please upload an image first!")
            return
        
        file_path = context.user_data['last_image']
        
        try:
            image = Image.open(file_path)
            exifdata = image.getexif()
            
            if exifdata is not None:
                result_text = "\U0001F4CA **EXIF Data Analysis**\n\n"
                
                for tag_id in exifdata:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exifdata.get(tag_id)
                    
                    if isinstance(data, bytes):
                        data = data.decode()
                    
                    result_text += f"**{tag}**: {data}\n"
                
                if len(result_text) > 4000:
                    result_text = result_text[:4000] + "...\\n\\n*Truncated due to length*"
            else:
                result_text = "\U0001F4CA **EXIF Data Analysis**\n\nNo EXIF data found in this image."
                
        except Exception as e:
            result_text = f"❌ Error extracting EXIF data: {str(e)}"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def website_archive(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get archived versions of a website"""
        if not context.args:
            await update.message.reply_text("Usage: /website_archive <url>")
            return
        
        url = context.args[0]
        
        # Create Wayback Machine link
        wayback_url = f"https://web.archive.org/web/*/{url}"
        
        result_text = f"\U0001F3DB️ **Website Archive Search**\n\n"
        result_text += f"\U0001F517 **Original URL**: {url}\n"
        result_text += f"\U0001F4DA **Wayback Machine**: {wayback_url}\n\n"
        result_text += "\U0001F4A1 *Click the Wayback Machine link to view archived versions*"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def subdomain_finder(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Find subdomains for a domain"""
        if not context.args:
            await update.message.reply_text("Usage: /subdomain_finder <domain>")
            return
        
        domain = context.args[0]
        await update.message.reply_text(f"\U0001F50D Searching subdomains for: {domain}")
        
        # Simulate subdomain discovery
        common_subdomains = ['www', 'mail', 'ftp', 'admin', 'blog', 'shop', 'api', 'dev', 'test', 'staging']
        found_subdomains = []
        
        for sub in common_subdomains:
            subdomain = f"{sub}.{domain}"
            # In real implementation, you would actually test these
            found_subdomains.append(subdomain)
        
        result_text = f"\U0001F310 **Subdomain Discovery for: {domain}**\n\n"
        result_text += "\U0001F50D **Common Subdomains Found**:\n"
        
        for subdomain in found_subdomains[:10]:  # Limit to first 10
            result_text += f"  • {subdomain}\n"
        
        result_text += "\n\U0001F4A1 *This is a simulated result. Use tools like sublist3r for real discovery*"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def port_scan(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Passive port scanning information"""
        if not context.args:
            await update.message.reply_text("Usage: /port_scan <ip_address>")
            return
        
        ip = context.args[0]
        
        result_text = f"\U0001F513 **Port Scan Information for: {ip}**\n\n"
        result_text += "⚠️ **Note**: This bot performs passive scanning only.\n\n"
        result_text += "\U0001F50D **Recommended Tools**:\n"
        result_text += "  • Shodan.io - Internet-wide scan data\n"
        result_text += "  • Censys.io - Device discovery\n"
        result_text += "  • Nmap - Local network scanning\n\n"
        result_text += f"\U0001F310 **Shodan Search**: https://shodan.io/host/{ip}\n"
        result_text += f"\U0001F50D **Censys Search**: https://search.censys.io/hosts/{ip}\n\n"
        result_text += "\U0001F4A1 *Use /shodan_lookup or /censys_lookup for API-based results*"
        
        await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)

    async def pastebin_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Search Pastebin for keywords"""
        if not context.args:
            await update.message.reply_text("Usage: /pastebin_search <keyword>")
            return
        
        keyword = ' '.join(context.args)
        
        result
