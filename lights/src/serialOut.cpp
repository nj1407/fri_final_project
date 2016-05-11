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

char state;

void chatterCallback(const std_msgs::String msg)
{
  state = msg.data[0];
}

int baud_rate = B115200;


int main(int argc, char **argv) 
{
	ros::init(argc, argv, "serial_out");
	ros::NodeHandle n;
	ros::Subscriber sub = n.subscribe("/five", 1000, chatterCallback);
	int fd;
	fd = open("/dev/ttyACM2", O_RDWR | O_NOCTTY | O_NDELAY);
	struct termios options;
    options.c_cflag = baud_rate | CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(fd, TCIFLUSH);
    tcsetattr(fd, TCSANOW, &options);
    
    //fstream = fdopen(fd, "rw");
while(ros::ok())
{
	
	if (fd >= 0)
		ROS_INFO("OPEN");
	else
	{
		ROS_INFO("FAILED TO OPEN");
		//cfsetispeed(&port_settings, B115200);
		
	}
	ROS_INFO_STREAM("State: " << state);

	std::string data;
	if (state == 'd')
		data = "" + state;
	else if (state == 'p')
		data = "e";
	else if (state == 'w')
		data = "w 250 0 0";
	else if(state == 'i')
		data = "w 0 250 0";
	else
		data = "w 250 250 0";
	
	
	//int colors = 
	//write(fd, data.c_str(), data.length());
	
	ROS_INFO_STREAM("Wrote " << data);
	close(fd);
	
	ros::spin();
}
	 
	return 0;
		
}