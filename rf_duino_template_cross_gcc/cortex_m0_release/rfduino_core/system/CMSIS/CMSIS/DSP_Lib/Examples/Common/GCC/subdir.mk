################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
S_UPPER_SRCS += \
../rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Examples/Common/GCC/startup_ARMCM0.S \
../rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Examples/Common/GCC/startup_ARMCM3.S \
../rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Examples/Common/GCC/startup_ARMCM4.S 

OBJS += \
./rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Examples/Common/GCC/startup_ARMCM0.o \
./rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Examples/Common/GCC/startup_ARMCM3.o \
./rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Examples/Common/GCC/startup_ARMCM4.o 


# Each subdirectory must supply rules for building sources it contributes
rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Examples/Common/GCC/%.o: ../rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Examples/Common/GCC/%.S
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Assembler'
	arm-none-eabi-as -I"/home/remi/Outils Developpement/Embarqué/Arduino/IDE/arduino-1.5.2/hardware/arduino/RFduino/cores/arduino" -I"/home/remi/Outils Developpement/Embarqué/Arduino/IDE/arduino-1.5.2/hardware/arduino/RFduino/variants/RFduino" -I"/home/remi/Outils Developpement/Embarqué/Arduino/IDE/arduino-1.5.2/hardware/arduino/RFduino/system/RFduino" -I"/home/remi/Outils Developpement/Embarqué/Arduino/IDE/arduino-1.5.2/hardware/arduino/RFduino/system/RFduino/Include" -I"/home/remi/Outils Developpement/Embarqué/Arduino/IDE/arduino-1.5.2/hardware/arduino/RFduino/system/CMSIS/CMSIS/Include" -I../rf_duino_template_cross_gcc/arduino_libraries/RFduinoBLE -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


