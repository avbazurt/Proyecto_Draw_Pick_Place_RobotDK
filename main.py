"""Autor: Adrian Vidal Bazurto Onofre
Detalles completos del proyecto en https://github.com/TheLast20/Proyecto_Draw_Pick_Place_RobotDK

Por la presente se otorga permiso, sin cargo, a cualquier persona que obtenga una copia.
de este software y los archivos de documentación asociados.

El aviso de copyright anterior y este aviso de permiso se incluirán en todos
copias o partes sustanciales del Software."""


from data.draw import RobotDraw
from data.camera import RobotPicture
from data.move import RobotMove

from time import sleep

from functools import partial
import logging
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


TEXTO, TAMAÑO, COLOR, VALIDAR, FINAL = range(5)


def start(update: Update, context: CallbackContext,RobotMove) -> int:
    RobotMove.ColocarHojaNueva()
    update.message.reply_text(
        "Ingrese el texto a trazar, no mas de 10 letras por palabra",
    )
    return TAMAÑO


def definir_tamaño(update: Update, context: CallbackContext) -> int:
    # Guardamos el texto escrito
    context.user_data["texto"] = update.message.text

    # Creamos el menu
    menu = [["10", "20"], ["30", "40"], ["50", "60"]]
    markup = ReplyKeyboardMarkup(menu, one_time_keyboard=True)

    update.message.reply_text(
        "De que tamaño le gustaria trazar las letras, valores en mm",
        reply_markup=markup
    )

    return COLOR


def definir_color(update: Update, context: CallbackContext) -> int:
    # Guardamos el color escrito
    context.user_data["tamaño"] = update.message.text

    # Creamos el menu
    menu = [["RED", "BLUE", "GREEN", ], ["YELLOW", "BLACK", "ORANGE"], ["LETRA RANDOM", "PALABRA RANDOM"]]

    texto = """Ingrese el color con el que se trazara sus letras

LETRA RANDOM: Cada letra sera trazada con un color random diferente
PALABRA RANDOM: Cada palabra sera trazada con un color random diferente
    """

    markup = ReplyKeyboardMarkup(menu, one_time_keyboard=True)

    update.message.reply_text(
        texto,
        reply_markup=markup
    )

    return VALIDAR


def validar_datos(update: Update, context: CallbackContext) -> int:
    # Guardamos el color escrito
    context.user_data["color"] = update.message.text
    print(context.user_data)

    texto = """Resumen Trazo:
Mensaje:
{}

Tamaño:
{} mm

Color:
{}

Presione INICIAR para empezar con el trazo
Presione CANCELAR para terminar la ejecucion
""".format(context.user_data["texto"], context.user_data["tamaño"], context.user_data["color"])

    menu = [["INICIAR", ], ["CANCELAR"]]

    markup = ReplyKeyboardMarkup(menu, one_time_keyboard=True)

    update.message.reply_text(
        texto,
        reply_markup=markup
    )
    return FINAL


def ejecutar_dibujo(update: Update, context: CallbackContext, RobotDraw, RobotPicture,RobotMove) -> None:
    texto = context.user_data["texto"]
    tamaño = context.user_data["tamaño"]
    color = context.user_data["color"]

    dic_color = {
        "RED": "red",
        "BLUE": "blue",
        "GREEN": RobotDraw.GenerarRGBACode(0, 255, 0, 255),
        "YELLOW": "yellow",
        "BLACK": RobotDraw.GenerarRGBACode(0, 0, 0, 255),
        "ORANGE": RobotDraw.GenerarRGBACode(255, 111, 0, 255),
    }

    text = "Realizando el trazo"
    context.bot.sendMessage(text=text, parse_mode="HTML", chat_id=update.message.from_user.id)


    RobotDraw.UpdateHoja(RobotMove.actual)
    #RobotDraw.LimpiarPizarra()


    for palabra in texto.split(" "):
        if color == "PALABRA RANDOM":
            codigo_color = RobotDraw.GenerateRandomColor()
        elif color != "LETRA RANDOM":
            codigo_color = dic_color[color]

        for letra in palabra:
            if color == "LETRA RANDOM":
                codigo_color = RobotDraw.GenerateRandomColor()

            RobotDraw.DrawLetra(letra, tamaño, codigo_color)
        RobotDraw.Enter()
    RobotDraw.Final()

    RobotPicture.TomarFoto()

    sleep(2)
    RobotMove.QuitarHoja()

    context.bot.send_photo(chat_id=update.message.chat_id,photo=open("recourses/foto.png",'rb'),caption="Resultado Final")
    context.bot.sendMessage(text=text, parse_mode="HTML", chat_id=update.message.from_user.id)


    text = "Si deseas volver a utilizarme presiona /start"
    context.bot.sendMessage(text=text, parse_mode="HTML", chat_id=update.message.from_user.id)
    return ConversationHandler.END


def cancelar_dibujo(update: Update, context: CallbackContext) -> None:
    text = "Parece que has cancelado la Ejecucion, porfavor presiona /start para volver intentarlo "
    context.bot.send_messagecontext.bot.sendMessage(text=text, parse_mode="HTML", chat_id=update.message.from_user.id)
    return ConversationHandler.END


if __name__ == '__main__':
    # Enable logging ----------------------------------
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    updater = Updater("1865261960:AAHa2Km0ohpmuHwH1-wqkrDrWfQBnvc6p4E")
    dispatcher = updater.dispatcher

    Vidal = RobotDraw()
    Bazurto = RobotPicture()
    Onofre = RobotMove()

    f_ejecutar_dibujo = partial(ejecutar_dibujo, RobotDraw=Vidal,RobotPicture=Bazurto,RobotMove=Onofre)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', partial(start,RobotMove=Onofre))],
        states={
            TAMAÑO: [MessageHandler(Filters.text, definir_tamaño)],
            COLOR: [MessageHandler(Filters.text, definir_color)],
            VALIDAR: [MessageHandler(Filters.text, validar_datos)],
            FINAL: [MessageHandler(Filters.regex('^INICIAR$'), f_ejecutar_dibujo),
                    MessageHandler(Filters.regex('^CANCELAR$'), cancelar_dibujo)]

        },
        fallbacks=[MessageHandler(Filters.regex('^DONE$'), cancelar_dibujo)],
    )

    dispatcher.add_handler(conv_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
