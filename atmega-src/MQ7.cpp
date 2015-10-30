#include <Arduino.h>
#include "MQ7.h"

CS_MQ7::CS_MQ7(int COVREG_G_Pin, int COVREG_EN_Pin)
{

    pinMode(COVREG_G_Pin, OUTPUT);
    pinMode(COVREG_EN_Pin, OUTPUT);

    _COVREG_G_Pin = COVREG_G_Pin;
    _COVREG_EN_Pin = COVREG_EN_Pin;

    currTime = 0;
    prevTime = 0;
    currCoPwrTimer = 0;
    CoPwrState = HIGH;
    currCoPwrTimer = 500;

}

void CS_MQ7::CoPwrCycler()
{
    currTime = millis();

    if (currTime - prevTime > currCoPwrTimer) {
        prevTime = currTime;

        if(CoPwrState == LOW) {
            CoPwrState = HIGH;
            _COVREG_G = LOW;
            _COVREG_EN = HIGH;

            currCoPwrTimer = HIGH_TIME;  // 60 seconds at 5V
        }
    else {
      CoPwrState = LOW;
      _COVREG_G = HIGH;
      _COVREG_EN = LOW;

      currCoPwrTimer = LOW_TIME;  // 90 seconds at 1.5V
    }
    digitalWrite(_COVREG_G_Pin, _COVREG_G);
    digitalWrite(_COVREG_EN_Pin, _COVREG_EN);
  }
}

boolean CS_MQ7::CurrentState()
{
    if(CoPwrState == LOW) {
        return false;
    }
    else {
        return true;
    }
}
