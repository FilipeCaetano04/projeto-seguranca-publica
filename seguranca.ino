#include <WiFi.h>
#include <ctime>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

#define button 4

//Ajuste de data e hora
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -3 * 3600;
const int daylightOffset_sec = 0;

const char* ssid = "brisa-1760147";
const char* password = "pnril0ir";

const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;


WiFiClient espClient;
PubSubClient client(espClient);
String endereco = "gov/seguranca";



time_t curtime;
int timer;
int dT = 1000;



bool pressionado = false;


char buffer[100];
struct Local{
  short AIS;
  String municipio;
  String dia_da_semana;
  short dia;
  short mes;
  short ano;
  short hora;
  short minuto;
  short segundo;
};


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESPCLIENT";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }

  
}


void set_wifi() {
  Serial.println("Conectando ao Wi-Fi...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }


  Serial.println("\nConectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}




/*
struct Local{
  short AIS;
  String Município;
  String dia_da_semana;
  short dia;
  short mês;
  short ano;
  short hora;
};
*/

void sendData() {



  Local local = {
    .AIS = 5,
    .municipio = "Fortaleza",
    .dia_da_semana = "Sexta",
    .dia = 29,
    .mes = 9,
    .ano = 2025,
    .hora = 1,
    .minuto = 33,
    .segundo = 1,

  };

  sprintf(buffer , "AIS %0.2d,%s,%s,%0.4d-%0.2d-%0.2d,%0.2d:%0.2d:%0.2d", 
  local.AIS, local.municipio, local.dia_da_semana, local.ano, 
  local.mes, local.dia, local.hora, local.minuto, local.segundo);

  String response = String(buffer);

  bool resp = client.publish(endereco.c_str(), response.c_str());

  if (resp == 1) Serial.printf("Enviado: %s\n", response.c_str());
  else Serial.printf("falha ao enviar dados\n");
}




void setup() {
  srand(time(nullptr));

  Serial.begin(115200);
  delay(1000);



  set_wifi();
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  //espClient.setInsecure();

  client.setServer(mqtt_server, mqtt_port);

//Limite do buffer em bytes
 // client.setBufferSize(8192);


  pinMode(button, INPUT);

  timer = millis();
}



void loop() {
  time(&curtime);


  if (!client.connected()) {
    reconnect();
  }


  while(digitalRead(button)){
    pressionado = true;
  }

  

  if (millis() - timer > dT) {
      

    Serial.printf("Incio Loop:\n");
    Serial.printf("Botão Pressionado: %d\n", pressionado);
    if(pressionado == true){
      sendData();
      pressionado = false;
    }
    

    timer = millis();

    Serial.printf("Fim Loop:\n");
  }

}
