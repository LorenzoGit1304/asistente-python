import speech_recognition as sr
import pyttsx3
import openai
from datetime import datetime

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Asistente: Escuchando...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language="es-ES")
        print("Tú: " + command)
        return command
    except sr.UnknownValueError:
        print("Asistente: Lo siento, no pude entender lo que dijiste.")
        return ""
    except sr.RequestError:
        print("Asistente: Lo siento, ha ocurrido un error en la conexión con el servicio de reconocimiento de voz.")
        return ""

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()


def add_task(task, task_file):
    with open(task_file, "a") as file:
        file.write(task + "\n")

def read_tasks(task_file):
    tasks = []
    with open(task_file, "r") as file:
        tasks = file.read().splitlines()
    return tasks

def write_tasks(tasks, task_file):
    with open(task_file, "w") as file:
        for task in tasks:
            file.write(task + "\n")

def search_web(query):
    openai.api_key = "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"  
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Buscar en la web: {query}"}
        ]
    )
    answer = response.choices[0].message['content'].strip()
    return answer

# def set_reminder(reminder_time, reminder_text):
#     now = datetime.now()
#     reminder_time = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
    
#     if reminder_time > now:
#         time_difference = (reminder_time - now).total_seconds()
#         reminder_timer = threading.Timer(time_difference, remind, args=[reminder_text])
#         reminder_timer.start()
#         print(f"Asistente: Recordatorio programado para {reminder_time}.")
#         speak(f"Recordatorio programado para {reminder_time}.")
#     else:
#         print("Asistente: La hora del recordatorio ya ha pasado. Por favor, elige una hora futura.")
#         speak("La hora del recordatorio ya ha pasado. Por favor, elige una hora futura.")

def remind(reminder_text):
    print(f"Asistente: Recordatorio: {reminder_text}")
    speak(f"Recordatorio: {reminder_text}")

def main():
    task_file = "tasks.txt"
    tasks = read_tasks(task_file)

    print("Hola, ¿en qué puedo ayudarte?")
    speak("Hola, ¿en qué puedo ayudarte?")

    while True:
        command = listen().lower()

        if "agregar tarea" in command:
            task = command.replace("agregar tarea", "").strip()
            if task:
                tasks.append(task)
                add_task(task, task_file)
                speak("Tarea agregada " + task)
                
            else:
                print("No has especificado una tarea para agregar.")
                speak("No has especificado una tarea para agregar.")
                

        elif "ver tareas" in command:
            if tasks:
                speak("Tareas:")
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task}")
                    speak(f"{index}. {task}")
            else:
                print("No tienes tareas pendientes.")
                speak("No tienes tareas pendientes.")
                
        # elif "recordar" in command:
        #     speak("¿Qué texto deseas recordar?")
        #     reminder_text = listen()
        #     if reminder_text:
        #         speak("¿Cuándo deseas que te recuerde eso? Por favor, especifica la fecha y hora en el formato 'AAAA-MM-DD HH:MM'.")
        #         reminder_time = listen()
        #         if reminder_time:
        #             set_reminder(reminder_time, reminder_text)
        #         else:
        #             print("No se detectó ninguna fecha y hora válida. Por favor, intenta nuevamente.")
        #             speak("No se detectó ninguna fecha y hora válida. Por favor, intenta nuevamente.")
        #     else:
        #         print("No se detectó ningún texto para recordar. Por favor, intenta nuevamente.")
        #         speak("No se detectó ningún texto para recordar. Por favor, intenta nuevamente.")


        elif "pregunta" in command:
            print("¿Qué deseas preguntar?")
            speak("¿Qué deseas preguntar?")
            query = listen()
            if query:
                speak("Buscando en la web: "+ query)
                search_result = search_web(query)
                print(search_result)
                speak(search_result)
            else:
                print("No se detectó ninguna consulta. Por favor, intenta nuevamente.")
                speak("No se detectó ninguna consulta. Por favor, intenta nuevamente.")

        elif "salir" in command:
            print("Hasta luego.")
            speak("Hasta luego.")
            break

        else:
            print("Lo siento, no entiendo ese comando.")
            speak("Lo siento, no entiendo ese comando.")

if __name__ == "__main__":
    main()
