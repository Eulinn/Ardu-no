#include <ESP8266WiFi.h> //Suporte ao WIFI
#include <WiFiClient.h> //Provê a comunicação no modo cliente
#include <ESP8266WebServer.h> //Servidor WEB para maniuplar requisições GET e POST
#include <ESP8266mDNS.h> //Multicast MDNS (Ex. esp8266.local)


const char* ssid = "node6"; //SSID do roteador WIFI
const char* password = "840D8EAD9973"; //Senha do roteador WIFI

ESP8266WebServer server(80); //Cria um serviço WEB na porta 80

const int pinOut0 = 0; //Configura o pino 0 do ESP-01
const int pinOut2 = 2; //Configura o pino 2 do ESP-01

//Manipula as requisições recebidas na página principal
void handleRoot() { 

  for (uint8_t i=0; i<server.args(); i++){
    //Caso os parâmetros sejam relay0 e on -> liga o Relê 0
    if ((server.argName(i) == "relay0") && (server.arg(i) == "on")) {
      if(digitalRead(pinOut0)){
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay0:juston""}]");
      }else{
        digitalWrite(pinOut0, HIGH);
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay0:on""}]");
        }

    }
    //Caso os parâmetros sejam relay0 e on -> desliga o Relê 0    
    else if ((server.argName(i) == "relay0") && (server.arg(i) == "off")) {
      if(!digitalRead(pinOut0)){
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay0:justoff""}]");
      }else{
        digitalWrite(pinOut0, LOW);
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay0:off""}]");
      }
      
      
    //Caso os parâmetros sejam relay2 e on -> liga o Relê 2 por 50ms e depois desliga o Relê
    } else if ((server.argName(i) == "relay2") && (server.arg(i) == "on")) {
      if(digitalRead(pinOut0)){
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay2:juston""}]");
      }else{
        digitalWrite(pinOut0, HIGH);
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay2:on""}]");
        }
    } else if ((server.argName(i) == "relay2") && (server.arg(i) == "off")) {
      if(!digitalRead(pinOut0)){
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay2:justoff""}]");
      }else{
        digitalWrite(pinOut0, LOW);
        server.send(200,"Content-Type: application/json; charset=utf-8","[{""relay2:off""}]");
      }
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
