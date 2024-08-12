#include "num.h"
#include "display.h"

Player::Player(float speed):Obj(Display::image[0]){//显性调用父类构造函数
	this->x = Random::random(0,SCREEN_WIDTH-this->width);
	this->y = Random::random(0,SCREEN_HEIGHT-this->height);
	this->direction = 'w';
	this->speed =speed;
}

Player::Player(const Player &p):Obj(p){
	//gun = new Gun(*p.gun);
}
//如果子类访问父类同名成员要加上作用域
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
		Bullet* b =new Bullet(this->x,this->y,this->direction);
		Display::bullet.push_back(b);
	}
}
//暂时把display函数写在各个子类
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
//Player::~Player(){
//	if((this->gun) != NULL){
//		delete (this->gun);
//		this->gun = NULL;
//	}
//}

