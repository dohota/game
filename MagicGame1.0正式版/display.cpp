#include "display.h"
//在类外对类的静态变量进行初始化，像这种复杂类型需要显式初始化
PIMAGE Display::image[20] = {nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,nullptr};
std::vector<Player> Display::player;
std::vector<Bullet*> Display::bullet;

Display::Display(){
	for(int i=0;i<20;i++){
		image[i] =newimage();
	}
	getimage(image[0],"player.png");
	getimage(image[1],"bullet.png");
}
void Display::show(){
	for (unsigned i = 0; i < player.size(); i++){//i不用unsigned类型会弹出警告
		player[i].control();
		player[i].display();
	}
	for (unsigned i = 0;i < bullet.size(); i++){
		if(bullet[i]->alive){
			bullet[i]->move2(bullet[i]->direction);
			bullet[i]->display();
		}
	}
}
//delete不知道为什么会报错
//		else{
//			delete bullet[i];
//			bullet[i] = nullptr;
//			bullet.erase(bullet.begin() + i); // 从容器中移除已删除的对象
//			i--; // 更新索引，使得后续循环能够正确处理
//		}	
		
//template <class T>//如果是模板类.h和.cpp文件中都需要这行代码

