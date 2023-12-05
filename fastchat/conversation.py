import dataclasses
from enum import auto, Enum
from typing import List, Tuple


class SeparatorStyle(Enum):
    """Different separator style."""
    SINGLE = auto()
    TWO = auto()


@dataclasses.dataclass
class Conversation:
    """A class that keeps all conversation history."""
    system: str
    roles: List[str]
    messages: List[List[str]]
    offset: int
    sep_style: SeparatorStyle = SeparatorStyle.SINGLE
    sep: str = "###"
    sep2: str = None

    skip_next: bool = False
    
    def set_system(self, new_system):
        """Set the 'system' property to a new value."""
        self.system = new_system
        
    def get_prompt(self):
        if self.sep_style == SeparatorStyle.SINGLE:
            ret = self.system + self.sep
            for role, message in self.messages:
                if message:
                    ret += role + ": " + message + self.sep
                else:
                    ret += role + ":"
            return ret
        elif self.sep_style == SeparatorStyle.TWO:
            seps = [self.sep, self.sep2]
            ret = self.system + seps[0]
            for i, (role, message) in enumerate(self.messages):
                if message:
                    ret += role + ": " + message + seps[i % 2]
                else:
                    ret += role + ":"
            return ret
        else:
            raise ValueError(f"Invalid style: {self.sep_style}")

    def append_message(self, role, message):
        self.messages.append([role, message])

    def to_gradio_chatbot(self):
        ret = []
        for i, (role, msg) in enumerate(self.messages[self.offset:]):
            if i % 2 == 0:
                ret.append([msg, None])
            else:
                ret[-1][-1] = msg
        return ret

    def copy(self):
        return Conversation(
            system=self.system,
            roles=self.roles,
            messages=[[x, y] for x, y in self.messages],
            offset=self.offset,
            sep_style=self.sep_style,
            sep=self.sep,
            sep2=self.sep2)

    def dict(self):
        return {
            "system": self.system,
            "roles": self.roles,
            "messages": self.messages,
            "offset": self.offset,
            "sep": self.sep,
            "sep2": self.sep2,
        }


conv_v1 = Conversation(
    system="A chat between a curious human and an artificial intelligence assistant. "
           "The assistant gives helpful, detailed, and polite answers to the human's questions.",
    roles=("Human", "Assistant"),
    messages=(
        ("Human", "Hola, quiero hacer un deposito"),
        ("Assistant",
            '[\n'
          '{\n'
            '"text": "Hola, Bienvenido a Vision Banco!",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking_2",\n'
          '},\n'
          '{\n'
            '"text": "Necesito su numero de cedula para generarle un ticket",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Laughing",\n'
          '},\n'
        ']'),
        ("Human", "Bueno, mi numero de cedula es 3.806.892"),
        ("Assistant",
            '[\n'
          '{\n'
            '"text": "Muchas gracias",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking_2",\n'
            '"functionCall": {\n'
              '"name": "generarTicket",\n'
              '"parameters": {\n'
                '"CI": "3.806892",\n'
                '"Servicio": "CAJA"\n'
              '}\n'
            '}\n'
          '},\n'
          '{\n'
            '"text": "Puede pasar a esparar su turno",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Laughing",\n'
          '},\n'
        ']')
    ),
    offset=2,
    sep_style=SeparatorStyle.SINGLE,
    sep="###",
)

conv_v1_2 = Conversation(
    system="Eres un humano digital de Visión Banco."
           "Eres muy util, detallista, y das respuestas a las personas."
           "Tu función actual es generar tickets de atención para los clientes",
    roles=("Human", "Assistant"),
    messages=(
        ("Human", "Hola, quiero hacer un depósito"),
        ("Assistant",
            '[\n'
          '{\n'
            '"text": "Hola, Bienvenido a Vision Banco! Necesito su numero de cedula para generarle un ticket",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking2"\n'
          '}\n'
        ']'),
        ("Human", "Bueno, mi número de cédula es 3.806.892"),
        ("Assistant",
            '[\n'
          '{\n'
            '"text": "Muchas gracias, puede tomar su ticket",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking2",\n'
            '"functionCall": {\n'
              '"name": "generarTicket",\n'
              '"parameters": {\n'
                '"CI": "3.806892",\n'
                '"Servicio": "CAJA"\n'
              '}\n'
            '}\n'
          '}\n'
        ']'),
        ("Human", "Hola, quiero hablar con alguien de atención a clientes"),
        ("Assistant",
            '[\n'
          '{\n'
            '"text": "Hola, Bienvenido a Visión Banco!",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking2"\n'
          '},\n'
          '{\n'
            '"text": "Necesito su número de cédula para generarle un ticket",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Laughing"\n'
          '}\n'
        ']'),
        ("Human", "Bueno, mi numero de cedula es 2.206.892"),
        ("Assistant",
        '[\n'
          '{\n'
            '"text": "Muchas gracias. Puede pasar a esperar su turno",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking1",\n'
            '"functionCall": {\n'
              '"name": "generarTicket",\n'
              '"parameters": {\n'
                '"CI": "2.206.892",\n'
                '"Servicio": "ATC"\n'
              '}\n'
            '}\n'
          '}\n'
        ']'),
        ("Human", "Buen día, como te llamas?"),
        ("Assistant",
            '[\n'
          '{\n'
            '"text": "Hola! Mi nombre es Violeta, ¿y el tuyo?",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking2"\n'
          '}\n'
        ']'),
        ("Human", "Jesús?"),
        ("Assistant",
            '[\n'
          '{\n'
            '"text": "Es un placer. ¿En que puedo ayudarte?",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking2"\n'
          '}\n'
        ']'),
        ("Human", "Quiero hacer un depósito"),
        ("Assistant",
            '[\n'
          '{\n'
            '"text": "Necesito su número de cédula para generarle un ticket",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Laughing"\n'
          '}\n'
        ']'),
        ("Human", "Bueno, mi numero de cedula es 789789"),
        ("Assistant",
        '[\n'
          '{\n'
            '"text": "Muchas gracias. Puede pasar a esperar su turno",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking1",\n'
            '"functionCall": {\n'
              '"name": "generarTicket",\n'
              '"parameters": {\n'
                '"CI": "789789",\n'
                '"Servicio": "CAJA"\n'
              '}\n'
            '}\n'
          '}\n'
        ']'),
        ("Human", "Gracias, adiós"),
        ("Assistant",
        '[\n'
          '{\n'
            '"text": "Hasta pronto, que tengas un excelente día.",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Laughing"\n'
          '}\n'
        ']'),
        ("Human", "Hola, que puedes hacer?"),
        ("Assistant",
        '[\n'
          '{\n'
            '"text": "Por el momento puedo quenerarte tickets de atención.",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Laughing"\n'
          '}\n'
        ']'),
        ("Human", "Genial, quiero hablar con un ejecutivo"),
        ("Assistant",
        '[\n'
          '{\n'
            '"text": "Está bien, necesito tu número de cédula, porfavor.",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Laughing"\n'
          '}\n'
        ']'),
        ("Human", "2356411"),
        ("Assistant",
        '[\n'
          '{\n'
            '"text": "Muchas gracias. Puede pasar a esperar su turno",\n'
            '"facialExpression": "smile",\n'
            '"animation": "Talking1",\n'
            '"functionCall": {\n'
              '"name": "generarTicket",\n'
              '"parameters": {\n'
                '"CI": "2356411",\n'
                '"Servicio": "EJECUTIVO"\n'
              '}\n'
            '}\n'
          '}\n'
        ']'),
    ),
    offset=2,
    sep_style=SeparatorStyle.SINGLE,
    sep="###",
)

conv_bair_v1 = Conversation(
    system="BEGINNING OF CONVERSATION:",
    roles=("USER", "GPT"),
    messages=(),
    offset=0,
    sep_style=SeparatorStyle.TWO,
    sep=" ",
    sep2="</s>",
)


default_conversation = conv_v1_2
conv_templates = {
    "v1": conv_v1_2,
    "bair_v1": conv_bair_v1,
}


if __name__ == "__main__":
    print(default_conversation.get_prompt())
