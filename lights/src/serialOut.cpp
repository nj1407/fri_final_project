#include <stdio.h> // standard input / output functions
#include <string.h> // string function definitions
#include <unistd.h> // UNIX standard function definitions
#include <fcntl.h> // File control definitions
#include <errno.h> // Error number definitions
#include <termios.h> // POSIX terminal control definitionss
#include <time.h>
#include <ros/ros.h>
#include "std_msgs/String.h"

//String data = 

//bool SerialConnection::send_data(const std::string &data)
//{
//    int written_bytes = write(fd, data.c_str(), data.length());
//    ROS_INFO_STREAM("Wrote " << written_bytes << " bytes");
//    return written_bytes == data.length();
//}

char state = 'i';
char lastState = 'x';
bool rcv = true;
bool change = true;
int count;
std::string data;

void chatterCallback(const std_msgs::String msg)
{
  state = msg.data[0];
	rcv = true;
}

int baud_rate = B115200;


int main(int argc, char **argv) 
{
	ros::init(argc, argv, "serial_out");
	ros::NodeHandle n;
	ros::Subscriber sub = n.subscribe("five", 1000, chatterCallback);
	int fd;
	fd = open("/dev/ttyACM2", O_RDWR | O_NOCTTY | O_NDELAY);
	struct termios options;
    options.c_cflag = baud_rate | CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(fd, TCIFLUSH);
    tcsetattr(fd, TCSANOW, &options);

	if (fd >= 0)
		ROS_INFO("OPEN");
	else
	{
		ROS_INFO("FAILED TO OPEN");
		//cfsetispeed(&port_settings, B115200);
		
	}
    
    //fstream = fdopen(fd, "rw");
	ros::Rate loop_rate(1000);
	while(ros::ok())
	{
		ros::spinOnce();
		while(!rcv && ros::ok())
		{
			ros::spinOnce();
			loop_rate.sleep();
		}
		rcv = false;
	
		if(state != 'p' && change)
		{
			lastState = state;
	
	
			ROS_INFO_STREAM("State: " << state);

			
			if (state == 'd')
				data = "d 0 0 0";
			else if (state == 'p')
				data = "e 0 0 0";
			else if (state == 'w')
				data = "b 250 0 0";
			else if(state == 'i')
				data = "w 0 250 0";
			else
				data = "w 250 250 0";
	
	
			//int colors = 
			write(fd, data.c_str(), data.length());
	
			ROS_INFO_STREAM("Wrote " << data);
		}
		else
		{
			if(count <= 20)
			{
				change = false;
				data = "e 0 0 0";
				write(fd, data.c_str(), data.length());
				ROS_INFO_STREAM("Wrote " << data);
				count++;
			}
			else
			{
				count = 0;
				change = true;
			}
		}
	
	
	
}
close(fd);
	 
	return 0;
		
}
