################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../rfduino_core/cores/arduino/Print.cpp \
../rfduino_core/cores/arduino/RingBuffer.cpp \
../rfduino_core/cores/arduino/Stream.cpp \
../rfduino_core/cores/arduino/Tone.cpp \
../rfduino_core/cores/arduino/UARTClass.cpp \
../rfduino_core/cores/arduino/WMath.cpp \
../rfduino_core/cores/arduino/WString.cpp \
../rfduino_core/cores/arduino/main.cpp \
../rfduino_core/cores/arduino/wiring_pulse.cpp 

C_SRCS += \
../rfduino_core/cores/arduino/Memory.c \
../rfduino_core/cores/arduino/WInterrupts.c \
../rfduino_core/cores/arduino/hooks.c \
../rfduino_core/cores/arduino/itoa.c \
../rfduino_core/cores/arduino/syscalls.c \
../rfduino_core/cores/arduino/wiring.c \
../rfduino_core/cores/arduino/wiring_analog.c \
../rfduino_core/cores/arduino/wiring_digital.c \
../rfduino_core/cores/arduino/wiring_shift.c 

OBJS += \
./rfduino_core/cores/arduino/Memory.o \
./rfduino_core/cores/arduino/Print.o \
./rfduino_core/cores/arduino/RingBuffer.o \
./rfduino_core/cores/arduino/Stream.o \
./rfduino_core/cores/arduino/Tone.o \
./rfduino_core/cores/arduino/UARTClass.o \
./rfduino_core/cores/arduino/WInterrupts.o \
./rfduino_core/cores/arduino/WMath.o \
./rfduino_core/cores/arduino/WString.o \
./rfduino_core/cores/arduino/hooks.o \
./rfduino_core/cores/arduino/itoa.o \
./rfduino_core/cores/arduino/main.o \
./rfduino_core/cores/arduino/syscalls.o \
./rfduino_core/cores/arduino/wiring.o \
./rfduino_core/cores/arduino/wiring_analog.o \
./rfduino_core/cores/arduino/wiring_digital.o \
./rfduino_core/cores/arduino/wiring_pulse.o \
./rfduino_core/cores/arduino/wiring_shift.o 

C_DEPS += \
./rfduino_core/cores/arduino/Memory.d \
./rfduino_core/cores/arduino/WInterrupts.d \
./rfduino_core/cores/arduino/hooks.d \
./rfduino_core/cores/arduino/itoa.d \
./rfduino_core/cores/arduino/syscalls.d \
./rfduino_core/cores/arduino/wiring.d \
./rfduino_core/cores/arduino/wiring_analog.d \
./rfduino_core/cores/arduino/wiring_digital.d \
./rfduino_core/cores/arduino/wiring_shift.d 

CPP_DEPS += \
./rfduino_core/cores/arduino/Print.d \
./rfduino_core/cores/arduino/RingBuffer.d \
./rfduino_core/cores/arduino/Stream.d \
./rfduino_core/cores/arduino/Tone.d \
./rfduino_core/cores/arduino/UARTClass.d \
./rfduino_core/cores/arduino/WMath.d \
./rfduino_core/cores/arduino/WString.d \
./rfduino_core/cores/arduino/main.d \
./rfduino_core/cores/arduino/wiring_pulse.d 


# Each subdirectory must supply rules for building sources it contributes
rfduino_core/cores/arduino/%.o: ../rfduino_core/cores/arduino/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	arm-none-eabi-gcc -DF_CPU=16000000 -DARM_MATH_CM0 -Dprintf=iprintf -DARDUINO=157 -D__RFduino__ -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/cores/arduino" -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/kiss_fft130 -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher/nrf51822/Include -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/variants/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino/include" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/CMSIS/CMSIS/Include" -Os -g -Wall -c -ffunction-sections -fdata-sections -nostdlib --param max-inline-insns-single=500 -mcpu=cortex-m0 -mthumb -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

rfduino_core/cores/arduino/%.o: ../rfduino_core/cores/arduino/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cross G++ Compiler'
	arm-none-eabi-g++ -DF_CPU=16000000 -DARM_MATH_CM0 -Dprintf=iprintf -DARDUINO=157 -D__RFduino__ -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/RFduinoBLE" -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/kiss_fft130 -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher/nrf51822/Include -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/cores/arduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/variants/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino/include" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/CMSIS/CMSIS/Include" -Os -g -Wall -c -ffunction-sections -fdata-sections -nostdlib --param max-inline-insns-single=500 -fno-rtti -fno-exceptions -mcpu=cortex-m0 -mthumb -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


