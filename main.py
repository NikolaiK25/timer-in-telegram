import ptbot
from decouple import config
import pytimeparse


def wait(chat_id, text, bot):
    delay_seconds = pytimeparse.parse(text)


    if delay_seconds is None:
        bot.send_message(chat_id,  "Не могу понять время. Укажите задержку, например: 5s, 30 секунд")

    else:
        message_id = bot.send_message(chat_id, f"Таймер запущен на {delay_seconds} секунд\n{render_progressbar(delay_seconds, 0)}")
        
        bot.create_countdown(delay_seconds, countdown,
                            chat_id=chat_id,
                            message_id=message_id,
                            total=delay_seconds, bot=bot)
        

        bot.create_timer(delay_seconds, send_message, author_id=chat_id, bot=bot)


def countdown(seconds_left, chat_id, message_id, total, bot):
    progress = total - seconds_left
    bot.update_message(chat_id, message_id, 
                        f"Осталось {seconds_left} секунд\n{render_progressbar(total, progress)}")


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def send_message(author_id, bot):
    bot.send_message(author_id, "Время вышло")


def main():
    tg_token = config('tg_token')
    tg_chat_id = config('tg_chat_id')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(wait, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()