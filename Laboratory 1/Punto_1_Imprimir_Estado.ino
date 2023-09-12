// GPIO pin for built in led

#define Pinvoltaje 25
#define pinboot 0



void Task1code( void * parameter) {
  int myCounter;
  double lectura = 0;
  double voltaje = 0;

  while(1){

    
    Serial.print("Task running on core ");
    Serial.print(xPortGetCoreID());
    lectura = analogRead(Pinvoltaje);
    voltaje = (lectura/4095)*3.3;
    Serial.print(" and voltage value is: ");
    Serial.println(voltaje);
    vTaskDelay(1000/portTICK_PERIOD_MS);
  } 
}

void Task2code( void * parameter) {
  int lecturaboot = 0;
  while(1){
    
    lecturaboot = (digitalRead(pinboot));
    
    Serial.print("\t\t\t\t\t\t Task running on core ");
    Serial.print(xPortGetCoreID());
    Serial.print(" and state pin boot value is: ");
    Serial.println(lecturaboot);
    vTaskDelay(50/portTICK_PERIOD_MS);
  }
}


void setup() {

  TaskHandle_t Task1,Task2;
  Serial.begin(115200);
  pinMode(Pinvoltaje,INPUT);
  // Built in led pint as outpt  
  Serial.print("setup() running on core ");
  Serial.println(xPortGetCoreID());

  xTaskCreatePinnedToCore(
      Task1code, /* Function to implement the task */
      "Task1", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      10,  /* Priority of the task */
      &Task1,  /* Task handle. */
      1); /* Core where the task should run */

  xTaskCreatePinnedToCore(
      Task2code, /* Function to implement the task */
      "Task2", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      10,  /* Priority of the task */
      &Task2,  /* Task handle. */
      0); /* Core where the task should run */
}

void loop() {
 // Clears loop function from OS
 vTaskDelete(NULL);
 delay(10000);
}
