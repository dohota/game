#include "display.h"

Gun::Gun(int x,int y,char direction){
	this->x = x;
	this->y = y;
	this->shoot_direction = direction;
	this->clip = new Clip(this->x,this->y,this->shoot_direction);
}
char Gun::get_direction(){
	return this->shoot_direction;
}
//queue先进先出
void Gun::shoot(){
	Bullet bu[20];
	for(int i=0;i<20;i++){
		bu[i] = Bullet(this->x,this->y,this->shoot_direction);
		this->clip->load(bu[i]);
	}
	if (!this->clip->bullet.empty()){
		Display::bullet.push_back(this->clip->bullet.front());
		this->clip->bullet.pop();
	}	
}

Gun::Gun(const Gun &g){
	shoot_direction = g.shoot_direction;
	x = g.x;
	y = g.y;
	clip = new Clip(*g.clip);
}

Gun::~Gun(){
	if((this->clip) != NULL){
		delete (this->clip);
		this->clip = NULL;
	}
}

Clip::Clip(int x,int y,char dir){
	this->x = x;
	this->y = y;
	this->dir = dir;
}

void Clip::load(Bullet b){
	this->bullet.push(b);
}

