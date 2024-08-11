#ifndef TOOL_H
#define TOOL_H
#endif
#include "obj.h"
#include <vector>
#include <list>
#include <queue>
//各种武器，背包，身体机制等参考逃离塔克夫
class Clip{
	int x;
	int y;
	char dir;
	
public:
	std::queue<Bullet> bullet;	//弹夹中子弹
	Clip(int x,int y,char dir);
	void load(Bullet b);
};

class Knife{
	
};

class Gun{
	int x;
	int y;
	char shoot_direction;//发射方向
	//char shoot_way; //发射子弹的方式
	Clip* clip;//弹夹
public:
	Gun(int x,int y,char direction);
	Gun(const Gun &g);
	char get_direction();
	void shoot();
	//void change_clip();//换弹夹
	~Gun();
};
template <class T>
class ToolBag{
	//背包本身尺寸
	int x;
	int y;
	int z;
	//背包能装载的质量
	int m;
	ToolBag(int x,int y, int z,int m);
	//背包中物品
	std::list<T> tools;
	//每个物品具体放在什么位置
};


