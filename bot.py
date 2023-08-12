import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import start_polling

from tgbot.config import load_config
from tgbot.filters import AdminFilter
from tgbot.handlers import register_admin, register_user, register_errors
from tgbot.misc.notifications import startup_notify

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    data = {
        'config': config,
    }
    dp.setup_middleware(EnvironmentMiddleware(data))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_errors(dp)


async def on_startup(dp: Dispatcher):
    register_all_middlewares(dp, dp.bot['config'])
    register_all_filters(dp)
    register_all_handlers(dp)

    await startup_notify(dp.bot['config'].tg_bot.admin_ids)


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    # start
    try:
        start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    finally:
        logging.warning("Bot closed")


if __name__ == '__main__':
    main()
