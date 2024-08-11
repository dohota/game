#include "num.h"
#include "display.h"
//显性调用父类构造函数
Player::Player(float speed):Obj(Display::image[0]){
	this->x = Random::random(0,SCREEN_WIDTH-this->width);
	this->y = Random::random(0,SCREEN_HEIGHT-this->height);
	this->direction = 'w';
	this->speed =speed;
	this->gun = new Gun(this->x,this->y,this->direction);
	//gun是Gun型指针,*gun是Gun的实例化对象
	Display::gun.push_back(this->gun);
}

Player::Player(const Player &p):Obj(p){
	gun = new Gun(*p.gun);
}
//子类访问父类同名成员要加上作用域
void Player::move2(char k){
	move(k);
	border();
}

void Player::control(){
	if (keystate(key_W)) {
		move2('w');
	}else if(keystate(key_S)){
		move2('s');
	}else if(keystate(key_A)){
		move2('a');
	}else if(keystate(key_D)){
		move2('d');
	}else if(keystate(key_J)){
		this->gun->shoot();
		//gun是指针，指向Gun类对象的成员函数
	}
}
void Player::display(){
	if(this->direction == 'w'){
		putimage(this->x,this->y,this->img);	
	}else if(this->direction == 's'){
		putimage_rotate(NULL,this->img,this->x+this->width/2,this->y+this->height/2,0.5,0.5,PI);
	}else if(this->direction == 'a'){
		putimage_rotate(NULL,this->img,this->x+this->width/2,this->y+this->height/2,0.5,0.5,PI/2);
	}else if(this->direction == 'd'){
		putimage_rotate(NULL,this->img,this->x+this->width/2,this->y+this->height/2,0.5,0.5,-PI/2);
	}
}
//父类构造函数会自动调用
//清空堆内存
Player::~Player(){
	if((this->gun) != NULL){
		delete (this->gun);
		this->gun = NULL;
	}
}

