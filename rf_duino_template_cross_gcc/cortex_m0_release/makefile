################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include rfduino_core/variants/RFduino/subdir.mk
-include rfduino_core/system/RFduino/source/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/TransformFunctions/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/SupportFunctions/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/StatisticsFunctions/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/MatrixFunctions/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/FilteringFunctions/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/FastMathFunctions/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/ControllerFunctions/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/ComplexMathFunctions/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/CommonTables/subdir.mk
-include rfduino_core/system/CMSIS/CMSIS/DSP_Lib/Source/BasicMathFunctions/subdir.mk
-include rfduino_core/libraries/RFduinoNonBLE/subdir.mk
-include rfduino_core/libraries/RFduinoGZLL/subdir.mk
-include rfduino_core/libraries/RFduinoBLE/subdir.mk
-include rfduino_core/cores/arduino/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: rf_duino_template_cross_gcc

# Tool invocations
rf_duino_template_cross_gcc: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: Cross G++ Linker'
	arm-none-eabi-g++ -L"/home/robin/Travail/ProjetSpé/vibrato/rf_duino_template_cross_gcc/rfduino_core/variants/RFduino" -Os -Wl,--gc-sections -mcpu=cortex-m0 -mthumb -D__RFduino__ -T../rfduino_core/variants/RFduino/linker_scripts/gcc/RFduino.ld -Wl,-Map,rf_duino_template_cross_gcc.map -o "rf_duino_template_cross_gcc" $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '
	$(MAKE) --no-print-directory post-build

# Other Targets
clean:
	-$(RM) $(C++_DEPS)$(OBJS)$(C_DEPS)$(CC_DEPS)$(CPP_DEPS)$(EXECUTABLES)$(CXX_DEPS)$(C_UPPER_DEPS) rf_duino_template_cross_gcc
	-@echo ' '

post-build:
	-arm-none-eabi-objcopy -O ihex ./rf_duino_template_cross_gcc ./rf_duino_template_cross_gcc.hex;  ../rfduino_core/RFDLoader_linux -q /dev/ttyUSB0 ./rf_duino_template_cross_gcc.hex
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY: post-build

-include ../makefile.targets
