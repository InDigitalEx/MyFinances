from abc import ABC
from dataclasses import dataclass

from .buttons import Buttons


@dataclass(frozen=True)
class Messages(ABC):
    UNKNOWN_MESSAGE = 'Я вас не понял, напишите /start'

    BOT_START = 'Бот запущен и работает исправно, извините за предоставленные неудобства!'

    BOT_STOP =  'В данный момент ведутся технические работы. Функционал бота может быть недоступен'

    START = 'Привет, {name}!\n\n' \
            'Я финансовый бот для Telegram.\n' \
            'Я помогу Вам контролировать свои финансы, управлять бюджетом, отслеживать расходы\n\n' \
            'Ваша текущая группа: <b>{group}</b>'

    CHANGE_GROUPS = f"<b>{Buttons.START['groups']}</b>\n\n" \
                    "Ваша текущая группа: <b>{group_name}</b>"

    HELP = f"<b>{Buttons.START['help']}</b>\n\n" \
           "Главное меню: /start\n\n" \
           "Добавление нового расхода в текущую группу: напишите сообщение: сумма категория\n" \
           "(Пример: 500 такси)\n\n" \
           "Добавление в бюджет нового дохода: напишите сообщение: Добавить сумма категория\n" \
           "(Пример: Добавить 50000 зарплата)\n\n" \
           "Остальная информация будет позже"

    SETTINGS = f'<b>{Buttons.START["settings"]}</b>\n\n' \
               'Настроим вам всё, не переживайте! (в разработке)'

    AUTHOR = 'Автор, разработчик и по совместительству созидатель бота: <b>@InDigitalE8</b>\n\n' \
             '<i>Напишите, если что-то не работает, возможно починим...</i>'

    ALREADY_IN_GROUP = 'Вы уже в этой группе'

    #region Expense

    EXPENSE_CREATE_TO_USERS = 'Группа: <b>{group_name}</b>\n\n' \
                              'Пользователь <b>{name}</b> добавил расход:\n' \
                              '<b>Стоимость:</b> {amount}\n' \
                              '<b>Описание:</b> {text}'

    EXPENSE_CREATE_TO_CREATOR = 'Вы добавили расход в группу <b>{group_name}</b>\n\n' \
                                '<b>Стоимость:</b> {amount} руб.\n' \
                                '<b>Описание:</b> {text}'

    EXPENSE_DELETE_TO_USERS = '<b>{name}</b> удалил расход <i>{text} ({amount} руб.)</i> в группе <b>{group_name}</b>'

    EXPENSE_DELETE_TO_CREATOR = 'Вы удалили расход <b>{text} ({amount} руб.)</b> в группе <b>{group_name}</b>'

    #endregion

    #region Income

    INCOME_CREATE_TO_USERS = 'Группа: <b>{group_name}</b>\n\n' \
                              'Пополнение от пользователя <b>{name}</b>:\n' \
                              '<b>Сумма:</b> {amount} руб.\n' \
                              '<b>Описание:</b> {text}'

    INCOME_CREATE_TO_CREATOR = 'Вы пополнили бюджет группы <b>{group_name}</b>\n\n' \
                                '<b>Сумма:</b> {amount} руб.\n' \
                                '<b>Описание:</b> {text}'

    INCOME_DELETE_TO_USERS = '<b>{name}</b> отменил пополнение бюджета на ' \
                             '<b>{amount} руб. ({text})</b> в группе {group_name}'

    INCOME_DELETE_TO_CREATOR = 'Вы удалили доход <b>{amount} руб. ({text})</b> в группе {group_name}'

    #endregion

    # region Create group

    CREATE_GROUP = '<b>Нужна новая группа? Не вопрос...</b>\n\nВведите название для новой группы!'

    CANCEL_CREATE_GROUP = 'Создание группы отменено ❌'

    CREATE_GROUP_NAME_INVALID = 'Не тыкайте по кнопкам, просто напишите название группы...'

    CREATE_GROUP_PRIVATE_INVALID = 'Такой ответ меня не устраивает, попробуйте ещё раз!'

    CREATE_GROUP_PRIVATE = '<b>Отлично, почти всё готово, ' \
                           'только остался один небольшой вопрос...</b>\n\n' \
                           'Группа будет приватная или публичная?'

    CREATE_GROUP_DONE = 'Группа <b>{group_name}</b> успешно создана!\n\n' \
                        f'Для смены группы используйте кнопку\n' \
                        f'"<b>{Buttons.START["groups"]}</b>"'

    #endregion

    # region Invite user

    INVITE = f'<b>{Buttons.START["invite"]}</b>\n' \
                  'Группа: <b>{group_name}</b>\n\n' \
                  'Выберите тип приглашения:'

    CANCEL_INVITE = '❌ Приглашение в группу отменено'

    INVITE_TYPE_INVALID = 'Сначала выберите тип приглашения:'

    INVITE_LINK = 'Ваша ссылка на приглашение в группу <b>{group_name}</b>:\n{link}'

    INVITE_LINK_USER_IS_INVITER = 'Это ваша группа, зачем Вам вступать в неё?'

    INVITE_LINK_USER_IN_GROUP = 'Вы уже состоите в этой группе'

    INVITE_LINK_JOIN = 'Приглашение от пользователя <b>{name}</b> ' \
                       'в группу <b>{group_name}</b> принято!\n\n' \
                       'Вы можете посмотреть основные команды написав команду <i>/help</i>'

    INVITE_LINK_JOIN_TO_USERS = 'Группа <b>{group_name}</b>:\n\n' \
                                'Пользователь <b>{name}</b> присоединился ' \
                                'к группе через пригласительную ссылку'

    INVITE_PERSONAL = 'Для приглашения в группу отправьте ссылку на пользователя\n' \
                      '(в формате «@ссылка»), либо его контакт'

    INVITE_PERSONAL_CONTACT_INVALID = 'Отправьте контакт пользователя'

    INVITE_PERSONAL_SENDER_CONTACT = '❌ Вы не можете пригласить самого себя!'

    INVITE_PERSONAL_CONTACT_NOT_EXISTS = '❌ К сожалению этот пользователь не пользуется нашим ботом 😢.\n' \
                                         'Вы можете пригласить его используя ссылку'

    INVITE_PERSONAL_CONTACT_IN_GROUP = '❌ Пользователь уже находится в этой группе'

    INVITE_PERSONAL_SEND = 'Приглашение в группу <b>{group_name}</b>\n' \
                           'от пользователя <b>{inviter}</b>\n\n' \
                           'Для взаимодействия нажмите на кнопки ниже'

    INVITE_PERSONAL_SEND_TO_INVITER = 'Приглашение пользователю <b>{name}</b> ' \
                                      'в группу <b>{group_name}</b> успешно отправлено'

    INVITE_PERSONAL_SEND_TO_USERS = 'Группа <b>{group_name}</b>:\n\n' \
                                    '<b>{inviter}</b> отправил(а) приглашение пользователю <b>{name}</b>'

    INVITE_PERSONAL_ACCEPT = 'Вы успешно вступили в группу <b>{group_name}</b>'

    INVITE_PERSONAL_ACCEPT_TO_USERS = 'Группа <b>{group_name}</b>:\n\n' \
                                      '<b>{name}</b> вступил в группу через приглашение'

    INVITE_PERSONAL_DECLINE = 'Вы отклонили заявку на вступление в группу'

    INVITE_PERSONAL_DECLINE_TO_INVITER = '<b>{name}</b> отклонил ваше приглашение на ' \
                                         'вступление в группу <b>{group_name}</b>'

    #endregion

    # region Statistics

    STATISTICS = '📌 Группа: <b>{group_name}</b>\n' \
                 '📊 Ваша статистика:\n\n' \
                 '{type}\n{items}'

    STATISTICS_MISSING = 'За этот промежуток времени отсутствуют записи'

    EXPENSES = '✏ Расходы ✏\n'

    INCOMES = '📈 Доходы 📈\n'

    STATISTICS_ITEM = '{amount} руб.: {text}\n'

    #endregion
