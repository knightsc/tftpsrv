/**
 * This is the reversed strucuture of the D-Link DPH-128MS tftpsrv main function
 */
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>

void sys_begin_thread(void *(*start_routine)(void *), void *arg)
{
	pthread_t thread;
	pthread_create(&thread, NULL, start_routine, arg);
}

void sys_thread_exit()
{
	pthread_exit(NULL);
}

int sys_sleep(unsigned int usec)
{
	return usleep(usec);
}

int sys_current_time()
{
	//get_time_of_day
	return 0;
}

void get_all_if()
{
	//
}

void initialize()
{
	//unpack config files if needed
}

void run_server()
{
}

void *tftp_auto_free_thread(void *param)
{
	while (1)
	{
		sys_sleep(1000);
		printf("tftp auto free\n");
	}
}

void *lcd_thread(void *param)
{
	//LCDInit
	//wait for something then do it
	//LCDFin
	sys_thread_exit();
}

void read_setupinfo()
{
}

int main(int argc, char *argv[])
{
	pid_t child;

	child = fork();

	if (child > 0)
	{
		printf("TFTP Server PID = %d\n", child);
		exit(0);
	}
	else
	{
		//sigemptyset
		//sigaction
		//sigaction

		//system("insmod /sbin/act_lcd.o;insmod /sip/sdvepfxs.o;insmod /sip/sdvepvoip.o");
		sys_sleep(100);

		get_all_if();

		printf("===============================\n");
		printf("TFTP_SRV V: 03.02.00 2008.01.09\n");
		printf("\n");

		initialize();

		sys_current_time();

		sys_begin_thread(lcd_thread, NULL);
		sys_begin_thread(tftp_auto_free_thread, NULL);

		read_setupinfo();

		sys_sleep(4000);

		//system("cd /sbin;chmod 755 act_sip;./act_sip ph");

		run_server();
	}
}