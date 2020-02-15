import requests

from managing import Emojis

def random_dog_url():
    contents = requests.get('https://random.dog/woof.json').json()
    return contents.get('url')


def send_dog(update, context):
    url = random_dog_url()
    if not url:
        return
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=url,
        disable_notification=True,
        caption=f'Here is the random dog picture for you, enjoy! {Emojis.DOG.value}',
    )

# https://financialmodelingprep.com/api/v3/cryptocurrency/BTC
