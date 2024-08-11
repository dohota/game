#include "display.h"
//在类外对类的静态变量进行初始化，像这种复杂类型需要显式初始化。在xxx.h里声明了一般就在xxx.cpp里初始化
std::vector<PIMAGE> Display::image;
std::vector<Player> Display::player;
std::vector<Bullet> Display::bullet;
std::vector<Gun*> Display::gun;

Display::Display(){
	PIMAGE i1 = NULL;
	PIMAGE i2 = NULL;
	//i1 =newimage();
	// = newimage();
	//getimage(i1,"player.png");
	//(i2,"bullet.png");
	Display::image.push_back(i1);
	Display::image.push_back(i2);
}
void Display::show(){
	//i不用unsigned类型会弹出警告
	for (unsigned i = 0; i < Display::player.size(); i++){
		Display::player[i].control();
		Display::player[i].display();
	}
//	for(unsigned i = 0; i< Display::gun.size();i++){
//		
//	}
	for (unsigned i = 0;i < Display::bullet.size(); i++){
		bullet[i].move2(gun[0]->get_direction());
		bullet[i].display();
	}	
}
//template <class T>//如果是模板类.h和.cpp文件中都需要这行代码
Display::~Display(){
	
}
