#include <random>
#include "obj.h"
#include "num.h"

int Random::random(int a,int b){
	std::random_device rd; // 随机数种子
	std::mt19937 gen(rd()); // 使用Mersenne Twister 19937算法生成随机数引擎
	std::uniform_real_distribution<double> dis(0.0, 1.0); // 定义在[0, 1)范围内的均匀分布随机数
	double random = dis(gen); // 生成0到1之间的随机数
	return random *(b-a) +a;
}
//this指针的用途是让类的实例对象调用其成员函数，this指针指向调用成员函数的实例对象
//类的非静态成员函数中返回对象本身：return *this;

Obj::Obj(PIMAGE img){
	this->img = img;
	this->img = newimage();
	getimage(this->img,"player.png");
	this->width = getwidth(img);
	this->height = getheight(img);
}

Obj::Obj(const Obj &o){
	direction = o.direction;
	x = o.x;
	y = o.y;
	speed = o.speed;
	width = o.width;
	height = o.height;
}

void Obj::border(){
	if(this->x < 0){
		this->x = SCREEN_WIDTH-this->width;
	}else if(this->x > SCREEN_WIDTH-this->width){
		this->x = 0;
	}else if(this->y < 0){
		this->y = SCREEN_HEIGHT-this->height;
	}else if(this->y >SCREEN_HEIGHT-this->height){
		this->y = 0;
	}
}

void Obj::move(char k){
		if (k == 'w') {  
			this->direction = 'w';
			this->y -= this->speed;
		} else if (k == 's') {  
			this->direction = 's';
			this->y += this->speed;
		} else if (k == 'a') {  
			this->direction = 'a';
			this->x -= this->speed;
		} else if (k == 'd') {  
			this->direction = 'd';
			this->x += this->speed;
		}	
}
//	void Obj::display(){
//		if(this->direction == 'w'){
//			putimage(this->x,this->y,this->img);	
//		}else if(this->direction == 's'){
//			putimage_rotate(NULL,this->img,this->x+this->width/2,this->y+this->height/2,0.5,0.5,PI);
//		}else if(this->direction == 'a'){
//			putimage_rotate(NULL,this->img,this->x+this->width/2,this->y+this->height/2,0.5,0.5,PI/2);
//		}else if(this->direction == 'd'){
//			putimage_rotate(NULL,this->img,this->x+this->width/2,this->y+this->height/2,0.5,0.5,-PI/2);
//		}
//	}
// 使用newimage() 创建的图像是动态内存分配的图像，不使用时需要使用 delimage(pimg) 进行销毁
Obj::~Obj(){
	delimage(this->img);
}

