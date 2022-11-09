#include <ESP8266WiFi.h> //Suporte ao WIFI
#include <WiFiClient.h> //Provê a comunicação no modo cliente
#include <ESP8266WebServer.h> //Servidor WEB para maniuplar requisições GET e POST
#include <ESP8266mDNS.h> //Multicast MDNS (Ex. esp8266.local)


const char* ssid = "node4"; //SSID do roteador WIFI
const char* password = "cc50e3c19eea"; //Senha do roteador WIFI

ESP8266WebServer server(80); //Cria um serviço WEB na porta 80

const int pinOut0 = 0; //Configura o pino 0 do ESP-01
const int pinOut2 = 2; //Configura o pino 2 do ESP-01
const bool statusR0 = false;
const bool statusR2 = false;

//Manipula as requisições recebidas na página principal
void handleRoot() { 

  for (uint8_t i=0; i<server.args(); i++){
    //Caso os parâmetros sejam relay0 e on -> liga o Relê 0
    if ((server.argName(i) == "relay0") && (server.arg(i) == "on") && (statusR0 == false)) {
        digitalWrite(pinOut0, HIGH);
        statusR0 = true;
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay0:on""}]");
    }else{
      server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay0:juston""}]");
    }
    //Caso os parâmetros sejam relay0 e on -> desliga o Relê 0    
    if ((server.argName(i) == "relay0") && (server.arg(i) == "off") && (statusR0 == true)) {
      digitalWrite(pinOut0, LOW);
      statusR0 = false;
      server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay0:off""}]");
  
    } else{
      server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay0:justoff""}]");
    }
      if ((server.argName(i) == "relay2") && (server.arg(i) == "on") && (relay2 == false)) {
        digitalWrite(pinOut0, HIGH);
        relay2 = true;
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay2:on""}]");
    }else{
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay2:juston""}]");
    }
    if ((server.argName(i) == "relay2") && (server.arg(i) == "off") && (relay2 == true)) {
        digitalWrite(pinOut0, LOW);
        relay2 = false;
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay2:off""}]");
    }else{
      server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay2:justoff""}]");
    }
  }
  //Caso seja recebido algum parâmetro incompatível, retorna msg de erro para o cliente
  server.send(200, "text/html; charset=utf-8", "Erro nos parâmetros");

}

//Se a página não existe, retorna página não encontrada
void handleNotFound() { 
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

//Configura os pinos digitais (0 e 2) e conecta no roteador WIFI
void setup(void) {
  pinMode(pinOut0, OUTPUT);
  pinMode(pinOut2, OUTPUT);
  digitalWrite(pinOut0, LOW);
  digitalWrite(pinOut2, LOW);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  //Publica o nome do dispositivo para ser consultado via mDNS (Ex. esp8266.local)
  if (MDNS.begin("node6")) {
    Serial.println("MDNS responder started");
  }

  //Publica o evento da página principal  
  server.on("/", handleRoot);

  //Publica o evento de página não encontrada
  server.onNotFound(handleNotFound);

  //Inicia o servidor WEB  
  server.begin();
  Serial.println("HTTP server started");
}

//Coloca o módulo em funcionamento e esperando requisições HTTP
void loop(void) {
  server.handleClient();
}
