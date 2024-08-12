#ifndef DISPLAY_H
#define DISPLAY_H
#endif
#include "player.h"
//渲染屏幕上所有东西
//渲染和逻辑分离
class Display{
public:
	static PIMAGE image[20];
	//LPCSTR为图片路径
	static std::vector<Player> player;
	static std::vector<Bullet*> bullet;
	Display();
	void show();
};

