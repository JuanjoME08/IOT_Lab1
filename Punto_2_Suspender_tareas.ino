//#include <Arduino_FreeRTOS.h>
#define Pinvoltaje 25
#define Pinboot 0

void tarea1(void *pvParameters);
void tarea2(void *pvParameters);

TaskHandle_t handleTask1;
TaskHandle_t handleTask2;

void setup() {

  Serial.begin(115200);
  pinMode(Pinvoltaje,INPUT);


  xTaskCreatePinnedToCore(
      Task1code, /* Function to implement the task */
      "Task1", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      10,  /* Priority of the task */
      &handleTask1,  /* Task handle. */
      1); /* Core where the task should run */

  xTaskCreatePinnedToCore(
      Task2code, /* Function to implement the task */
      "Task2", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      10,  /* Priority of the task */
      &handleTask2,  /* Task handle. */
      0); /* Core where the task should run */
}

void loop() {
  
}

void Task1code(void *pvParameters) {
  double lectura = 0;
  double voltaje = 0;
  
  while(1){

      Serial.print("Task 1 running on core ");
      Serial.print(xPortGetCoreID());
      lectura = analogRead(Pinvoltaje);
      voltaje = (lectura/4095)*3.3;
      Serial.print(" and voltage value is: ");
      Serial.println(voltaje);
      delay(1000);
  }
vTaskDelay(10);
}

void Task2code(void *pvParameters) {
  bool buttonWasPressed = false;
  bool Task1status = true;

  while(1){

    bool buttonState = digitalRead(Pinboot);

    if (buttonState == LOW && !buttonWasPressed) {
      buttonWasPressed = true;
    }
      
    if (buttonState == HIGH && buttonWasPressed) {
      buttonWasPressed = false;

        if(Task1status){
          vTaskSuspend(handleTask1);
          Serial.println("Task 1 suspended");
          Task1status = false;
        }else{
          vTaskResume(handleTask1);
          Task1status = true;
        }
      }
   delay(100);
  }
  vTaskDelay(10);
}
