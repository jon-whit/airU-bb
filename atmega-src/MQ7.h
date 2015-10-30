#ifndef CS_MQ7_H
#define CS_MQ7_H

#include <Arduino.h>

#define HIGH_TIME 60000
#define LOW_TIME 90000

class CS_MQ7 {

    public:

        CS_MQ7(int COVREG_G_Pin, int COVREG_EN_Pin);
        void CoPwrCycler();
        boolean CurrentState();

        unsigned long currTime;
        unsigned long prevTime;
        unsigned long currCoPwrTimer;
        boolean CoPwrState;

    private:
        int _COVREG_G_Pin;
        int _COVREG_EN_Pin;
        int _COVREG_G;
        int _COVREG_EN;

};

#endif
