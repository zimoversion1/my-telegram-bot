import asyncio
from telethon import TelegramClient, events

# --- သင့်ရဲ့ အချက်အလက်များ ---
api_id = 32506978
api_hash = '9c6ee3d7ed39a95d21ecf64ac29fa875'

# Source Groups (မူရင်းဂရု ၃ ခု)
source_groups = [-1002475027155, -1003562918575, -1002151004457]
# Target Group (ပို့မည့်ဂရု ID အမှန် - မျက်တောင်ဖွင့်ပိတ် မပါရပါ)
target_group = 'https://t.me/+raPEpk9bIpIyMWE1'

client = TelegramClient('my_session', api_id, api_hash)
is_running = True # False အစား True ပြောင်းလိုက်ပါ

print(f"Source Group {len(source_groups)} ခုကို စောင့်ကြည့်ဖို့ ပြင်ဆင်နေပါတယ်...")

@client.on(events.NewMessage(chats=source_groups))
async def forward_handler(event):
    if is_running:
        try:
            # တိုက်ရိုက် Forward လုပ်ခြင်း
            await client.forward_messages(target_group, event.message)
            chat = await event.get_chat()
            print(f"Forwarded: {chat.title} မှ Message {event.message.id}")
        except Exception as e:
            print(f"Forward Error: {e}")

@client.on(events.NewMessage(pattern='/forward_(.+)'))
async def control_handler(event):
    global is_running
    cmd = event.pattern_match.group(1).lower()
    if cmd == 'start':
        is_running = True
        await event.respond('🚀 Forwarder စတင်နေပါပြီ...')
    elif cmd == 'stop':
        is_running = False
        await event.respond('🛑 Forwarder ကို ရပ်နားလိုက်ပါပြီ။')

async def main():
    await client.start()
    # Target Group ကို အရင်ဆုံး ချိတ်ဆက်ထားရန်
    await client.get_input_entity(target_group)
    print("Bot အလုပ်လုပ်နေပါပြီ။ /forward_start ပို့ပြီး စတင်နိုင်ပါတယ်။")
    await client.run_until_disconnected()

if __name__ == '__main__':

    asyncio.run(main())
