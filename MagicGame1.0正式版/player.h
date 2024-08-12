#ifndef PLAYER_H
#define PLAYER_H

#endif

#include "tool.h"
class Player:public Obj{
//protected:
	//Gun* gun;
	//ToolBag<T> toolbag;搞个泛型竟然要把player也设置成为模板类！
public:
	using Obj::Obj; // c++11继承父类的构造函数
	Player(float speed);
	Player(const Player &p);
	void move2(char k);
	void control();
	void display();
	//~Player();
};

