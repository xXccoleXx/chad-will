#include <Arduino.h>

//include header for the ADXL345 class
#include "ADXL345.h"

//create a static instance of the ADXL345 class
ADXL345 accel;

/************************************************************************/
/* Place holder for x, y, and z axis readings. Could be done another way but
this is how I chose to implement :)
/************************************************************************/
int16_t xAxis=0;
int16_t yAxis=0;
int16_t zAxis=0;

//dummy variable for processing the magnitude
//long magnitude = 0;

// varibales used
  int idx = 0;
  
  const int A = 10;  //constant length of 10
  int mag[A+1];      // magnitudes
  int diff[A];     //differences
  int sqre[A];   // difference squared

  //float sum = 0;
  float avg = 0;       //some large value
  
  int steps = 0;
  //int wait = 0; // for step detection logic
  float previousavg = 1000000;

//vars to keep track of timing
long timeAcquire=0;
long timeProcess=0;
long timeDecide=0;
long algorithmDone=0;


/**
* \brief Function acquires data from either an online (ADXL345) or offline (data via Serial port) source
*
* \param _ONLINE_ENABLE True if source should be from "online"; otherwise will pull from Serial port
*
* \return void
*/
void acquire(bool _ONLINE_ENABLE, int16_t& xAxis, int16_t& yAxis, int16_t& zAxis)
{


  
  //acquire data from the ADXL345
  if(_ONLINE_ENABLE==true)
  { 
    xAxis = accel.getXAcceleteration();
    yAxis = accel.getYAcceleteration();
    zAxis = accel.getZAcceleteration();
  }
  
  //acquire data from the Serial port
  else  
  {   
    //wait for response
    while (Serial.available()==0)
    {
      //send '!' up the chain
      Serial.println('!');
      
      //spam the host until they respond :)
      delay(10);
    }
    
    //parse response attempt #2 (about 20ms with timeout)
    int x_accel = Serial.parseInt();
    int y_accel = Serial.parseInt();
    int z_accel = Serial.parseInt();
    
    xAxis=x_accel;
    yAxis=y_accel;
    zAxis=z_accel;
  }
}

float calcavg(int sqre[]) {
  float sum = 0;
  for (int i = 0; i < A; i++) 
  {
    sum += sqre[i];
  }
  avg = sum / A;
  return avg;
  
  
}

/**
* \brief Function to process all data before a decision is rendered. Should be mostly diff, squaring, summing...etc
    will be modified based upon each individual's implementation
*
* \return void
*/
void process()
{
    //ALL YOUR SIGNAL PROCESSING CODE HERE!
    mag[idx % (A +1)] = sqrt((xAxis*xAxis) + (yAxis*yAxis) + (zAxis*zAxis)); // calculate magnitude
    diff[idx % A] = mag[idx % (A + 1)] - mag[(idx - 1) % (A + 1)]; // calculate difference of mag
    sqre[idx % A] = diff[idx % A] * diff[idx % A]; // calculate square of difference

  return;
}

//    if (idx > 10) // array full
//    {
//      double value = 0; 
//      for (int i = 0; i < 10; i++) // loop average calc 
//      {
//        value += sqre[(idx-10+i) % 10];
//      }
//      avg[idx] = value / 10;
//      
//      //cout << "average: " << avg[idx] ; 
   



/**
* \brief Run the step decision algorithm.
*
* \return void
*/
void decide()
{
 
if (idx % A == 0) {
  avg = calcavg(sqre);
  }

  float currentavg = avg;
  if (currentavg > 250 && currentavg > previousavg) {
  steps += 1;
  }
  previousavg = currentavg;
  idx++;
 return;
}

/**
* \brief Report the algorithm results back to the PC
*
* \return void
*/
void report()
{
  //calculate how long the acquire() took
  long time_to_acquire = timeProcess - timeAcquire;
  
  //calculate how long the processs() took
  long time_to_process = timeProcess - timeDecide;
  
  //calculate how long the decide() took
  long time_to_decide = timeDecide - algorithmDone;
  
  //print all back to host PC
  Serial.print("steps="); 
  Serial.print(steps);
  Serial.print(",");
  Serial.print(time_to_acquire); 
  Serial.print(","); 
  Serial.print(time_to_process); 
  Serial.print(",");
  Serial.print(time_to_decide);
  Serial.println(",");

}

void setup() {

  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,HIGH);

  //**Step #1: Initialize the ADXL345 and select your CS pin**
  accel.setup(7);
  
  //**Step #2: Perform a self-test to see if you can read
  //from the accelerometer. Device will not progress is self-test fails.
  bool success = accel.selfTest();
  
  //infinite loop if self-test fails
  while(!success){}
  
  //initialize serial
  Serial.begin(9600);
  
  //this is imperative. If otherwise all read operations take 1s
  Serial.setTimeout(10);
}


//flag to determine whether we're in online or offline mode
const boolean ONLINE_MODE=false;

//flag to keep track of LED state
boolean led_state = HIGH;

void loop() 
{
  /************************************************************************/
  /*  Acquire data from either the ADXL345 (online) or the Serial port (offline)
  /************************************************************************/
  timeAcquire=millis();
  acquire(ONLINE_MODE,xAxis,yAxis,zAxis);
  
  //blink an LED to ensure we're receiving data
  
  led_state=(led_state==HIGH)?(LOW):(HIGH);
  digitalWrite(LED_BUILTIN,led_state);
  
  /************************************************************************/
  /*  Process the data that has been acquired. This should be all the diff, squaring...etc. functions
  /************************************************************************/
  timeProcess=millis();
  process();
  
  /************************************************************************/
  /*  Based upon the data that has been collected, render some decision and report it back up the chain
  /************************************************************************/
  timeDecide=millis();
  decide();
  
  /************************************************************************/
  /*  Now that all calculations have completed; report back to the host PC
  /************************************************************************/
  algorithmDone=millis();
  report();
  
  
  delay(10);

}
