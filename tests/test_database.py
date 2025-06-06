import uuid
from data_base.threads_repository import ThreadsRepository
from data_base.messages_repository import MessagesRepository

USER_ID = 1
PROVIDER = "test-insert"
MENSAJE_USUARIO = "Mensaje de prueba del usuario."
RESPUESTA_ASISTENTE = "Respuesta simulada del asistente."

def test_insert_thread_and_messages():
    id_thread = str(uuid.uuid4())

    # Insertar hilo
    threadsid = ThreadsRepository.create_thread(
        user_id=USER_ID,
        provider=PROVIDER,
        status='test',
        id_thread=id_thread,
        description='Hilo de prueba para validación de inserción'
    )

    assert threadsid is not None

    MessagesRepository.create_message(
        thread_id=threadsid,
        type_='user',
        content=MENSAJE_USUARIO
    )

    MessagesRepository.create_message(
        thread_id=threadsid,
        type_='assistant',
        content=RESPUESTA_ASISTENTE
    )

    print(f"[✔] Inserción exitosa: hilo={id_thread} (THREADSID={threadsid})")
    print(f"[→] Usuario: {MENSAJE_USUARIO}")
    print(f"[←] Asistente: {RESPUESTA_ASISTENTE}")

    # Validaciones
    mensajes = MessagesRepository.get_messages_by_thread(threadsid)
    assert len(mensajes) == 2
    assert mensajes[0]['TYPE'] == 'user'
    assert mensajes[0]['CONTENT'] == MENSAJE_USUARIO
    assert mensajes[1]['TYPE'] == 'assistant'
    assert mensajes[1]['CONTENT'] == RESPUESTA_ASISTENTE
