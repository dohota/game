#include "display.h"

Bullet::Bullet():Obj(Display::image[1]){
	//空的无参构造函数，让对象数组初始化
}

Bullet::Bullet(int px,int py,char p_direction):Obj(Display::image[1]){
	this->x = px;
	this->y = py;
	//xx,yy是子弹初始位置，是不变的
	this->xx = px;
	this->yy = py;
	this->direction =p_direction;
	this->speed = 4;
	this->distance = 450;
}

void Bullet::move2(char k){
	move(k);
	beyond();
}

void Bullet::beyond(){
	if((xx-x)>(this->distance) || (x-xx)>(this->distance) || (yy-y)>(this->distance) || (y-yy)>(this->distance)){
		Bullet::~Bullet();
	}
}

void Bullet::display(){
	putimage(this->x,this->y,this->img);
}

Bullet::~Bullet(){
	
}
