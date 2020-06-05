#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dirent.h>

char filename[201];
char cmd_buf[201];

int main()
{
	DIR *d;
	struct dirent *dir;
	d = opendir(".");
	if(d){
		while((dir = readdir(d)) != NULL) {
			strcpy(filename, dir->d_name);
			sprintf(cmd_buf, "/bin/unzip %s -d 2012", filename);
			if(strlen(filename) > 16)
				system(cmd_buf);
		}
		closedir(d);
	}
	return 0;
}

