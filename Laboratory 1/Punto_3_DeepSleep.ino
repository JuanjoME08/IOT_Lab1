//#include <Arduino_FreeRTOS.h>
#define TIME_TO_SLEEP 20
#define Pinvoltaje 25
#define Pinboot 0


void tarea1(void *pvParameters);
void tarea2(void *pvParameters);
RTC_DATA_ATTR bool Task1status = true;


TaskHandle_t handleTask1;
TaskHandle_t handleTask2;

void setup() {

  Serial.begin(115200);
  pinMode(Pinvoltaje,INPUT);

  if (Task1status == false){
    Serial.println("Task 1 suspended");
  }


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
      1,  /* Priority of the task */
      &handleTask2,  /* Task handle. */
      0); /* Core where the task should run */
}

void loop() {
  
}

void Task1code(void *pvParameters) {
  double lectura = 0;
  double voltaje = 0;
  
  while(1){

    if (Task1status){
      Serial.print("Task 1 running on core ");
      Serial.print(xPortGetCoreID());
      lectura = analogRead(Pinvoltaje);
      voltaje = (lectura/4095)*3.3;
      Serial.print(" and voltage value is: ");
      Serial.println(voltaje);
      }else{
      vTaskSuspend(NULL);
     }
  delay(1000);
  }
vTaskDelay(10);
}

void Task2code(void *pvParameters) {
  unsigned long buttonPressStartTime = 0;
  bool buttonWasPressed = false;

  while(1){

    bool buttonState = digitalRead(Pinboot);

    if (buttonState == LOW && !buttonWasPressed) {
      buttonWasPressed = true;
      buttonPressStartTime = millis();
    }
      
    if (buttonState == HIGH && buttonWasPressed) {
      buttonWasPressed = false;

      if (millis() - buttonPressStartTime < 10000) {
        if(Task1status){
          vTaskSuspend(handleTask1);
          Serial.println("Task 1 suspended");
          Task1status = false;
        }else{
          vTaskResume(handleTask1);
          Task1status = true;
        }
      }else {
        esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * 1000000);
        Serial.print("Esp entering deep sleep mode");
        vTaskDelay(10/portTICK_PERIOD_MS);
        esp_deep_sleep_start();
      }
   }
   delay(100);
  }
  vTaskDelay(10);
}
