# Compile without standard flags to decrease size
# Example of LCD initialization of the D-Link DPH-128MS screen
#
# gcc -O3 -s -nostdlib -o LEDInit LEDInit.S
# objcopy -R .reginfo LEDInit
#

#include <asm/regdef.h>
#include <asm/unistd.h>

        .data
lcddev: .asciz	"/dev/lcddev"        
		.text
		.global __start
__start:
        lui		a0, 0x0044
		ori		a0, a0,0x0100
		li      a1, 0x2
        li		v0, __NR_open
        syscall
        move 	s0, v0
        move 	a0, s0
        lui		a1, 0x8004
		ori		a1, a1, 0x6407
		move	a2, zero
		li		v0, __NR_ioctl
  		syscall
  		move	a0, s0
  		li		v0, __NR_close
  		syscall
        li 		a0, 99
        li 		v0, __NR_exit
        syscall        
