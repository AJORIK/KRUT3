import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing Railway Variable: {name}. "
            f"Добавь её в Railway → Service → Variables и сделай Redeploy."
        )

    return value


BOT_TOKEN = get_required_env("BOT_TOKEN")
CHANNEL_URL = get_required_env("CHANNEL_URL")
SUPPORT_URL = get_required_env("SUPPORT_URL")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


START_TEXT = """Рады видеть вас в нашем боте!

Здесь вы можете начать спокойно и постепенно разбираться в финансовой информации — даже если раньше вы никогда не смотрели на графики.

Мы подготовили короткие и простые материалы, которые помогут новичкам понять базовую логику рынка: что такое движение цены, как цена реагирует на уровни и почему графики не являются полностью случайными. Такой подход развивает внимательность к деталям и помогает увереннее принимать решения.

Здесь нет сложной терминологии и профессионального жаргона — по крайней мере, в самом начале. Только понятные объяснения, которые постепенно помогают сформировать крепкую основу знаний.

Вы можете изучать материалы в удобном темпе, возвращаться к разделам в любое время и двигаться дальше по мере роста понимания."""


PRICE_ANALYSIS_TEXT = """Анализ цены — это навык наблюдения за тем, как меняется стоимость актива со временем, и понимания факторов, которые могут влиять на это движение. Это не про торговлю и не про быстрые решения «выше-ниже», а про изучение логики рынка и того, как цена реагирует на события, уровни и общую динамику.

Главная ценность анализа цены заключается в том, что поведение рынка становится более понятным через повторяющиеся закономерности. Вы начинаете замечать, что движения не являются полностью случайными: похожие структуры, зоны реакции, моменты ускорения и замедления часто повторяются на графиках.

Для новичков такой подход помогает убрать ощущение хаоса и увидеть структуру рынка как последовательность событий. Когда вы понимаете, как формируется график, становится проще принимать более осознанные решения в любой финансовой ситуации — как в жизни, так и в работе.

Именно поэтому изучение анализа цены является мягкой и безопасной отправной точкой для тех, кто хочет повысить финансовую грамотность и лучше ориентироваться в происходящем вокруг.

Пример:

Вы открываете график и замечаете, что цена несколько часов движется вверх, но постоянно останавливается примерно на одном и том же уровне, после чего немного откатывается назад. Даже без опыта можно почувствовать, что есть определённая «зона», на которую цена реагирует. Умение замечать такие повторяющиеся моменты — это как раз то, что развивает анализ."""


PRICE_BASICS_TEXT = """Основа анализа — это умение читать направление цены: куда рынок движется сейчас и что происходит внутри этого движения. Первое, чему учится новичок, — отличать восходящее движение, нисходящее движение и боковой диапазон. Это становится базовой точкой отсчёта.

Следующий шаг — понимание уровней. Уровни — это зоны, где цена раньше разворачивалась, останавливалась или замедлялась. Такие точки становятся ориентирами и помогают увидеть, где рынок может снова замедлиться или ускориться. Даже без сложных инструментов эти наблюдения дают более структурное понимание происходящего.

Сильные движения тоже имеют свою логику. Рынок редко меняет направление «из ниоткуда», и анализ помогает это замечать. Постепенно вы начинаете понимать, почему в одних областях графика цена ускоряется, а в других становится более спокойной или рискованной.

Этот навык развивается постепенно: чем больше вы наблюдаете, тем лучше начинаете чувствовать ритм рынка. Именно это делает обучение безопасным и интуитивно понятным.

Пример:

Если график движется вниз, но каждый раз при снижении цена останавливается около одного и того же уровня, это можно назвать уровнем поддержки. Когда новичок впервые замечает такое повторение, рынок становится для него понятнее. Это первый шаг к восприятию графика как системы."""


ANALYZE_CHART_TEXT = """Перед тем как делать какой-либо прогноз, важно внимательно оценить текущую картину.

Начните с определения общего направления: восходящий тренд, нисходящий тренд или боковое движение. Это задаёт контекст для дальнейшего анализа. Если направление понятно, анализ становится проще. Если рынок движется в боковом диапазоне, любые выводы лучше делать осторожнее.

Затем найдите уровни, где цена явно реагировала раньше. Эти зоны показывают, где участники рынка принимали решения. Такие уровни становятся важными ориентирами, за которыми стоит наблюдать дальше.

Обращайте внимание на резкие скачки цены. В моменты высокой волатильности рынок может вести себя непредсказуемо, поэтому выводы становятся менее надёжными. А спокойные участки графика, наоборот, позволяют анализировать ситуацию более вдумчиво.

Структурный подход помогает не бросаться в хаос, а разбирать ситуацию шаг за шагом. Это развивает дисциплину и превращает обучение в постепенное открытие новой логики — без спешки и лишнего риска.

Пример:

Представьте, что вы видите боковое движение: цена поднимается и опускается, но остаётся внутри одного диапазона. В такие моменты многие делают поспешные прогнозы. Но правильный анализ подсказывает: лучше дождаться, пока цена выйдет из диапазона и покажет более понятное направление."""


RISK_MANAGEMENT_TEXT = """Управление рисками — это ключевое правило, которое помогает сохранять спокойствие во время обучения.

Оно помогает избегать эмоциональных решений и не перегружать себя. Даже если вы пока изучаете только теорию, эти принципы полезны и в обычной жизни.

Первое — установите границы.
Заранее решите, сколько времени и внимания вы готовы уделять анализу. Это помогает избежать импульсивных действий и формирует дисциплину — один из главных навыков финансовой грамотности.

Второе — сохраняйте умеренность.
Не пытайтесь понять всё сразу. Новички часто слишком глубоко погружаются в графики и быстро устают. Управление рисками учит двигаться постепенно, без перегрузки.

Третье — принимайте ошибки спокойно.
Обучение всегда связано с неточностями и неверными предположениями. Риск-ориентированное мышление помогает воспринимать это спокойно и делать выводы из наблюдений, а не переживать из-за каждого промаха.

Пример:

Новичок может смотреть на график 2–3 часа подряд, устать и потерять концентрацию. Управление рисками подсказывает: ограничьте время анализа до 20–30 минут. Это снижает эмоциональную усталость и помогает сохранить ясность мышления."""


SIMPLE_LEARNING_METHOD_TEXT = """Один из самых эффективных методов для новичков — изучать уровни, где цена несколько раз меняла направление. Такие зоны можно назвать зонами реакции. Они показывают места, где участники рынка действовали наиболее активно.

Когда вы наблюдаете, как цена подходила к уровню раньше и что происходило после этого, вы начинаете замечать закономерности. График перестаёт выглядеть хаотично — он становится более структурным и понятным.

Метод уровней силён своей простотой. Он не требует сложных инструментов и хорошо подходит для тех, кто только начинает. Вы концентрируетесь на базовой механике поведения цены, а уже потом строите на этом более глубокие знания.

Такой подход развивает осторожность, внимательность и постепенность — три качества, которые особенно важны для финансовой грамотности и понимания рыночной логики.

Пример:

Вы замечаете, что цена три раза отскакивала от уровня 1.2500. Когда она подходит к этому уровню в четвёртый раз, вы уже понимаете: рынок часто реагирует в этой зоне. Это не призыв к действию, а подтверждение того, что уровни могут быть полезными ориентирами."""


CHECKLIST_TEXT = """Перед началом анализа полезно пройти короткий чек-лист. Он помогает сфокусироваться и уменьшить влияние эмоций. Чёткая структура даёт больше спокойствия и делает процесс более предсказуемым.

✅ Понятно ли общее направление?
Если да — вы анализируете ситуацию осознанно. Если нет — лучше подождать и посмотреть, как цена поведёт себя дальше.

✅ Видны ли уровни?
Уровни помогают увидеть возможные зоны реакции цены и упрощают анализ.

✅ Есть ли высокая волатильность?
Резкие движения могут скрывать реальную картину. Спокойные участки графика безопаснее для анализа.

✅ Следуете ли вы своим правилам?
Личный план — главный инструмент дисциплины.

📝 Записывайте свои наблюдения. Даже короткие заметки помогают отслеживать прогресс и замечать повторяющиеся закономерности.

Пример:

Вы открываете график и видите резкие свечи в обе стороны. По чек-листу это явный сигнал «нет»: направление непонятно, уровни размыты, волатильность слишком высокая. Значит, вы просто закрываете график и ждёте. Так вы сохраняете дисциплину — именно для этого и нужен чек-лист."""


CONTINUE_LEARNING_TEXT = """Чтобы глубже погрузиться в тему, вы можете изучать дополнительные примеры, разборы графиков и практические советы. Мы регулярно публикуем такие материалы в отдельном канале, чтобы вы могли двигаться вперёд в удобном темпе.

Расширенные материалы помогают замечать больше нюансов: как цена ведёт себя в разные моменты, какие уровни сильные, а какие временные. Это делает обучение более наглядным и динамичным.

Вы можете продолжать обучение постепенно, проходя по одному разделу за раз. Такой формат хорошо подходит новичкам и всем, кто хочет развивать финансовую грамотность аккуратно, без перегрузки.

Все материалы носят исключительно образовательный характер. Они созданы для того, чтобы помочь лучше понимать графики и поведение цены, а не для выдачи торговых рекомендаций."""


HELP_TEXT = """🤖 Этот бот создан для того, чтобы помочь вам разобраться в анализе цены через понятную пошаговую систему.

Что вы можете найти здесь:

• 📚 Полезные обучающие материалы
• 🧠 Пошаговое объяснение и поддержку
• 🤝💬 Прямую связь с поддержкой и автором проекта

Если у вас возникли вопросы или что-то работает неправильно, нажмите кнопку ниже, чтобы связаться с поддержкой."""


SUPPORT_TEXT = """💬 Есть вопросы по боту? Что-то не работает или нужна помощь?

Нажмите кнопку ниже, чтобы напрямую связаться с создателем проекта или технической поддержкой.

Напишите нам — мы поможем разобраться!"""


def start_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Что такое анализ цены", callback_data="price_analysis")
    kb.button(text="Помощь", callback_data="help")
    kb.button(text="Поддержка", callback_data="support")
    kb.adjust(1)
    return kb.as_markup()


def price_analysis_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Основы анализа цены", callback_data="price_basics")
    kb.button(text="Назад", callback_data="back_start")
    kb.adjust(1)
    return kb.as_markup()


def price_basics_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Как анализировать ситуацию на графике", callback_data="analyze_chart")
    kb.button(text="Назад", callback_data="back_price_analysis")
    kb.adjust(1)
    return kb.as_markup()


def analyze_chart_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Управление рисками", callback_data="risk_management")
    kb.button(text="Назад", callback_data="back_price_basics")
    kb.adjust(1)
    return kb.as_markup()


def risk_management_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Простой метод обучения", callback_data="simple_learning")
    kb.button(text="Назад", callback_data="back_analyze_chart")
    kb.adjust(1)
    return kb.as_markup()


def simple_learning_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Чек-лист", callback_data="checklist")
    kb.button(text="Назад", callback_data="back_risk_management")
    kb.adjust(1)
    return kb.as_markup()


def checklist_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Продолжить обучение", callback_data="continue_learning")
    kb.button(text="Назад", callback_data="back_simple_learning")
    kb.adjust(1)
    return kb.as_markup()


def continue_learning_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Обучающие материалы", url=CHANNEL_URL)
    kb.button(text="Назад", callback_data="back_checklist")
    kb.adjust(1)
    return kb.as_markup()


def help_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Поддержка", callback_data="support")
    kb.adjust(1)
    return kb.as_markup()


def support_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Связаться с поддержкой", url=SUPPORT_URL)
    kb.adjust(1)
    return kb.as_markup()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        START_TEXT,
        reply_markup=start_keyboard()
    )


@dp.callback_query(F.data == "back_start")
async def back_start_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        START_TEXT,
        reply_markup=start_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "price_analysis")
async def price_analysis_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        PRICE_ANALYSIS_TEXT,
        reply_markup=price_analysis_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "back_price_analysis")
async def back_price_analysis_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        PRICE_ANALYSIS_TEXT,
        reply_markup=price_analysis_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "price_basics")
async def price_basics_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        PRICE_BASICS_TEXT,
        reply_markup=price_basics_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "back_price_basics")
async def back_price_basics_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        PRICE_BASICS_TEXT,
        reply_markup=price_basics_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "analyze_chart")
async def analyze_chart_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        ANALYZE_CHART_TEXT,
        reply_markup=analyze_chart_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "back_analyze_chart")
async def back_analyze_chart_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        ANALYZE_CHART_TEXT,
        reply_markup=analyze_chart_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "risk_management")
async def risk_management_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        RISK_MANAGEMENT_TEXT,
        reply_markup=risk_management_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "back_risk_management")
async def back_risk_management_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        RISK_MANAGEMENT_TEXT,
        reply_markup=risk_management_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "simple_learning")
async def simple_learning_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        SIMPLE_LEARNING_METHOD_TEXT,
        reply_markup=simple_learning_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "back_simple_learning")
async def back_simple_learning_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        SIMPLE_LEARNING_METHOD_TEXT,
        reply_markup=simple_learning_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "checklist")
async def checklist_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        CHECKLIST_TEXT,
        reply_markup=checklist_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "back_checklist")
async def back_checklist_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        CHECKLIST_TEXT,
        reply_markup=checklist_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "continue_learning")
async def continue_learning_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        CONTINUE_LEARNING_TEXT,
        reply_markup=continue_learning_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        HELP_TEXT,
        reply_markup=help_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "support")
async def support_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        SUPPORT_TEXT,
        reply_markup=support_keyboard()
    )
    await callback.answer()


async def main():
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
