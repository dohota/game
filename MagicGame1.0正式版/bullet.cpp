#include "display.h"
Bullet::Bullet(int px,int py,char p_direction):Obj(Display::image[1]){
	this->x = px;
	this->y = py;
	//xx,yy是子弹初始位置，是不变的
	this->xx = px;
	this->yy = py;
	this->direction =p_direction;
	this->speed = 10;
	this->alive = true;
	this->distance = 200;
}
Bullet::Bullet(const Bullet &b):Obj(b){
	xx = b.xx;
	yy = b.yy;
	distance = b.distance;
}
void Bullet::beyond(){
	if((this->xx)-(this->x)>(this->distance) || (this->x-this->xx)>(this->distance)
		|| (this->yy-this->y)>(this->distance) || (this->y-this->yy)>(this->distance)){
		this->alive =false;
	}
}
void Bullet::move2(char k){
	beyond();
	move(k);
}
void Bullet::display(){
	putimage(this->x,this->y,this->img);
}

Bullet::~Bullet(){
	
}

