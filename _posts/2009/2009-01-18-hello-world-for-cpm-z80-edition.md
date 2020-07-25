---
title: Hello World for CP/M (Z80 Edition)
data: 2009-01-18
---

As the current obsession is to build a Z80 microcomputer, myself and Ed decided
it might be a good idea to be able to actually write some Z80 programs.

Using the assembly language experience we had in other languages, other people's
simple .mac files and basically Googling any gaps in our information (memory
maps, register lists, valid opcodes) we got "Hello World" in under an hour.

```
	.Z80

BOOT    EQU 0000H ; Where BDOS' map begins.
BDOS    EQU BOOT+05H ; Do a SysCall.
PRINTST EQU 9 ; Print.

	ASEG
	ORG 0100H

	LD  HL,0 ; Set up 512b of stack, actually don't think we need this.
	ADD HL,SP
	LD  (STACK),HL
	LD  HL,CEND
	PUSH DE
	LD DE,512
	ADD HL,DE
	POP DE
	LD  SP,HL

	PUSH DE ; Parameters seem to go in this register.
	LD DE,TEXT1
	PUSH AF
	PUSH BC
	PUSH HL
	LD C,PRINTST ; C holds the SysCall we want.
	CALL BDOS
	POP HL
	POP BC
	POP AF
	POP DE

	JP BOOT ; Return to the OS.

TEXT1:	DB 'Hello, world$'
STACK:	DS 2 ; Somewhere to store the original stack. Probably unneeded.
CEND	EQU $

	END	
```

Considering the scale of the systems I manage, and Ed develops, on a daily
basis, there is something unbelievably cool about using technology that's older
than you are to build things.