#include "handlepics.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
//may need glbyte

int *giveTexture(char **buffer,int *xval, int *yval) {
  int d;
  int mark1=-1; //indexes for dimensions and different colours
  int mark2=-1;
  int mark3=-1;
  
  for (d=0;d<strlen(buffer[0]);d++) {
    if (buffer[0][d]==' '&&mark1==-1) {
      mark1=d;
    }
    else if (buffer[0][d]==' '&&mark2==-1) {
      mark2=d;
    }
    else if (buffer[0][d]==' '&&mark3==-1) {
      mark3=d;
      break;
    }
  }//fix up this mess later
  //printf("%d %d %d\n",mark1,mark2,mark3);

  //get number ranges based on first line
  char *tip=(char *)malloc(sizeof(char)*(mark1+1));
  for (d=0;d<mark1;d++) {
    tip[d]=buffer[0][d];
  }
  int x=(int)strtol((const char*)tip,NULL,10);//(int)buffer[0][0]-48;
  //printf("%d \n",x);
  char *jip=(char *)malloc(sizeof(char)*(mark2-mark1));
  //jip[0]='4';
  int g=0;
  for (d=mark1+1;d<mark2;d++) {  // in case map is more than 10
    jip[g]=buffer[0][d];
    g++;
  }
  //printf("6%s7\n",jip);
  int y=(int)strtol((const char*)jip,NULL,10);//(int)buffer[0][2]-48;
  //printf("%d\n",y);
  *xval=x;
  *yval=y;
  char *nip=(char *)malloc(sizeof(char)*(mark3-mark2-1));
  g=0;
  for (d=mark2+1;d<mark3;d++) {
    nip[g]=buffer[0][d];
    g++;
  }
  int numColors=(int)strtol((const char*)nip,NULL,10);//(int)buffer[0][4]-48;
  free(nip);
  free(jip);
  free(tip);
  //printf("%d\n",numColors);

  char *bip=(char *)malloc(sizeof(char)*(strlen(buffer[0])-mark3));
  
  g=0;
  for (d=mark3+1;d<strlen(buffer[0]);d++) {
    bip[g]=buffer[0][d];
    g++;
  }
  
  ///REDOOOO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
  int sizeColors=(int)strtol((const char*)bip,NULL,10);//(int)buffer[0][mark3+1]-48; // WE WILL NEED TO REDO IF MORE THAN 10 COLOURS
  free(bip);
  //printf("%d\n",sizeColors);
  char **symbolMap=(char**)malloc(sizeof(char*)*numColors);
  int **rgbMap=(int**)malloc(sizeof(int*)*numColors);
  
  int i;
  int mag=-1;
  //for (i=0;i<=numColors;i++) {
  int j;
  int noneflag=0;
  
  for (j=0;;j++) {
    if (buffer[1][j]=='c') {//note idk if this will be crashed on too many colors
      mag=j+3;
      break;
    }
  }
  for (i=0;i<numColors;i++) {
    //char *symbol=(*char)malloc(sizeof(char)*sizeColors);
    symbolMap[i]=(char*)malloc(sizeof(char)*sizeColors+1);
    
    int h;
    for (h=0;h<sizeColors;h++) {
      //printf("%d %d\n",i,h);
      symbolMap[i][h]=buffer[i+1][h];
    }
    symbolMap[i][h]='\0';
    if (buffer[i+1][mag-1]=='N') {
      rgbMap[i]=(int*)malloc(sizeof(int)*3);
      rgbMap[i][0]=-1;
      rgbMap[i][1]=-1;
      rgbMap[i][2]=-1;
    }
    else {
    rgbMap[i]=(int*)malloc(sizeof(int)*3);
    char *tp=(char *)malloc(sizeof(char)*2);
    tp[0]=buffer[i+1][mag+0];
    tp[1]=buffer[i+1][mag+1];
    rgbMap[i][0]=(int)(strtol((const char*)tp,NULL,16));
    tp[0]=buffer[i+1][mag+2];
    tp[1]=buffer[i+1][mag+3];
    rgbMap[i][1]=(int)(strtol((const char*)tp,NULL,16));
    tp[0]=buffer[i+1][mag+4];
    tp[1]=buffer[i+1][mag+5];
    rgbMap[i][2]=(int)(strtol((const char*)tp,NULL,16));
    //printf("%d %d %d\n",rgbMap[i][0],rgbMap[i][1],rgbMap[i][2]);
    free(tp);
    }
    //free(tpa);
    //free(tpb);
  }
  int *retBuffer=(int*)malloc(sizeof(int)*y*x*4);

  for (i=0;i<y;i++) {
    int u;
    //retBuffer[i]=(*int)malloc(sizeof(*int)*3);
    for (u=0;u<x*sizeColors;u+=sizeColors) {
      char *tmp=(char*)malloc(sizeof(int)*sizeColors+1);
      
      int o;
      //printf("mahh%d %d\n", i ,u);
      for (o=0;o<sizeColors;o++) {
	tmp[o]=buffer[i+numColors+1][u+o];
	//printf("a%ca\n",tmp[o]);
      }
      tmp[o]='\0';
      //printf("%d %d\n",sizeColors,strlen(tmp));
      //printf("|%d|%d|\n",tmp[0],symbolMap[0][0]);
      // printf("%d\n",strlen(tmp));
      //printf("%d\n",strcmp(tmp,symbolMap[0]));          
      int an;
      for (o=0;o<numColors;o++) {
	//printf("char%c\n",symbolMap[o][0]);
	if (strcmp(tmp,symbolMap[o])==0) {
	  an=o;
	  break;
	}
      }
      if (rgbMap[an][0]==-1) {
	
	retBuffer[i*x*4+(u/sizeColors)*4]=0;
	retBuffer[i*x*4+(u/sizeColors)*4+1]=0;
	retBuffer[i*x*4+(u/sizeColors)*4+2]=0;
	retBuffer[i*x*4+(u/sizeColors)*4+3]=0;
      }
      else {
	retBuffer[i*x*4+(u/sizeColors)*4]=rgbMap[an][0];
	retBuffer[i*x*4+(u/sizeColors)*4+1]=rgbMap[an][1];
	retBuffer[i*x*4+(u/sizeColors)*4+2]=rgbMap[an][2];
	retBuffer[i*x*4+(u/sizeColors)*4+3]=255;}
      free(tmp);

    }
    // printf("\n");
  }
  //free buffers
  for (i=0;i<numColors;i++) {
    free(symbolMap[i]);
    free(rgbMap[i]);
  }

  
 free(symbolMap);
 free(rgbMap);
 return retBuffer;
  
      //retBuffer[i][u]=
      
      
    
}
