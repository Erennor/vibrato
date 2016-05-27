################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../rfduino_core/libraries/RFduinoGZLL/RFduinoGZLL.cpp 

OBJS += \
./rfduino_core/libraries/RFduinoGZLL/RFduinoGZLL.o 

CPP_DEPS += \
./rfduino_core/libraries/RFduinoGZLL/RFduinoGZLL.d 


# Each subdirectory must supply rules for building sources it contributes
rfduino_core/libraries/RFduinoGZLL/%.o: ../rfduino_core/libraries/RFduinoGZLL/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cross G++ Compiler'
	arm-none-eabi-g++ -DF_CPU=16000000 -DARM_MATH_CM0 -Dprintf=iprintf -DARDUINO=157 -D__RFduino__ -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/RFduinoBLE" -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher/nrf51822/Include -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/cores/arduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/variants/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino/include" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/CMSIS/CMSIS/Include" -Os -g -Wall -c -ffunction-sections -fdata-sections -nostdlib --param max-inline-insns-single=500 -fno-rtti -fno-exceptions -mcpu=cortex-m0 -mthumb -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


