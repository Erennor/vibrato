################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../rfduino_core/libraries/kiss_fft130/tools/fftutil.c \
../rfduino_core/libraries/kiss_fft130/tools/kfc.c \
../rfduino_core/libraries/kiss_fft130/tools/kiss_fastfir.c \
../rfduino_core/libraries/kiss_fft130/tools/kiss_fftnd.c \
../rfduino_core/libraries/kiss_fft130/tools/kiss_fftndr.c \
../rfduino_core/libraries/kiss_fft130/tools/kiss_fftr.c \
../rfduino_core/libraries/kiss_fft130/tools/psdpng.c 

OBJS += \
./rfduino_core/libraries/kiss_fft130/tools/fftutil.o \
./rfduino_core/libraries/kiss_fft130/tools/kfc.o \
./rfduino_core/libraries/kiss_fft130/tools/kiss_fastfir.o \
./rfduino_core/libraries/kiss_fft130/tools/kiss_fftnd.o \
./rfduino_core/libraries/kiss_fft130/tools/kiss_fftndr.o \
./rfduino_core/libraries/kiss_fft130/tools/kiss_fftr.o \
./rfduino_core/libraries/kiss_fft130/tools/psdpng.o 

C_DEPS += \
./rfduino_core/libraries/kiss_fft130/tools/fftutil.d \
./rfduino_core/libraries/kiss_fft130/tools/kfc.d \
./rfduino_core/libraries/kiss_fft130/tools/kiss_fastfir.d \
./rfduino_core/libraries/kiss_fft130/tools/kiss_fftnd.d \
./rfduino_core/libraries/kiss_fft130/tools/kiss_fftndr.d \
./rfduino_core/libraries/kiss_fft130/tools/kiss_fftr.d \
./rfduino_core/libraries/kiss_fft130/tools/psdpng.d 


# Each subdirectory must supply rules for building sources it contributes
rfduino_core/libraries/kiss_fft130/tools/%.o: ../rfduino_core/libraries/kiss_fft130/tools/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	arm-none-eabi-gcc -DF_CPU=16000000 -DARM_MATH_CM0 -Dprintf=iprintf -DARDUINO=157 -D__RFduino__ -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/cores/arduino" -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/kiss_fft130 -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher/nrf51822/Include -I/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/libraries/memory_watcher -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/variants/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/RFduino/include" -I"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/system/CMSIS/CMSIS/Include" -Os -g -Wall -c -ffunction-sections -fdata-sections -nostdlib --param max-inline-insns-single=500 -mcpu=cortex-m0 -mthumb -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


