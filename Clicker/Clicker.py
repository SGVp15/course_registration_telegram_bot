import asyncio
from datetime import datetime

from Config.config import LOG_FILE, OLD_USERS
from queue_zoom import get_users_from_queue_file, del_user_from_temp_file, get_old_users
from Clicker.selenium_zoom import registration_user_zoom_link


async def run_clicker():
    print('webdriver run')
    while True:
        try:
            user = get_users_from_queue_file()[0]
        except IndexError:
            await asyncio.sleep(5)
            continue

        old_users = get_old_users()
        if user:
            if user in old_users:
                print(f'[ INFO ] [ Есть в логе ] {user}')
                del_user_from_temp_file()
            else:
                print(f'[ INFO ] {user}')
                if await registration_user_zoom_link(user):
                    with open(OLD_USERS, encoding='utf-8', mode='a') as file:
                        file.write(f'{user}\n')

                    write_user_to_log(f'{datetime.now()}\t{user}\n')
                    print(f'[ OK ] {user}')
                    del_user_from_temp_file()
                await asyncio.sleep(60 * 1)


def write_user_to_log(s):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(s)
