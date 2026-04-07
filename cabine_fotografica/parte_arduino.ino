Botão
Pino 1 → Arduino pino 2
Pino 2 → GND

------------------------------------------------------------

const int botao = 2;

void setup() {
  pinMode(botao, INPUT_PULLUP); 
  Serial.begin(9600);
}

void loop() {

  if (digitalRead(botao) == LOW) {   // botão pressionado
    Serial.println("Capture");       // envia comando ao PC
    delay(1000);                     // evita múltiplos disparos
  }

}