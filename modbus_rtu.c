#include <stdio.h>
#include <stdlib.h>
#include <modbus/modbus.h>
#include <modbus/modbus-rtu.h>
int main()
{
	modbus_t *ctx; //declare new modbus element variable
	uint16_t reg[2]; //two byte elements in array to store all registers
	int i,rc;

	// set up modbus client on UART device

	retry:
	ctx = modbus_new_rtu("/dev/ttyAMA0", 19200, 'N', 8, 1);

	modbus_set_slave(ctx, 2); //slave ID

	modbus_rtu_set_serial_mode(ctx, MODBUS_RTU_RS485); //setup modbus for RS485

	modbus_rtu_set_rts(ctx, MODBUS_RTU_RTS_DOWN); //setup RTS available on regular polarity

	if(modbus_connect(ctx) == -1) //establish connection and check for error
	{
		printf("Connexion Failed\n");
		modbus_free(ctx);
		exit(1);
	}

	//read registers

	rc = modbus_read_registers(ctx, 3900, 2, reg);

	for(i=1; i<=30,000; i++) //delay
	{
	}

	if(rc == -1)
	{
		printf("ERROR. trying again\n");
		modbus_free(ctx);
		modbus_close(ctx);
		goto retry;
	}

	printf("1st register is %d\n", reg[0]);
	printf("2nd register is %d\n", reg[1]);

	modbus_close(ctx);
	modbus_free(ctx);
	exit(1);
	return 0;
}
