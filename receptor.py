
import paho.mqtt.client as mqtt
import time

#Servidor
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883
TOPIC = "gov/seguranca"

banco_de_dados = './Furto_2009-a-2024-Fortaleza.csv' #CSV


#Conectando
def on_connect(client, userdata, flags, rc, properties=None):

    if rc == 0:
        print(f"Conectado com sucesso ao broker {BROKER_ADDRESS}")
        # Subscreve ao tópico após a conexão ser estabelecida
        client.subscribe(TOPIC)
        print(f"Subscrito ao tópico: {TOPIC}")
    else:
        print(f"Falha ao conectar, código de retorno: {rc}")



'''
    NOTA: Função mais importante do receptor, mostra o comportamento do cliente/servidor ao receber uma mensagem, no caso, será nessa função que
    se receberá o valor do botão e onde será adicionado na planilha!

'''

def on_message(client, userdata, msg):
    

    mensagem_recebida = msg.payload.decode("utf-8")
    print("-" * 30)
    print(f"Mensagem recebida!")
    print(f"  Mensagem: {mensagem_recebida}")
    print("-" * 30)
    mensagem_recebida = mensagem_recebida + "\n"

    with open(banco_de_dados, "a") as file:
        file.write(mensagem_recebida)
        file.close()







#Gerando um client e passando os comportamento
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("Tentando se conectar ao broker MQTT...")


try:
    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
except Exception as e:
    print(f"Não foi possível conectar ao broker: {e}")
    exit()



#Faz com que o script fique rodando até alguém desligar
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nScript terminado pelo utilizador.")
    client.disconnect()
    print("Desconectado do broker.")
