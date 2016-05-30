################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../rfduino_core/libraries/kiss_fft130/test/benchfftw.c \
../rfduino_core/libraries/kiss_fft130/test/benchkiss.c \
../rfduino_core/libraries/kiss_fft130/test/doit.c \
../rfduino_core/libraries/kiss_fft130/test/pstats.c \
../rfduino_core/libraries/kiss_fft130/test/test_real.c \
../rfduino_core/libraries/kiss_fft130/test/test_vs_dft.c \
../rfduino_core/libraries/kiss_fft130/test/twotonetest.c 

CC_SRCS += \
../rfduino_core/libraries/kiss_fft130/test/testcpp.cc 

OBJS += \
./rfduino_core/libraries/kiss_fft130/test/benchfftw.o \
./rfduino_core/libraries/kiss_fft130/test/benchkiss.o \
./rfduino_core/libraries/kiss_fft130/test/doit.o \
./rfduino_core/libraries/kiss_fft130/test/pstats.o \
./rfduino_core/libraries/kiss_fft130/test/test_real.o \
./rfduino_core/libraries/kiss_fft130/test/test_vs_dft.o \
./rfduino_core/libraries/kiss_fft130/test/testcpp.o \
./rfduino_core/libraries/kiss_fft130/test/twotonetest.o 

C_DEPS += \
./rfduino_core/libraries/kiss_fft130/test/benchfftw.d \
./rfduino_core/libraries/kiss_fft130/test/benchkiss.d \
./rfduino_core/libraries/kiss_fft130/test/doit.d \
./rfduino_core/libraries/kiss_fft130/test/pstats.d \
./rfduino_core/libraries/kiss_fft130/test/test_real.d \
./rfduino_core/libraries/kiss_fft130/test/test_vs_dft.d \
./rfduino_core/libraries/kiss_fft130/test/twotonetest.d 

CC_DEPS += \
./rfduino_core/libraries/kiss_fft130/test/testcpp.d 


# Each subdirectory must supply rules for building sources it contributes
rfduino_core/libraries/kiss_fft130/test/%.o: ../rfduino_core/libraries/kiss_fft130/test/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	arm-none-eabi-gcc -DF_CPU=16000000 -DARM_MATH_CM0 -Dprintf=iprintf -DARDUINO=157 -D__RFduino__ -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/cores/arduino" -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/kiss_fft130 -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher/nrf51822/Include -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/variants/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino/include" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/CMSIS/CMSIS/Include" -Os -g -Wall -c -ffunction-sections -fdata-sections -nostdlib --param max-inline-insns-single=500 -mcpu=cortex-m0 -mthumb -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

rfduino_core/libraries/kiss_fft130/test/%.o: ../rfduino_core/libraries/kiss_fft130/test/%.cc
	@echo 'Building file: $<'
	@echo 'Invoking: Cross G++ Compiler'
	arm-none-eabi-g++ -DF_CPU=16000000 -DARM_MATH_CM0 -Dprintf=iprintf -DARDUINO=157 -D__RFduino__ -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/RFduinoBLE" -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/kiss_fft130 -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher/nrf51822/Include -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/cores/arduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/variants/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino/include" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/CMSIS/CMSIS/Include" -Os -g -Wall -c -ffunction-sections -fdata-sections -nostdlib --param max-inline-insns-single=500 -fno-rtti -fno-exceptions -mcpu=cortex-m0 -mthumb -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


