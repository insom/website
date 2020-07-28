/*
 * Create an ALSA midi output which changes pitch according to the position
 * of a Griffin Powermate.
 *
 * Copyright 2007 - Aaron Brady <bradya@gmail.com>
 */

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <alsa/asoundlib.h>
#include <alsa/asoundef.h>
#include <alsa/global.h>
#include <alsa/rawmidi.h>
#include <linux/input.h>

int current_note, previous_note;
snd_rawmidi_t *output;

void play() {
	char buffer[512] = {0};
	int sz;

	/* Notes: 90 on, 80 off, B0 cc, C0 pc, E0 bend */
	buffer[0] = 0x80;
	buffer[1] = previous_note;
	buffer[2] = 64;
	sz = snd_rawmidi_write(output, buffer, 3);
	printf("(off)snd:rawmidi:write-%X\n", sz);
	buffer[0] = 0x90;
	buffer[1] = current_note;
	buffer[2] = 64;
	sz = snd_rawmidi_write(output, buffer, 3);
	printf("(on)snd:rawmidi:write-%X\n", sz);
}

int main(int argc, char **argv) {
	int inputf, e;
	struct input_event buffer;

	if(argc < 2) {
		fprintf(stderr, "%s /dev/input/event<X>\n", argv[0]);
		exit(-1);
	}
	current_note = 64;
	previous_note = 64;
	inputf = open(argv[1], O_RDONLY);
	printf("open-%X\n", inputf);
	e = snd_rawmidi_open(NULL, &output, "virtual", O_WRONLY);
	printf("snd:rawmidi:open-%X\n", e);

	while(1) {
		read(inputf, &buffer, 16);
		current_note = current_note + buffer.value;
		if(current_note < 0) current_note = 0;
		if(current_note > 127) current_note = 127;
		play();
		previous_note = current_note;
	}

	return 0;
}
