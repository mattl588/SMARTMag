#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<assert.h>
#include<termios.h>
#include<string.h>
#include<sys/time.h>
#include<time.h>
#include<sys/types.h>
#include<errno.h>

static int ret;
static int fd;
int h1; //my own additions 
int h2;
int h3;


#define BAUD 9600 //115200 for JY61 ,9600 for others, defines baudrate before compilation

int uart_open(int fd,const char *pathname) //communicating with UART port. "pathname" is treated as a pointer here; it POINTS to the USB port.
{
    fd = open(pathname, O_RDWR|O_NOCTTY); //flags in the second arg are "read and write" and the terminal will maintain control.
    if (-1 == fd) // -1 is returned upon any error. 
    { 
        perror("Can't Open Serial Port"); //custom error message
		return(-1); //output is fd in main. 
	} 
    else
		printf("open %s success!\n",pathname);
    if(isatty(STDIN_FILENO)==0)  //determines if data is being piped in. Zero is no data is flowing from tty. 
		printf("standard input is not a terminal device\n");  
    else 
		printf("isatty success!\n"); 
    return fd; 
}

int uart_set(int fd,int nSpeed, int nBits, char nEvent, int nStop)
{
     struct termios newtio,oldtio; //declaring three different structures. why?
     if  ( tcgetattr( fd,&oldtio)  !=  0) {  //output is 0 if favorable. Puts info into oldtio struct, which is a pointer. G
       //passes fd object info to oldtio struct. Saves current settings. 
      perror("SetupSerial 1");
	  printf("tcgetattr( fd,&oldtio) -> %d\n",tcgetattr( fd,&oldtio)); //just displaying previous calc 
      return -1; 
     } 
     bzero( &newtio, sizeof( newtio ) );  //clears struct for new port settings
     newtio.c_cflag  |=  CLOCAL | CREAD;  //clocal = local control, cread = enable reading characters from serial
     newtio.c_cflag &= ~CSIZE;  //this is bitwise math that's probably just unusual syntax. Something to do with "masking".
     switch( nBits ) //number of bits per ...message, I think? Set to eight by default. 
     { 
     case 7: 
      newtio.c_cflag |= CS7; 
      break; 
     case 8: 
      newtio.c_cflag |= CS8; //selecting eight data bits
      break; 
     } 
     switch( nEvent ) 
     { 
     case 'o':
     case 'O': 
      newtio.c_cflag |= PARENB; 
      newtio.c_cflag |= PARODD; 
      newtio.c_iflag |= (INPCK | ISTRIP); 
      break; 
     case 'e':
     case 'E': 
      newtio.c_iflag |= (INPCK | ISTRIP); 
      newtio.c_cflag |= PARENB; 
      newtio.c_cflag &= ~PARODD; 
      break;
     case 'n':
     case 'N': //required case. 
      newtio.c_cflag &= ~PARENB; //parity bit "slapped" onto the end of the message. 
      break;
     default:
      break;
     } 

     /*设置波特率*/ 

switch( nSpeed ) //self-explanatory. Just is the baudrate. 
     { 
     case 2400: 
      cfsetispeed(&newtio, B2400); 
      cfsetospeed(&newtio, B2400); 
      break; 
     case 4800: 
      cfsetispeed(&newtio, B4800); 
      cfsetospeed(&newtio, B4800); 
      break; 
     case 9600: 
      cfsetispeed(&newtio, B9600); 
      cfsetospeed(&newtio, B9600); 
      break; 
     case 115200: 
      cfsetispeed(&newtio, B115200); 
      cfsetospeed(&newtio, B115200); 
      break; 
     case 460800: 
      cfsetispeed(&newtio, B460800); 
      cfsetospeed(&newtio, B460800); 
      break; 
     default: 
      cfsetispeed(&newtio, B9600); 
      cfsetospeed(&newtio, B9600); 
     break; 
     } 
     if( nStop == 1 ) //this is always the case. 
      newtio.c_cflag &=  ~CSTOPB; //stopping the bit. what does this mean? 
     else if ( nStop == 2 ) 
      newtio.c_cflag |=  CSTOPB; 
     newtio.c_cc[VTIME]  = 0; //this code doesn't look formatted correctly
     newtio.c_cc[VMIN] = 0; 
     tcflush(fd,TCIFLUSH); 

if((tcsetattr(fd,TCSANOW,&newtio))!=0) 
     { 
      perror("com set error"); 
      return -1; 
     } 
     printf("set done!\n"); 
     return 0; 
}

int uart_close(int fd)
{
    assert(fd);
    close(fd);

    return 0;
}
int send_data(int  fd, char *send_buffer,int length)
{
	length=write(fd,send_buffer,length*sizeof(unsigned char));
	return length;
}
int recv_data(int fd, char* recv_buffer,int length)
{
	length=read(fd,recv_buffer,length);
	return length;
}
float a[3],w[3],Angle[3],h[3];
void ParseData(char chr)
{
		static char chrBuf[100];
		static unsigned char chrCnt=0;
		signed short sData[4]; //small data array which is eventually displayed
		unsigned char i;
		char cTemp=0;
		time_t now;//establishing current time. Called in the switch args. 
		chrBuf[chrCnt++]=chr; //chrBuf[1] = chr. This is the data itself. 
		if (chrCnt<11) return; //why does this exist? chrCnt is a fixed 0. 
		for (i=0;i<10;i++) cTemp+=chrBuf[i];
		if ((chrBuf[0]!=0x55)||((chrBuf[1]&0x50)!=0x50)||(cTemp!=chrBuf[10])) {printf("Error:%x %x\r\n",chrBuf[0],chrBuf[1]);memcpy(&chrBuf[0],&chrBuf[1],10);chrCnt--;return;}
		//above line is error handling. I'll get to it later. 
		memcpy(&sData[0],&chrBuf[2],8); //copies stuff from chrBuf address to sData. Does so for eight bytes. 
		switch(chrBuf[1]) //the actual address. 
		{
				case 0x51: //hexadecimal number. 
					for (i=0;i<3;i++) a[i] = (float)sData[i]/32768.0*16.0;
					time(&now);
					printf("\r\nTime:%s a:%6.3f %6.3f %6.3f ",asctime(localtime(&now)),a[0],a[1],a[2]);

					break;
				case 0x52:
					for (i=0;i<3;i++) w[i] = (float)sData[i]/32768.0*2000.0;
					printf("Angular w:%7.3f %7.3f %7.3f ",w[0],w[1],w[2]);					
					break;
				case 0x53:
					for (i=0;i<3;i++) Angle[i] = (float)sData[i]/32768.0*180.0;
					printf("Theta:%7.3f %7.3f %7.3f ",Angle[0],Angle[1],Angle[2]);
					break;
				case 0x54:
					for (i=0;i<3;i++) h[i] = (float)sData[i];
					printf("nT:%4.0f %4.0f %4.0f ",h[0],h[1],h[2]);
					h1 = h[0];
          h2 = h[1];
          h3 = h[2];
					break;
		}		
		chrCnt=0;		
}iukiju
int main(void)
{
    char r_buf[1024]; //unknown character array of length 1024, or 2^10. 
    bzero(r_buf,1024); //erases the bytestring entirely. 

    fd = uart_open(fd,"/dev/ttyUSB0"); //opening the port for usb 
    if(fd == -1) //integer output for fd. Not static in this scope.
    {
        fprintf(stderr,"uart_open error\n");
        exit(EXIT_FAILURE); //properly closes the program. 
    } //good up to here. 

    if(uart_set(fd,BAUD,8,'N',1) == -1)
    {
        fprintf(stderr,"uart set failed!\n");
        exit(EXIT_FAILURE);
    }
    //everything before this point is just initializing and communicating with the port. 
	FILE *fp;
	fp = fopen("Record.txt","w"); //we have a new fp object now
    while(1)
    {
        ret = recv_data(fd,r_buf,44); //message of length 44 is read from the serial port. It's read into r_buf as a pointer. 
        if(ret == -1)
        {
            fprintf(stderr,"uart read failed!\n");
            exit(EXIT_FAILURE);
        }
		for (int i=0;i<ret;i++) {
      //fprintf(fp,"%i, %i, %i\n", h1, h2, h3);
      ParseData(r_buf[i]);
      usleep(1000);
      }
        usleep(1000);
    }

    ret = uart_close(fd);
    if(ret == -1)
    {
        fprintf(stderr,"uart_close error\n");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}
