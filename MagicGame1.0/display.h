#ifndef DISPLAY_H
#define DISPLAY_H
#endif
#include "player.h"
//渲染屏幕上所有东西
//渲染和逻辑分离
class Display{
public:
	static std::vector<PIMAGE>image;
	//LPCSTR为图片路径
	static std::vector<Player> player;
	static std::vector<Bullet> bullet;
	static std::vector<Gun*> gun;
	
	template <typename T>
	static std::vector<T> tool_bag;
	//背包里所有的东西，交给gui显示
	Display();
	void show();
	~Display();
};

